import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_FILE_PATH_1 = "knowledge/45_2019_QH14_333670.doc.pdf"
PDF_FILE_PATH_2 = "knowledge/59_2020_QH14_427301.doc.pdf"
