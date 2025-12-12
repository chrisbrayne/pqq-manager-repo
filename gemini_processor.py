# gemini_processor.py
# This script handles text extraction from PDF and DOCX files,
# and all interactions with the Gemini API.

import os
import sys
import json
import pypdf
import docx # Added for .docx support
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- IMPORTANT: API Key Configuration ---
# The script expects your Gemini API key to be stored in an environment variable
# named "PQQ_API_KEY".
try:
    genai.configure(api_key=os.environ["PQQ_API_KEY"])
except KeyError:
    print("ERROR: The 'PQQ_API_KEY' environment variable is not set.")
    sys.exit(1)

# Initialize the generative model
model = genai.GenerativeModel('gemini-2.5-flash')
# Set a longer timeout for potentially complex requests
request_options = {"timeout": 120}

def extract_text_from_file(file_path):
    """Extracts raw text from a given PDF or DOCX file."""
    try:
        if file_path.lower().endswith('.pdf'):
            reader = pypdf.PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        elif file_path.lower().endswith('.docx'):
            document = docx.Document(file_path)
            text = "\n".join([para.text for para in document.paragraphs])
            return text
        else:
            print(f"Error: Unsupported file type for {file_path}. Only .pdf and .docx are supported.")
            return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def extract_questions_from_text(text):
    """Uses Gemini to find and list all questions in a block of text."""
    prompt = f"""
    Analyze the following text and extract all numbered or bulleted questions.
    Return the questions as a JSON array of strings. Do not return anything else.
    Example output: ["What is your name?", "What is your quest?"]

    Text to analyze:
    ---
    {text}
    ---
    """
    try:
        response = model.generate_content(prompt, request_options=request_options)
        json_response = response.text.strip().replace("`", "").replace("json", "")
        return json.loads(json_response)
    except Exception as e:
        print(f"Error calling Gemini API for question extraction: {e}")
        return []

def find_evidence_for_batch(questions, evidence_texts):
    """Uses Gemini to find the best evidence for a batch of questions."""
    # questions is a list of strings
    # evidence_texts is a single string containing all evidence
    prompt = f"""
    You are an expert assistant for filling out Pre-Qualification Questionnaires.
    Your task is to find the best answer for EACH question in the provided JSON list, using the evidence library.

    ## INSTRUCTIONS
    1.  Read the list of questions.
    2.  For each question, find the single most relevant snippet from the evidence library.
    3.  If no snippet provides a good answer for a question, use the value: "!!-- NO MATCH FOUND. PLEASE ANSWER MANUALLY --!!".
    Return a single JSON object where each key is the original question. The value for each question should be an object containing two keys: "answer" (the matched evidence snippet text, or the manual review message if no match) and "sources" (a JSON array of the filenames of the evidence documents used to formulate the answer).

    ## JSON Question List
    {json.dumps(questions, indent=2)}

    ## Evidence Library
    Each piece of evidence is prefixed with '--- Evidence File: [filename] ---'. When using evidence, extract the filename(s) from these markers.
    ---
    {evidence_texts}
    ---

    ## REQUIRED OUTPUT FORMAT
    Return ONLY a single valid JSON object. Do not include any other text or formatting.
    Example output structure:
    {{
        "What is the company's annual turnover?": {{
            "answer": "The company's annual turnover is £1,234,567.",
            "sources": ["financial_accounts.md", "financial_turnover.md"]
        }},
        "Do you have a health and safety policy?": {{
            "answer": "Yes, we have a comprehensive health and safety policy.",
            "sources": ["health_and_safety_policy.md"]
        }},
        "What is your policy on modern slavery?": {{
            "answer": "!!-- NO MATCH FOUND. PLEASE ANSWER MANUALLY --!!",
            "sources": []
        }}
    }}
    """
    try:
        response = model.generate_content(prompt, request_options=request_options)
        json_response = response.text.strip().replace("`", "").replace("json", "")
        return json.loads(json_response)
    except Exception as e:
        error_response = {}
        for q in questions:
            error_response[q] = {"answer": f"!!-- GEMINI API ERROR --!! Details: {e}", "sources": []}
        return error_response
if __name__ == "__main__":
    command = sys.argv[1]
    
    if command == "extract_text":
        file_path = sys.argv[2]
        print(extract_text_from_file(file_path))

    elif command == "extract_questions":
        input_text = sys.stdin.read()
        questions = extract_questions_from_text(input_text)
        print(json.dumps(questions))

    elif command == "find_evidence_batch":
        # Questions are passed as a JSON string via stdin
        # Evidence is passed as a file path in the second argument
        input_data = json.loads(sys.stdin.read())
        questions_list = input_data['questions']
        evidence_content = input_data['evidence']

        results = find_evidence_for_batch(questions_list, evidence_content)
        print(json.dumps(results, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)