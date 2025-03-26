import os
import re
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

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }

# Q31
def q31_generate_llm(question):
    # Define regex patterns for extracting values
    model_pattern = r"model\s*=\s*\"([^\"]+)\""
    num_addresses_pattern = r"num_addresses\s*=\s*(\d+)"
    required_fields_pattern = r"required fields:\s*([\w\s\(\),]+)"
    
    # Extract the values using regex
    model_match = re.search(model_pattern, question)
    num_addresses_match = re.search(num_addresses_pattern, question)
    required_fields_match = re.search(required_fields_pattern, question)

    # Extracted values or defaults
    model = model_match.group(1) if model_match else "gpt-4o-mini"  # Default if not found
    num_addresses = int(num_addresses_match.group(1)) if num_addresses_match else 10  # Default if not found
    required_fields = [field.strip() for field in required_fields_match.group(1).split(",")] if required_fields_match else ["zip", "longitude", "city"]  # Default if not found

    # Define specific descriptions for each field
    field_descriptions = {
        "zip": "The zip code, e.g. 10001",
        "longitude": "The longitude, e.g. -87.2564",
        "latitude": "The latitude, e.g. 40.7128",
        "city": "The city, e.g. New York"
    }

    # Create dynamic schema properties based on required fields
    properties = {}
    for field in required_fields:
        description = field_descriptions.get(field, f"The {field}")
        properties[field] = {
            "type": "string" if field == "city" else "number",  # City is a string, others are numbers
            "description": description
        }

    # Define the base structure for the request body
    request_body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"Generate {num_addresses} random addresses in the US"
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "address_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "addresses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": properties,
                                "required": required_fields,
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["addresses"],
                    "additionalProperties": False
                }
            }
        }
    }

    return {
        "answer": json.dumps(request_body, indent=2)
    }

#Q32
def q32_extract_text(question: str = Form(...), file: UploadFile = File(...)):
    # Fixed model and user content
    model = "gpt-4o-mini"
    user_content = "Extract text from this image"

    # Step 1: Create a temporary directory to save the uploaded file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Step 2: Write the uploaded file to the temporary directory
        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 3: Read the image from the temporary location
        with open(temp_file_path, 'rb') as img_file:
            image_bytes = img_file.read()

        # Step 4: Base64 encode the image
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # Step 5: Construct the JSON body with the base64 encoded image
    request_body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }
    
    return json.dumps(request_body, indent=2)
