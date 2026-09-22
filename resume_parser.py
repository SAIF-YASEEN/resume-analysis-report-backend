import io

import pymupdf
from docx import Document


def extract_text_from_pdf(file_bytes):

    text = ""

    document = pymupdf.open(stream=file_bytes, filetype="pdf")

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_docx(file_bytes):

    document = Document(io.BytesIO(file_bytes))

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text(file_bytes, filename):

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    raise ValueError("Only PDF and DOCX files are supported")


def analyze_resume(file_bytes, filename):

    text = extract_text(file_bytes, filename)

    if not text.strip():
        raise ValueError("Could not extract any text from the resume")

    return text
