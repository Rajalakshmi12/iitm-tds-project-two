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
    return {
        "answer": "q16_mv_rename"
    }


# Q21
def q21_github_page(question: str = None):
    GITHUB_USERNAME = "Rajalakshmi12"
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
        
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO_NAME = "GitHub-TDS-page-email-only"

    # Minimal HTML content
    html_content = "<!--email_off-->23ds3000149@ds.study.iitm.ac.in<!--/email_off-->"
    encoded_content = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")

    # --- Create repo ---
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    create_repo = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json={"name": REPO_NAME, "private": False, "auto_init": False}
    )
    if create_repo.status_code not in [200, 201]:
        return {
            "answer": 404
        }

    # --- Upload index.html to gh-pages branch ---
    upload_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/index.html"
    upload_payload = {
        "message": "Add index.html with email",
        "content": encoded_content,
        "branch": "gh-pages"
    }
    upload = requests.put(upload_url, headers=headers, json=upload_payload)
    if upload.status_code not in [200, 201]:
        return {
            "answer": 404
        }

    # --- Enable GitHub Pages ---
    pages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"
    pages_payload = {"source": {"branch": "gh-pages", "path": "/"}}
    pages = requests.post(pages_url, headers=headers, json=pages_payload)

    if pages.status_code in [201, 204]:
        return {
            "answer": f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
        }
    else:
        return {
            "answer": 404
        }
