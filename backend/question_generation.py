import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()
api_key = os.getenv(
    "GOOGLE_API_KEY") or "AIzaSyCsAaseIdwZssVYs47IC0pFXKHzhus3tmQ"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

def generate_mcq_for_questions(questions, text):
    """
    Generate multiple-choice answers for given questions.

    Args:
        questions (list): List of questions to generate MCQ for.
        text (str): Original context text.

    Returns:
        List[dict]: Multiple-choice questions with choices and correct answer.
    """
    # Prepare prompt for generating MCQ options
    prompt_text = f"For the following questions based on the text, generate multiple-choice answers:\n\n"
    prompt_text += "Context Text:\n" + text + "\n\n"
    prompt_text += "Questions:\n"
    for q in questions:
        prompt_text += q + "\n"
    
    prompt_text += "\nFor each question, provide:\n"
    prompt_text += "1. 4 answer choices (A, B, C, D)\n"
    prompt_text += "2. The correct answer\n"
    prompt_text += "3. A brief explanation"

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

        # Extract the full response text
        full_response = result['candidates'][0]['content']['parts'][0]['text']
        
        # Parse the response
        mcqs = []
        current_mcq = {}
        lines = full_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detect start of a new MCQ
            if line.startswith('Q:'):
                # If there's a previous MCQ, add it to the list
                if current_mcq:
                    mcqs.append(current_mcq)
                # Start a new MCQ
                current_mcq = {'question': line[2:].strip()}
            
            # Collect choices
            if line.startswith('Choices:'):
                choices = line[len('Choices:'):].strip().split('|')
                current_mcq['choices'] = [c.strip() for c in choices]
            
            # Collect correct answer
            if line.startswith('Correct Answer:'):
                current_mcq['correct_answer'] = line[len('Correct Answer:'):].strip()
            
            # Collect explanation
            if line.startswith('Explanation:'):
                current_mcq['explanation'] = line[len('Explanation:'):].strip()
        
        # Add the last MCQ
        if current_mcq:
            mcqs.append(current_mcq)
        
        return mcqs
    
    except requests.exceptions.RequestException as e:
        print(f"Error generating MCQ with Google Gemini API: {e}")
        return []

def generate_questions_from_file(file_path, num_questions=5):
    """
    Extract text from a file, then generate questions and MCQs using Google Gemini API.

    Args:
        file_path (str): Path to the input file (DOCX, PDF, or image).
        num_questions (int): Number of questions to generate.

    Returns:
        dict: A dictionary containing open-ended questions and MCQs.
    """
    # Use extract_text to get text content from the file
    extracted_text = extract_text(file_path)

    if extracted_text:
        # Generate open-ended questions
        questions = generate_questions(
            extracted_text, num_questions=num_questions)

        # Generate MCQs for the questions
        mcqs = generate_mcq_for_questions(questions, extracted_text)

        return {
            'questions': questions,  # Open-ended questions
            'mcqs': mcqs  # Multiple-choice questions
        }
    else:
        print("No text extracted from the file.")
        return {'questions': [], 'mcqs': []}

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