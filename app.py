from flask import Flask, request, jsonify
from chatbot import generate_response_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1, PDF_FILE_PATH_2

app = Flask(__name__)

# Trích xuất văn bản từ cả hai file PDF khi khởi động ứng dụng
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)
pdf_text_2 = extract_text_from_pdf(PDF_FILE_PATH_2)

# Kết hợp nội dung của cả hai file PDF
combined_pdf_text = pdf_text_1 + "\n\n" + pdf_text_2

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Sinh phản hồi dựa trên kiến thức từ cả hai PDF
    response = generate_response_from_pdf(query, combined_pdf_text)
    return jsonify({'response': response})

if __name__ == '__main__':
    # Chạy Flask app trên port cố định (ví dụ: 5001)
    app.run(debug=True, port=5001)
