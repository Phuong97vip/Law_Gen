# chatbot.py
import openai
import json
import os  
import pdfplumber
from config import PDF_FILE_PATH_2


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


# Function to extract a snippet from the PDF based on a reference
def extract_snippet_from_pdf(reference, pdf_text):
    """
    Extracts a relevant snippet from the PDF based on the reference (e.g., 'Điều 1').
    Returns the snippet and its span.
    """
    # Find the reference in the text
    start_idx = pdf_text.find(reference)

    if start_idx == -1:
        print(f"Reference '{reference}' not found in the PDF.")
        return None, None

    # Extract a context window around the reference
    context_start_idx = max(0, start_idx - 100)
    context_end_idx = min(start_idx + 500, len(pdf_text))

    snippet = pdf_text[context_start_idx:context_end_idx]
    span = [context_start_idx, context_end_idx]

    return snippet.strip(), span


# Function to generate questions and answers using OpenAI
def generate_questions_and_answers(pdf_text):
    prompt = (
        "Dựa trên nội dung tài liệu pháp lý dưới đây, tạo ra 5 câu hỏi và câu trả lời không được thiếu phải 5. "
        "Mỗi câu trả lời PHẢI kèm tham chiếu CHÍNH XÁC đến Điều/Khoản trong văn bản (VD: 'Điều 1, Khoản 2'). "
        "Output chỉ là JSON hợp lệ theo định dạng:\n\n"
        "[{\"user_input\": \"...\", \"response\": \"...\", \"reference\": \"Điều X, Khoản Y\"}]\n\n"
        f"Tài liệu:\n\n{pdf_text}"
    )

    response = generate_response(prompt)

    # Clean up the response
    cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', ' ').replace('\r', '')

    # Try parsing the cleaned-up response
    try:
        formatted_response = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"Lỗi: Phản hồi không phải là định dạng JSON hợp lệ. Lỗi: {e}")
        print(f"Raw Response that failed parsing: {repr(cleaned_response)}")
        formatted_response = []

    return formatted_response


# Function to generate a response using OpenAI
def generate_response(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key here
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


# Function to generate a response from the PDF
def generate_response_from_pdf(query, pdf_text):
    # Create a prompt that will query the content and provide the reference in Vietnamese
    prompt = f"Dựa trên nội dung tài liệu pháp lý dưới đây:\n\n{pdf_text}\n\nTrả lời câu hỏi sau:\n{query}\nTrả lời (bằng tiếng Việt):"
    response = generate_response(prompt)

    # Extract reference from the PDF
    reference = extract_reference_from_pdf(query, pdf_text)

    return response, reference


# Function to extract a reference from the PDF
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