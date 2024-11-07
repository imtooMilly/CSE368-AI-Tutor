# backend/question_generation.py

import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv
load_dotenv()

#Run pip install python-dotenv
#Add a .env file and put your api key in the .env file --> format == api_key = "api_key"
#Include .env in gitignore
api_key = os.getenv("api_key")
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
    # Set up prompt based on input text
    prompt_text = f"Generate {num_questions} educational questions based on the following content:\n\n{text}"

    headers = {
        "Content-Type": "application/json",
    }

    # Payload structure based on the Gemini API requirements
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extracting the generated questions from the response
        questions = []
        for candidate in result.get("candidates", []):
            question_text = candidate.get("output", {}).get("text", "").strip()
            if question_text:
                questions.append(question_text)

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
    # Use extract_text to get text content from the file
    extracted_text = extract_text(file_path)

    if extracted_text:
        questions = generate_questions(
            extracted_text, num_questions=num_questions)
        return questions
    else:
        print("No text extracted from the file.")
        return []


# Example usage
if __name__ == "__main__":
    # Update with the path to your test file
    file_path = r"C:\Users\oluwa\OneDrive - University at Buffalo\CSE 368\Project\CSE368-AI-Tutor\backend\tests\pdf\Georgia Tech Essays.pdf"
    questions = generate_questions_from_file(file_path, num_questions=5)
    print("Generated Questions:")
    for question in questions:
        print("-", question)
