import os
import requests
from text_extraction import extract_text  # Import the text extraction function
from dotenv import load_dotenv
import random
import re

# Load environment variables
load_dotenv()
api_key = os.getenv(
    "GOOGLE_API_KEY") or "AIzaSyCsAaseIdwZssVYs47IC0pFXKHzhus3tmQ"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

def generate_mcq_for_questions(questions, text):
    """
    Generate multiple-choice answers for given questions.

    Args:
        questions (list): List of dictionaries with 'question' and 'answer'.
        text (str): Original context text.

    Returns:
        List[dict]: Multiple-choice questions with choices, correct answer, and explanations.
    """
    print(f"Generating MCQs for Questions: {questions}")

    if not questions:
        print("No valid questions to generate MCQs.")
        return []

    # Prepare prompt for generating MCQ options
    prompt_text = f"For the following questions based on the text, generate multiple-choice answers:\n\n"
    prompt_text += "Context Text:\n" + text + "\n\n"
    prompt_text += "Questions:\n"
    for q in questions:
        prompt_text += f"{q['question']}\n"

    prompt_text += "\nFor each question, provide:\n"
    prompt_text += "1. 4 answer choices (A, B, C, D)\n"
    prompt_text += "2. The correct answer (e.g., A, B, C, or D)\n"
    prompt_text += "3. A brief explanation for the answer."

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extract the full response text
        full_response = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Full API Response for MCQs:\n{full_response}")

        # Parse the response
        mcqs = []
        question_blocks = re.split(r'\n\n', full_response.strip())
        for block in question_blocks:
            question_match = re.search(r'\*\*(.*?)\*\*', block)  # Extract question
            choices_match = re.findall(r'([a-d]\))\s(.*?)\n', block)  # Extract choices
            correct_match = re.search(r'\*\*Answer:\*\*\s(.*?)\n', block)  # Correct Answer
            explanation_match = re.search(r'\*\*Explanation:\*\*\s(.*?)$', block, re.DOTALL)  # Explanation

            if question_match and choices_match and correct_match and explanation_match:
                question = question_match.group(1).strip()
                choices = [f"{choice[0]} {choice[1].strip()}" for choice in choices_match]
                correct_answer = correct_match.group(1).strip()
                explanation = explanation_match.group(1).strip()

                mcqs.append({
                    "question": question,
                    "choices": choices,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })

        return mcqs

    except requests.exceptions.RequestException as e:
        print(f"Error generating MCQs with Google Gemini API: {e}")
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
        # Generate open-ended questions with answers
        questions = generate_questions(extracted_text, num_questions=num_questions)

        # Generate MCQs using the questions
        mcqs = generate_mcq_for_questions(questions, extracted_text)

        return {
            'questions': questions,  # List of dicts with 'question' and 'answer'
            'mcqs': mcqs  # List of dicts with MCQ details
        }
    else:
        print("No text extracted from the file.")
        return {'questions': [], 'mcqs': []}

def generate_questions(text, num_questions=5):
    """
    Generate contextually relevant questions **with answers** using Google Gemini API.

    Args:
        text (str): The extracted text to generate questions from.
        num_questions (int): Number of questions to generate.

    Returns:
        List[dict]: A list of dictionaries with 'question' and 'answer'.
    """
    # Updated prompt to include answers
    prompt_text = f"Generate {num_questions} educational questions based on the following content. " \
                  f"For each question, also provide a concise and accurate answer.\n\n{text}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Parse the response into questions and answers
        questions_text = result['candidates'][0]['content']['parts'][0]['text']
        questions_and_answers = []

        # Use regex to find Question and Answer pairs
        qa_pairs = re.split(r'\*\*Question.*?:\*\*', questions_text)
        for pair in qa_pairs[1:]:  # Ignore the first empty split
            question_match = re.search(r'(.*?)\n', pair, re.DOTALL)
            answer_match = re.search(r'\*\*Answer:.*?\*\* (.*?)\n', pair, re.DOTALL)

            if question_match and answer_match:
                question = question_match.group(1).strip()
                answer = answer_match.group(1).strip()
                questions_and_answers.append({"question": question, "answer": answer})

        return questions_and_answers[:num_questions]  # Return only the desired number
    except requests.exceptions.RequestException as e:
        print(f"Error generating questions with Google Gemini API: {e}")
        return []