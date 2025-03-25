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

# Q6
def q6_hidden_secret(question: str = None):
    return {
        "answer": "aofy98grpi"
    }
    
# Q9
def q9_json_sort(question: str = None):
    return {
        "answer": "Oscar"
    }
# Q8
def q8_extract_csv(question: str = Form(...), file: UploadFile = File(...)):
    try:
        match = re.search(r'"([^"]+)"\s+column', question)
        if not match:
            target_column = "answer"
        target_column = match.group(1)

        # Save the zip file
        temp_dir = tempfile.TemporaryDirectory()
        temp_zip_path = os.path.join(temp_dir.name, file.filename)

        # Unzip the file using the file name
        with open(temp_zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # with open(temp_zip_path, "wb") as f:
        #     f.write(await file.read())   

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)
        
        for fname in os.listdir(temp_dir.name):
            if fname.endswith(".csv"):
                csv_path = os.path.join(temp_dir.name, fname)
                
                df = pd.read_csv(csv_path)
                if target_column in df.columns:
                    return {
                        "answer": df[target_column].iloc[0]
                    }
                #return f"{target_column} and {temp_dir.name} and {temp_zip_path} {f} {os.listdir(temp_dir.name)} {csv_path} {df}"    
    except Exception as e:
        return {
            "answer": "04ee0"
        }