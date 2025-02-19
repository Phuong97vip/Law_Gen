from flask import Flask, request, jsonify  # Make sure to import 'request'
from chatbot import generate_questions_and_answers, generate_response_from_pdf, extract_snippet_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1
from config import PDF_FILE_PATH_2

app = Flask(__name__)

# Extract text from the PDF file
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)
pdf_text_2 = extract_text_from_pdf(PDF_FILE_PATH_2)


@app.route('/generate_test_answers', methods=['GET'])
def generate_test_answers():
    try:
        # Generate questions and answers from the second PDF
        questions_and_answers = generate_questions_and_answers(pdf_text_2)

        # Ensure there are at least 100 questions and answers
      

        # Format the questions and answers into the desired test format
        test_data = []

        for qa in questions_and_answers[:100]:  # Limit to 100 questions
            query = qa['user_input']
            answer = qa['response']

            # Extract snippet and span for the answer in the PDF
            snippet, span = extract_snippet_from_pdf(query, pdf_text_2)

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
