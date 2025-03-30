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
from PIL import Image
import numpy as np
import colorsys
import shutil
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from io import BytesIO
from fastapi import Form, File, UploadFile
import tempfile, shutil, os, zipfile, subprocess, requests

#def q23_pixels_brightness(question: str = Form(...), file: UploadFile = File(...)):

# Q0
def q0_nomatch(question: str = None):
    return {
        "answer": "q0_nomatch"
    } 

# Q16
def q16_mv_rename(question: str = Form(...), file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, file.filename)

            # Save uploaded ZIP file
            with open(zip_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Create a new flat folder
            flat_dir = os.path.join(temp_dir, "flat")
            os.makedirs(flat_dir, exist_ok=True)

            # Move and rename all files into flat_dir
            for root, _, files in os.walk(temp_dir):
                for filename in files:
                    full_path = os.path.join(root, filename)

                    # Skip our own output and zip file
                    if full_path.startswith(flat_dir) or full_path == zip_path:
                        continue

                    # Rename: shift digits (1→2, ..., 9→0)
                    def shift_digits(name):
                        return ''.join(
                            str((int(c) + 1) % 10) if c.isdigit() else c
                            for c in name
                        )

                    new_filename = shift_digits(filename)
                    dest_path = os.path.join(flat_dir, new_filename)
                    shutil.copy2(full_path, dest_path)

            # Simulate: grep . * | LC_ALL=C sort | sha256sum
            all_lines = []
            for fname in sorted(os.listdir(flat_dir)):
                path = os.path.join(flat_dir, fname)
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            line = line.rstrip('\n')
                            all_lines.append(f"{fname}:{line}")

            all_lines.sort()
            joined = '\n'.join(all_lines) + '\n'
            sha256_hash = hashlib.sha256(joined.encode('utf-8')).hexdigest()

            return {"answer": sha256_hash}

    except Exception as e:
        return {
            "answer": str(e)
            }