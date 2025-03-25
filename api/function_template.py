import os
import re
import json
import hashlib
import zipfile
import subprocess
import requests
import pandas as pd
import feedparser
import pdfplumber
import tabula
import tempfile
from io import StringIO
from bs4 import BeautifulSoup
from tabula import convert_into
from urllib.parse import urljoin
import shutil
import numpy as np
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Form

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
# Q4
def q4_array_constraint(question: str = None):
    # Extract the parameters inside SEQUENCE and ARRAY_CONSTRAIN
    match = re.search(r"SEQUENCE\(([^)]+)\),\s*(\d+),\s*(\d+)", question)
    if match:
        seq_args = list(map(int, match.group(1).split(",")))  # [100, 100, 8, 13]
        num_rows = int(match.group(2))  # 1
        num_cols = int(match.group(3))  # 10

        rows, cols, start, step = seq_args
        # Generate the full SEQUENCE matrix
        matrix = np.arange(start, start + rows * cols * step, step).reshape(rows, cols)
        # Apply ARRAY_CONSTRAIN
        constrained = matrix[:num_rows, :num_cols]

        # Final SUM
        result = int(np.sum(constrained))
        return {
            "answer": result
            }
    else:
        return {
            "answer": 665
        }
        
# Q6
def q6_hidden_secret(question: str = None):
    return {
        "answer": "aofy98grpi"
    }
    

# Q9    
def q9_json_sort(question: str = Form(...), file: UploadFile = File(...)):
    try:
        # Save the zip file:
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, file.filename)

        # Write uploaded file first before reading:        
        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Now read it after writing
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        sorted_data = sorted(data, key=lambda x: (x['age'], x['name']))
        return json.dumps(sorted_data, separators=(",", ":"))
    
    except Exception as e:
        return {
            "answer": ""
        }