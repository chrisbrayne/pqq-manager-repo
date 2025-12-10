# create_new_pqq.py
# This script generates a new dummy PQQ .docx file for testing.

import os
import docx

INCOMING_DIR = os.path.join(os.path.dirname(__file__), 'incoming')

NEW_PQQ_QUESTIONS = [
    "Company Name:",
    "Registered Address:",
    "Provide evidence of your Professional Indemnity Insurance.",
    "Describe your approach to Health and Safety.",
    "Provide details of your quality management system.",
    "List any RIDDOR incidents in the past 3 years.",
    "Provide your carbon reduction plan.",
    "Provide details on your data protection (GDPR) compliance.",
    "Outline your equality and diversity policy.",
    "Provide a modern slavery declaration.",
]

def create_docx(filename, questions):
    """Creates a .docx file with a list of questions."""
    doc = docx.Document()
    doc.add_heading(f"Dummy PQQ: {filename}", level=1)
    for q in questions:
        doc.add_paragraph(q, style='List Bullet')
    
    filepath = os.path.join(INCOMING_DIR, filename)
    doc.save(filepath)
    print(f"Successfully created {filepath}")

if __name__ == "__main__":
    if not os.path.exists(INCOMING_DIR):
        print(f"Error: The directory '{INCOMING_DIR}' does not exist.")
    else:
        create_docx("New_PQQ_Test.docx", NEW_PQQ_QUESTIONS)
        print("New dummy PQQ file created: New_PQQ_Test.docx.")
