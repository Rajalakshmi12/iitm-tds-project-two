import os
import requests
import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import tabula
from tabula import convert_into
import pdfplumber
import re

def q46_tabula_marks(question):
    # Define dynamic regular expressions for extracting values
    subject_pattern = r"total\s+([A-Za-z]+)\s+marks"  # Capture subject (e.g., English)
    score_pattern = r"(\d+)\s*or\s+more\s+marks\s+in\s+([A-Za-z\s]+)\s+in\s+groups"  # Capture minimum score and the subject
    groups_pattern = r"groups\s+(\d+)-(\d+)"  # Capture group range
    
    # Extract the subject (e.g., English)
    subject_match = re.search(subject_pattern, question)
    subject = subject_match.group(1) if subject_match else None
    
    # Extract the score (e.g., 59 or more) and the subject (e.g., Biology)
    score_match = re.search(score_pattern, question)
    min_score = int(score_match.group(1)) if score_match else None
    score_subject = score_match.group(2) if score_match else None
    
    # Extract group range (e.g., 63-93)
    group_match = re.search(groups_pattern, question)
    group_start = int(group_match.group(1)) if group_match else None
    group_end = int(group_match.group(2)) if group_match else None

    # Create dictionary of extracted parameters
    params = {
        'subject': subject,
        'min_score': min_score,
        'score_subject': score_subject,
        'group_start': group_start,
        'group_end': group_end
    }

    #Save contents from url into folder location
    pdf_path = os.path.join(os.path.dirname(__file__), "q-extract-tables-from-pdf.pdf")
    print(pdf_path)

    # with open(pdf_path, "rb") as f:
    #     pdf_bytes = f.read()
    #     print(pdf_bytes[:200])  # print first 100 bytes for a peek

    total_english = 0

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(params['group_start']-1,params['group_end']):
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.apply(pd.to_numeric, errors='coerce')
                    filtered = df[df[params['score_subject']] >= params['min_score']]
                    total_english += filtered[params['subject']].sum()
        return {"answer": int(total_english)}
    except Exception as e:
        return {"error": str(e)}


# Test the function
question = "What is the total English marks of students who scored 59 or more marks in Biology in groups 63-93 (including both groups)?"
params = q46_tabula_marks(question)
print(params)



