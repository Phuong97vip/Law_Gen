import openai
import json
from config import OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def generate_response(prompt):
    # Call OpenAI API to generate responses
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=16384,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def generate_questions_and_answers(pdf_text):
    prompt = (
        "Dựa trên nội dung tài liệu pháp lý dưới đây, tạo ra 100 câu hỏi và câu trả lời có ý nghĩa "
        "cho mỗi câu hỏi, cung cấp câu trả lời ngắn gọn và rõ ràng. "
        "Ngoài ra, bao gồm tham chiếu từ tài liệu nơi thông tin được tìm thấy. "
        "Output chỉ là JSON hợp lệ (mảng JSON) mà không có văn bản thừa. "
        "JSON phải theo định dạng chính xác này:\n\n"
        "[{\"user_input\": \"câu hỏi\", \"response\": \"câu trả lời\", \"reference\": \"trích dẫn tài liệu\"}]\n\n"
        "Tài liệu pháp lý:\n\n"
        f"{pdf_text}"
    )


    response = generate_response(prompt)
    
    # Debug: print the raw API response
    print("Raw API response:", response)

    # Clean up the response further, removing unwanted characters
    cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', ' ').replace('\r', '')

    # Handle possible unterminated string or JSON format issues
    if cleaned_response.endswith(','):
        cleaned_response = cleaned_response[:-1]  # Remove trailing comma if present

    # Try parsing the cleaned-up response
    try:
        formatted_response = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"Lỗi: Phản hồi không phải là định dạng JSON hợp lệ. Lỗi: {e}")
        print(f"Raw Response that failed parsing: {repr(cleaned_response)}")
        formatted_response = []

    return formatted_response

def format_questions_and_answers(response):
    questions_and_answers = []
    try:
        # Remove any extra spaces, newline characters, or unexpected characters before parsing
        response = response.strip()
        
        # Debugging: Print the response right before parsing to check for issues
        print(f"Response before parsing: {repr(response)}")
        
        # Ensure the response starts with "[" and ends with "]"
        if response.startswith("[") and response.endswith("]"):
            questions_and_answers = json.loads(response)
        else:
            print(f"Lỗi: Phản hồi không phải là định dạng JSON hợp lệ: {response}")
    except Exception as e:
        # Provide more detailed error information
        print(f"Lỗi khi định dạng câu hỏi và câu trả lời: {e}")
        print(f"Error parsing response: {repr(response)}")  # Print the raw response in a safe format
    return questions_and_answers

def generate_response_from_pdf(query, pdf_text):
    # Create a prompt that will query the content and provide the reference in Vietnamese
    prompt = f"Dựa trên nội dung tài liệu pháp lý dưới đây:\n\n{pdf_text}\n\nTrả lời câu hỏi sau:\n{query}\nTrả lời (bằng tiếng Việt):"
    response = generate_response(prompt)
    
    # Extract reference from the PDF
    reference = extract_reference_from_pdf(query, pdf_text)
    
    return response, reference

def extract_reference_from_pdf(query, pdf_text):
    """
    Extracts a meaningful reference from the PDF text based on the user's query.
    The reference should provide surrounding context for the keyword found in the query.
    """
    # Define a list of possible keywords from the query that could serve as reference points
    keywords = ["Điều", "Khoản", "Luật", "Thông tư", "Nghị định", "Hiến pháp"]
    
    reference = None
    
    # Search for each keyword in the text
    for keyword in keywords:
        start_idx = pdf_text.lower().find(keyword)
        
        if start_idx != -1:
            # Get some text before and after the keyword to provide a better context
            context_start_idx = max(0, start_idx - 300)  # 300 characters before the keyword
            context_end_idx = min(start_idx + 500 + len(keyword), len(pdf_text))  # 500 characters after the keyword

            reference = pdf_text[context_start_idx:context_end_idx]
            reference = f"{reference.strip()}"
            break
    
    # If no keyword was found, provide a default message
    if reference is None:
        reference = "Không tìm thấy tham chiếu rõ ràng từ tài liệu."
    
    return reference
