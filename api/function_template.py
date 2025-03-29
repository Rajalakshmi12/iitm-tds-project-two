import os
import re
import csv
import json
import base64
import hashlib
from tkinter import Image
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
    
# Q57
def q57_reconstruct_image(question: str = Form(...), file: UploadFile = File(...)):
    mapping = []
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, file.filename)

            # Save the uploaded ZIP file
            with open(temp_file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Validate ZIP
            if not zipfile.is_zipfile(temp_file_path):
                return "error0"
            # Extract contents
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Locate CSV and image inside extracted contents
            csv_file_path = None
            image_file_path = None
            output_image_path = os.path.join(temp_dir, 'output_rgb.png')

            for root, _, files in os.walk(temp_dir):
                for name in files:
                    full_path = os.path.join(root, name)
                    if name.lower().endswith(".csv"):
                        csv_file_path = full_path
                    elif name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        image_file_path = full_path
                        
            if not csv_file_path or not image_file_path:
                return {
                        "answer": "image"
                    }
            # Read and process the CSV
            with open(csv_file_path, 'rb') as f:
                df = pd.read_csv(f)
            df.columns = df.columns.str.strip()

            def safe_int(val):
                try:
                    return int(val)
                except:
                    return 0

            mapping = [
                {
                    "original_row": safe_int(row["Original Row"]),
                    "original_col": safe_int(row["Original Column"]),
                    "scrambled_row": safe_int(row["Scrambled Row"]),
                    "scrambled_col": safe_int(row["Scrambled Column"]),
                }
                for _, row in df.iterrows()
            ]

            # Load the image using PIL
            try:
                scrambled_image = Image.open(image_file_path).convert("RGB")
                reconstructed_image = Image.new("RGB", (500, 500))

                grid_size = 5

                # Calculate the size of each piece
                piece_width = scrambled_image.width// grid_size
                piece_height = scrambled_image.height// grid_size
                reconstructed_image = Image.new("RGB", (scrambled_image.width, scrambled_image.height))

                for entry in mapping:
                    original_row = entry["original_row"]
                    original_col = entry["original_col"]
                    scrambled_row = entry["scrambled_row"]
                    scrambled_col = entry["scrambled_col"]

                    # Calculate the bounding box for the scrambled piece
                    scrambled_box = (
                        scrambled_col * piece_width,
                        scrambled_row * piece_height,
                        (scrambled_col + 1) * piece_width,
                        (scrambled_row + 1) * piece_height,
                    )

                    # Calculate the bounding box for the original position
                    original_box = (
                        original_col * piece_width,
                        original_row * piece_height,
                        (original_col + 1) * piece_width,
                        (original_row + 1) * piece_height,
                    )

                    # Crop the scrambled piece and paste it into the correct position
                    piece = scrambled_image.crop(scrambled_box)
                    reconstructed_image.paste(piece, original_box)
                
                # Save the reconstructed image
                reconstructed_image.save(output_image_path)
                with open(output_image_path, "rb") as image_file:
                    image_bytes = image_file.read()
                    base64_image = base64.b64encode(image_bytes).decode("utf-8")

                return {
                    "answer": base64_image
                }                
            except e:
                return "error2.1!"

    except Exception as e:
        return "error3!"