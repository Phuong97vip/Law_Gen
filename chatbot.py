import openai
from config import OPENAI_API_KEY

# Sử dụng API key từ file cấu hình
openai.api_key = OPENAI_API_KEY
print("OpenAI API key:", openai.api_key)

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Thay vì "gpt-4", sử dụng "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def generate_response_from_pdf(query, pdf_text):
    prompt = f"Based on the following document content:\n\n{pdf_text}\n\nAnswer the following question:\n{query}\nAnswer:"
    return generate_response(prompt)
