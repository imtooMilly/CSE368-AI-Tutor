# backend/question_generation.py

import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# API Key and Endpoint
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_API_KEY in the .env file.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"


def generate_questions(text, num_questions=5):
    """
    Generate contextually relevant questions using Google Gemini API.

    Args:
        text (str): The extracted text to generate questions from.
        num_questions (int): Number of questions to generate.

    Returns:
        List[str]: A list of generated questions.
    """
    prompt_text = f"Generate {num_questions} educational questions based on the following content without any explanations or additional context after each question:\n\n{text}"
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

        questions_text = result['candidates'][0]['content']['parts'][0]['text']
        questions = [q.strip() for q in questions_text.split(
            "\n\n") if q.strip() and not q.startswith("This")]

        return questions[:num_questions]
    except requests.exceptions.RequestException as e:
        print(f"Error generating questions with Google Gemini API: {e}")
        return []


def generate_questions_from_file(file_path, num_questions=5):
    """
    Extract text from a file, then generate questions using Google Gemini API.

    Args:
        file_path (str): Path to the input file (DOCX, PDF, or image).
        num_questions (int): Number of questions to generate.

    Returns:
        List[str]: Generated questions based on the extracted content.
    """
    extracted_text = extract_text(file_path)
    if extracted_text:
        questions = generate_questions(
            extracted_text, num_questions=num_questions)
        return questions
    else:
        print("No text extracted from the file.")
        return []


if __name__ == "__main__":
    file_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\pdf\7-CSE305.pdf"
    questions = generate_questions_from_file(file_path, num_questions=5)
    print("Generated Questions:")
    for question in questions:
        print("-", question)
