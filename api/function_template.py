import os
import re
import csv
import json
import base64
import hashlib
import zipfile
import subprocess
import requests
import pandas as pd
import feedparser
import pdfplumber
import tabula
import tempfile
import tiktoken
from io import StringIO
from bs4 import BeautifulSoup
from tabula import convert_into
from urllib.parse import urljoin
import shutil
import numpy as np
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }

# Q53
def q53_json_sales(question: str = Form(...), file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path =  os.path.join(temp_dir, file.)   
        return {
            "answer": "q53_json_sales"
        }
    except:
        return "error!"
       
# Q54
def q54_key_count(question: str = Form(...), file: UploadFile = File(...)):
    return {
        "answer": "q54_key_count"
    }
