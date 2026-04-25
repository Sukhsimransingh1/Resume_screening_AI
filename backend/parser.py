import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    
    for page in doc:
        text += page.get_text()
    
    return text

from docx import Document

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    
    for para in doc.paragraphs:
        text.append(para.text)
    
    return "\n".join(text)

import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    
    else:
        raise ValueError("Unsupported file format")