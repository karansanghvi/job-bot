import os
import re
import fitz  # PyMuPDF
from pyresparser import ResumeParser

# ✅ Extract text from PDF or TXT
def extract_text_from_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        with fitz.open(file_path) as doc:
            return "\n".join([page.get_text() for page in doc])
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

# ✅ Extract email from raw text using regex (fallback)
def extract_email_from_text(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else "N/A"

# ✅ Parse and return resume components
def parse_resume(file_path):
    try:
        text = extract_text_from_resume(file_path)
        data = ResumeParser(file_path).get_extracted_data()
        email = data.get('email') or extract_email_from_text(text)
        return {
            'text': text,
            'skills': set(map(str.lower, data.get('skills', []))),
            'email': email
        }
    except Exception as e:
        # Fallback in case pyresparser fails
        text = extract_text_from_resume(file_path)
        email = extract_email_from_text(text)
        return {
            'text': text,
            'skills': set(),
            'email': email
        }
