import os
import hashlib
import subprocess
import re
import requests
import pandas as pd
from io import StringIO
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
    
#Q40
def q40_wikipedia(question: str = None):
    match = re.search(r'country=([a-zA-Z\s]+)\b', question)
    if match:
        country = match.group(1).strip()
        return country
    else:
        country = ''
    
    if 'What is the URL of your API endpoint' in question:
        return {
            "answer": f"http://127.0.0.1:8000/execute?country={country}"
        }
    else:
        return country
        wiki_url = f"https://en.wikipedia.org/wiki/{country}"
        print(wiki_url)  # Debugging: Print the URL to check if it's correct
        response = requests.get(wiki_url)

        if response.status_code != 200:
            return {"error": "Page not found or invalid request"}
        
        # Parse HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract headings
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        result = []
        # Generate Markdown outline from the headings
        markdown_outline = "## Contents\n\n"
        
        for heading in headings:
            print(heading)
            level = int(heading.name[1])  # Extract heading level from h1, h2, etc...
            markdown_outline += f"{'#' * level} {heading.get_text(strip=True)}\n\n" # '#' * level creates the correct number of # symbols

        return {
            "answer": markdown_outline
        }
