# backend/question_generation.py

import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv

# Replace 'YOUR_API_KEY' with your actual API key
#Run pip install python-dotenv
#Add a .env file and put your api key in the .env file --> format == api_key = "api_key"
#Include .env in gitignore
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
    # Adjusted prompt to encourage generating separate questions without explanations
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

        # Extract questions from the correct field in the response
        questions_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Split the response text by double line breaks or numbers (1., 2., etc.) to isolate individual questions
        questions = [q.strip() for q in questions_text.split("\n\n") if q.strip() and not q.startswith("This")]

        # Return only the requested number of questions
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
