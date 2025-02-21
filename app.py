import json
from chatbot import generate_questions_and_answers, extract_snippet_from_pdf
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1, PDF_FILE_PATH_2

# Extract text from the PDF files
pdf_text_1 = extract_text_from_pdf(PDF_FILE_PATH_1)
pdf_text_2 = extract_text_from_pdf(PDF_FILE_PATH_2)

def generate_test_answers():
    try:
        questions_and_answers = generate_questions_and_answers(pdf_text_2)
        print("Generated Questions and Answers:", questions_and_answers)
        test_data = []

        for qa in questions_and_answers[:5]:  # Limit to 5 questions
            query = qa['user_input']
            reference = qa.get('reference', '')

            if not reference:
                print(f"Skipping question due to missing reference: {query}")
                continue

            snippet, span = extract_snippet_from_pdf(reference, pdf_text_2)

            if snippet is None:
                print(f"Skipping question due to missing snippet: {query}")
                continue

            test_case = {
                "query": query,
                "snippets": [
                    {
                        "file_path": "knowledge/59_2020_QH14_427301.doc.pdf",
                        "span": span,
                        "answer": snippet
                    }
                ]
            }

            test_data.append(test_case)

        # Save to file
        with open('generate_test_answers.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(test_data, ensure_ascii=False, indent=4))

        print("Test answers generated and saved to generate_test_answers.txt")

    except Exception as e:
        print(f"Error generating test answers: {e}")

def generate_answers():
    try:
        questions_and_answers = generate_questions_and_answers(pdf_text_2)

        if not questions_and_answers:
            raise Exception('Failed to generate questions and answers')

        # Save to file
        with open('generate_answers.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(questions_and_answers[:5], ensure_ascii=False, indent=4))  # Limit to 5 questions

        print("Answers generated and saved to generate_answers.txt")

    except Exception as e:
        print(f"Error generating answers: {e}")

if __name__ == '__main__':
    # Automatically run the functions on startup
    generate_test_answers()
    generate_answers()
