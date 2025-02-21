from flask import Flask, request, jsonify
from chatbot import generate_questions_and_answers, generate_response_from_pdf,extract_snippet_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1, PDF_FILE_PATH_2
from pdf_utils import extract_text_from_pdf

# Initialize Flask app
app = Flask(__name__)

# Extract text from the PDF files
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)
pdf_text_2 = extract_text_from_pdf(PDF_FILE_PATH_2)


# Endpoint to generate test answers
@app.route('/generate_test_answers', methods=['GET'])
def generate_test_answers():
    try:
        # Generate questions and answers from the second PDF
        questions_and_answers = generate_questions_and_answers(pdf_text_2)

        # Format the questions and answers into the desired test format
        test_data = []

        for qa in questions_and_answers[:100]:  # Limit to 100 questions
            query = qa['user_input']
            reference = qa.get('reference', '')

            # Skip if no reference is provided
            if not reference:
                continue

            # Extract snippet and span for the answer in the PDF based on the reference
            snippet, span = extract_snippet_from_pdf(reference, pdf_text_2)

            # Skip cases with no relevant snippet
            if snippet is None:
                continue

            # Prepare the formatted test case
            test_case = {
                "query": query,
                "snippets": [
                    {
                        "file_path": "knowledge/59_2020_QH14_427301.doc.pdf",  # Example file path
                        "span": span,
                        "answer": snippet
                    }
                ]
            }

            test_data.append(test_case)

        return jsonify(test_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to handle chat queries
@app.route('/chat', methods=['POST'])
def chat():
    # Access the incoming JSON data
    data = request.get_json()

    query = data.get('query')  # Retrieve the query from the incoming data

    if not query:
        return jsonify({'error': 'No query provided'}), 400  # Return an error if 'query' is not provided

    # Generate the response from the PDF
    response, reference = generate_response_from_pdf(query, pdf_text_1)

    return jsonify({
        'response': response,
        'reference': reference
    })


# Endpoint to generate raw questions and answers
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


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)