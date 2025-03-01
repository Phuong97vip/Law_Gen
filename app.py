# app.py
import json
from chatbot import generate_questions_and_answers, extract_snippet_from_pdf,generate_response_from_openai
from pdf_utils import extract_text_from_pdf
from config import PDF_FILE_PATH_1, PDF_FILE_PATH_2
import pandas as pd

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

def process_customer_data(input_excel_path, output_excel_path):
    # Read customer data from Excel
    try:
        df = pd.read_excel(input_excel_path, engine='openpyxl')  # Ensure using the right engine for reading Excel
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Initialize a list to store results
    results = []

    # Process each customer in the list
    for index, row in df.iterrows():
        company_name = row['Công ty']

        # Generate Prompt 1 (Detailed)
        prompt1 = f"Từ tháng 8/2024 đến hết tháng 1/2025 có số dư CASA, có những sự kiện gì với công ty này, {company_name}"
        response1 = generate_response_from_openai(prompt1)

        # Generate Prompt 2 (Summary)
        prompt2 = f"Tóm tắt nội dung trên: {response1}"
        response2 = generate_response_from_openai(prompt2)

        # Generate Prompt 3 (Sentiment Analysis)
        prompt3 = f"Phân tích ý nghĩa tích cực hay tiêu cực của nội dung sau: {response1}"
        response3 = generate_response_from_openai(prompt3)

        # Add the results to the list
        results.append({
            'Công ty': company_name,
            'Prompt1': response1,
            'Prompt2': response2,
            'Prompt3': response3
        })

    # Convert results to a DataFrame and save to Excel
    try:
        results_df = pd.DataFrame(results)
        results_df.to_excel(output_excel_path, index=False, engine='openpyxl')
        print(f"Results saved to {output_excel_path}")
    except Exception as e:
        print(f"Error writing to Excel file: {e}")

if __name__ == '__main__':
    # Automatically run the functions on startup
    generate_test_answers()
    generate_answers()
    # input_excel = 'customer_list.xlsx'  # Input Excel file containing customer data
    # output_excel = 'customer_results.xlsx'  # Output Excel file for saving the results
    # process_customer_data(input_excel, output_excel)
