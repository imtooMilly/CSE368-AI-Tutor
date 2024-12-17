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
    if not questions:
        print("No valid questions to generate MCQs.")
        return []

    # Prepare the prompt for the API
    prompt_text = (
        f"Based on the following context, generate multiple-choice questions with correct answers and explanations:\n\n"
        f"Context Text:\n{text}\n\nQuestions:\n"
    )
    for q in questions:
        prompt_text += f"{q['question']}\n"

    prompt_text += (
        "\nFormat the response like this:\n"
        "**Question:** [The question here]\n"
        "A) Choice 1\n"
        "B) Choice 2\n"
        "C) Choice 3\n"
        "D) Choice 4\n"
        "**Correct Answer:** [Correct choice letter]\n"
        "**Explanation:** [Brief explanation]."
    )

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"role": "user", "parts": [{"text": prompt_text}]}]}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extract the API response text
        full_response = result['candidates'][0]['content']['parts'][0]['text']
        print("Full API Response:\n", full_response)

        mcqs = []
        question_blocks = re.split(r'\n(?=\*\*Question:)', full_response.strip())

        # Parse each question block
        for block in question_blocks:
            question_match = re.search(r'\*\*Question:\*\*\s*(.*?)\n', block)
            choices_match = re.findall(r'([A-D])\)\s(.*?)\n', block)
            correct_answer_match = re.search(r'\*\*Correct Answer:\*\*\s*([A-D])', block)
            explanation_match = re.search(r'\*\*Explanation:\*\*\s*(.*?)$', block, re.DOTALL)

            if question_match and choices_match and correct_answer_match and explanation_match:
                mcqs.append({
                    "question": question_match.group(1).strip(),
                    "choices": [f"{choice[0]}) {choice[1].strip()}" for choice in choices_match],
                    "correct_answer": correct_answer_match.group(1).strip(),
                    "explanation": explanation_match.group(1).strip()
                })

        # Check if MCQs were parsed successfully
        if not mcqs:
            print("No valid MCQs parsed. Adding fallback MCQs.")
            for q in questions:
                mcqs.append({
                    "question": q['question'],
                    "choices": [
                        "A) Placeholder Option 1",
                        "B) Placeholder Option 2",
                        "C) Placeholder Option 3",
                        "D) Placeholder Option 4"
                    ],
                    "correct_answer": "A",
                    "explanation": "The answer explanation is unavailable."
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
    prompt_text = (
        f"Generate {num_questions} educational questions based on the following content. "
        f"For each question, also provide a concise and accurate answer.\n\n{text}"
    )

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

        # Extract and parse the response
        questions_text = result['candidates'][0]['content']['parts'][0]['text']
        questions_and_answers = []

        # Use regex to split and extract Question/Answer pairs
        qa_pairs = re.split(r'\*\*Question.*?:\*\*', questions_text)
        for pair in qa_pairs[1:]:  # Skip the first split
            question_match = re.search(r'(.*?)\n', pair, re.DOTALL)
            answer_match = re.search(r'\*\*Answer:.*?\*\* (.*?)\n', pair, re.DOTALL)

            if question_match and answer_match:
                question = question_match.group(1).strip()
                answer = answer_match.group(1).strip()
                questions_and_answers.append({"question": question, "answer": answer})

        return questions_and_answers[:num_questions]  # Return the required number of questions
    except requests.exceptions.RequestException as e:
        print(f"Error generating questions with Google Gemini API: {e}")
        return []