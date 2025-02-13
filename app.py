from flask import Flask, request, jsonify  # Make sure to import 'request'
from chatbot import generate_questions_and_answers
from chatbot import generate_response_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1

app = Flask(__name__)

# Extract text from the PDF file
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)
pdf_text_2 = extract_text_from_pdf(PDF_FILE_PATH_2)

@app.route('/chat', methods=['POST'])
def chat():
    # Access the incoming JSON data
    data = request.get_json()  # Use 'request.get_json()' to parse the incoming data
    
    query = data.get('query')  # Retrieve the query from the incoming data
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400  # Return an error if 'query' is not provided

    # Generate the response from the PDF
    response, reference = generate_response_from_pdf(query, pdf_text_1)
    
    return jsonify({
        'response': response,
        'reference': reference
    })

@app.route('/generate_answers', methods=['GET'])
def generate_answers():
    try:
        questions_and_answers = generate_questions_and_answers(pdf_text_2)
        
        # Check if the result is valid
        if not questions_and_answers:
            return jsonify({'error': 'Failed to generate questions and answers'}), 500
        
        # Return the generated questions and answers as JSON
        return jsonify(questions_and_answers)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run Flask app on fixed port (e.g., 5001)
    app.run(debug=True, port=5001)
