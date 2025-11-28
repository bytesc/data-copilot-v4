import io
import docx
import PyPDF2
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

def extract_text_from_txt(file_content: bytes) -> str:
    return file_content.decode('utf-8')


def extract_text_from_docx(file_content: bytes) -> str:
    file_stream = io.BytesIO(file_content)
    doc = docx.Document(file_stream)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)


def extract_text_from_pdf(file_content: bytes) -> str:
    file_stream = io.BytesIO(file_content)
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = []
    for page in pdf_reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)


def extract_text_from_doc(file_content: bytes) -> str:
    try:
        return file_content.decode('utf-8', errors='ignore')
    except:
        raise HTTPException(status_code=400, detail="DOC file processing requires additional libraries")


def process_file_content(file_content: bytes, file_extension: str) -> str:
    file_extension = file_extension.lower()
    if file_extension == '.txt':
        return extract_text_from_txt(file_content)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_content)
    elif file_extension == '.doc':
        return extract_text_from_doc(file_content)
    elif file_extension == '.pdf':
        return extract_text_from_pdf(file_content)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")