# backend/quiz_generation_with_interactivity.py

import os
import requests
from dotenv import load_dotenv  # Import dotenv to load environment variables
import pytesseract
from PIL import Image
import fitz
import os
from docx import Document

# Load environment variables from .env file
load_dotenv()

# API Key and Endpoint
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_API_KEY in the .env file."
    )

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

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


def generate_quiz_with_preferences(text, num_questions=5, question_type="multiple-choice", difficulty="medium"):
    """
    Generate a quiz based on user-selected preferences.

    Args:
        text (str): The extracted text to generate quiz questions from.
        num_questions (int): Number of questions to generate.
        question_type (str): Type of questions (e.g., "multiple-choice", "true/false").
        difficulty (str): Difficulty level of the questions ("easy", "medium", "hard").

    Returns:
        List[Dict]: A list of quiz questions with options and answers.
    """
    prompt_text = (
        f"Generate {num_questions} {question_type} quiz questions based on the following content. "
        f"Ensure all questions are of '{difficulty}' difficulty. For multiple-choice, include 4 options for each question "
        f"and indicate the correct answer:\n\n{text}"
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Parse the response for quiz questions
        quiz_content = result['candidates'][0]['content']['parts'][0]['text']
        quiz_items = [
            item.strip() for item in quiz_content.split("\n\n") if item.strip()
        ]

        quizzes = []
        for item in quiz_items:
            if "Q:" in item and "Answer:" in item:
                question = item.split("\n")
                question_text = question[0].split("Q: ")[1].strip()
                options = [opt.split(") ")[1].strip()
                           for opt in question[1:5] if ") " in opt]
                correct_answer = question[-1].split("Answer: ")[1].strip()
                quizzes.append({
                    "question": question_text,
                    "options": options,
                    "answer": correct_answer,
                })

        return quizzes[:num_questions]
    except requests.exceptions.RequestException as e:
        print(f"Error generating quiz with Google Gemini API: {e}")
        return []


def conversational_agent(query, context):
    """
    Simulates a conversational agent to allow users to ask clarifying questions.

    Args:
        query (str): The question or query from the user.
        context (str): The lecture content or quiz context to refer to.

    Returns:
        str: AI-generated response to the query.
    """
    prompt_text = (
        f"You are a tutor. Answer the following question based on the given context:\n\n"
        f"Context: {context}\n\n"
        f"Question: {query}\n\n"
        f"Provide a detailed and accurate response."
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        return result['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error querying the conversational agent: {e}")
        return "Unable to process the query. Please try again."
    
def extract_text(file_path):
    """
    Determine if the file is an image, PDF, or DOCX, then extract text accordingly.
    Supports .jpg, .jpeg, .png, .pdf, and .docx file formats.
    """
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        return extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        print("Unsupported file type. Please use a .jpg, .jpeg, .png, .pdf, or .docx file.")
        return None


def interactive_quiz(file_path, num_questions=5, question_type="multiple-choice", difficulty="medium"):
    """
    Extract text, generate a quiz, and allow interaction with a conversational agent.

    Args:
        file_path (str): Path to the input file (DOCX, PDF, or image).
        num_questions (int): Number of questions to generate.
        question_type (str): Type of questions (e.g., "multiple-choice", "true/false").
        difficulty (str): Difficulty level of the questions ("easy", "medium", "hard").

    Returns:
        None: Interactively prints quiz and allows follow-up queries.
    """
    extracted_text = extract_text(file_path)
    if extracted_text:
        quiz = generate_quiz_with_preferences(
            extracted_text, num_questions=num_questions, question_type=question_type, difficulty=difficulty
        )
        print("Generated Quiz:")
        for idx, item in enumerate(quiz, start=1):
            print(f"Q{idx}: {item['question']}")
            for opt_idx, option in enumerate(item['options'], start=1):
                print(f"  {chr(64+opt_idx)}) {option}")
            print(f"Answer: {item['answer']}\n")

        while True:
            user_query = input("Ask the tutor a question about the content (or type 'exit' to quit): ")
            if user_query.lower() == "exit":
                break
            response = conversational_agent(user_query, extracted_text)
            return response
            print(f"Tutor: {response}")
    else:
        print("No text extracted from the file.")
        response = "No text extracted from the file."


if __name__ == "__main__":
    file_path = r"/Users/aaronessien/Documents/368/CSE368-AI-Tutor/server/pdf/Chapter2Notes.pdf"
    interactive_quiz(file_path, num_questions=5, question_type="multiple-choice", difficulty="medium")
