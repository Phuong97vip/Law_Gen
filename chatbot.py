import openai
from config import OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def generate_response_from_pdf(query, pdf_text):
    # Create a prompt that will query the content and provide the reference
    prompt = f"Based on the following legal document content:\n\n{pdf_text}\n\nAnswer the following question:\n{query}\nAnswer (in Vietnamese):"
    response = generate_response(prompt)
    
    # Extract reference from the PDF
    reference = extract_reference_from_pdf(query, pdf_text)
    
    return response, reference

def extract_reference_from_pdf(query, pdf_text):
    # In a real scenario, this function could be improved to pinpoint exact references from the document.
    # For now, we just return a generic string indicating the reference.
    return f"Reference from the PDF: {pdf_text[:300]}..."  # Example to return part of the text
