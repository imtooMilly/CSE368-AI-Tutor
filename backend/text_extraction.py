import pytesseract
from PIL import Image
import fitz
import os
from text_summarization import summarize_text_local
from docx import Document

# Path to the Tesseract executable, adjust if necessary
# Update based on your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path):
    """Extract text from a single image file using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    try:
        # Open the PDF file
        with fitz.open(pdf_path) as pdf:
            # Iterate over each page
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text += f"\n\n--- Page {page_num + 1} ---\n\n"
                text += page.get_text("text")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def extract_text_from_docx(docx_path):
    """Extract text from a .docx file using python-docx."""
    try:
        doc = Document(docx_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None


def extract_and_summarize_text(file_path):
    """
    Extract text from a file and summarize it.
    Supports .jpg, .jpeg, .png, .pdf, and .docx file formats.
    """
    # Determine file type and extract text accordingly
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_text = extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        extracted_text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file type. Please use a .jpg, .jpeg, .png, .pdf, or .docx file.")
        return None

    # If text was extracted, summarize it
    if extracted_text:
        # Summarize the extracted text
        summary = summarize_text_local(extracted_text)
        return summary
    else:
        print("No text extracted.")
        return None


# # Example usage
# if __name__ == "__main__":
#     # Replace 'sample_image.jpg', 'sample_document.pdf', and 'sample_document.docx' with actual file paths for testing
#     image_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\images\sample_png.png"
#     pdf_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\pdf\EthicsAssignment (1).pdf"
#     docx_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\docx\368 project proposal.docx"

#     print("Text extracted from image:")
#     print(extract_text(image_path))

#     print("\nText extracted from PDF:")
#     print(extract_text(pdf_path))

#     print("\nText extracted from DOCX:")
#     print(extract_text(docx_path))
# Example usage
if __name__ == "__main__":
    # Replace with the path to your file
    file_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\docx\368 project proposal.docx"
    summary = extract_and_summarize_text(file_path)
    print("Final Summary:\n", summary)