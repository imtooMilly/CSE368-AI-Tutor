# backend/question_generation.py

import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("api_key")

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
    # Update with the path to your test file
    file_path = r"/Users/aaronessien/Documents/368/CSE368-AI-Tutor/backend/tests/pdf/Georgia Tech Essays.pdf"
    questions = generate_questions_from_file(file_path, num_questions=5)
    print("Generated Questions:")
    for question in questions:
        print("-", question)
