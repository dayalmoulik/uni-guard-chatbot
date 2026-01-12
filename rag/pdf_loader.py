"""
PDF Text Extraction Utility
"""

from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def save_as_markdown(text: str, output_path: str):
    Path(output_path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    pdf_path = "data/raw/Admission_booklet.pdf"
    output_md = "data/admission_booklet.md"

    text = extract_text_from_pdf(pdf_path)
    save_as_markdown(text, output_md)

    print("✅ PDF converted to Markdown")
