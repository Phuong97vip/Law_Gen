from flask import Flask, request, jsonify
from chatbot import generate_response_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1

app = Flask(__name__)

# Extract text from the PDF file
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)

@app.route('/chat', methods=['POST'])
def chat():
    print("Chat request received with query: ", request.data)  # Log the request data
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Generate the response from the PDF
    response, reference = generate_response_from_pdf(query, pdf_text_1)
    
    print("Generated response: ", response)  # Log the generated response
    return jsonify({
        'response': response,
        'reference': reference
    })

if __name__ == '__main__':
    # Run Flask app on fixed port (e.g., 5001)
    app.run(debug=True, port=5001)
