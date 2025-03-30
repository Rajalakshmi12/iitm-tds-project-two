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
import gzip
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from datetime import timezone
from dateutil import parser as date_parser
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from io import BytesIO
from collections import defaultdict
from fastapi import Form, File, UploadFile
import tempfile, shutil, os, zipfile, subprocess, requests

#def q23_pixels_brightness(question: str = Form(...), file: UploadFile = File(...)):

# Q0
def q0_nomatch(question: str = None):
    return {
        "answer": "q0_nomatch"
    } 

# Q51
def q51_apache_get(question: str = Form(...), file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            gz_path = f"{temp_dir}/{file.filename}"
            with open(gz_path, "wb") as f_out:
                shutil.copyfileobj(file.file, f_out)

            with gzip.open(gz_path, "rt", encoding="utf-8", errors="ignore") as f:
                log_data = f.readlines()

        count = 0
        url_filter = "/telugu/"
        t_start_hour = 11
        t_end_hour = 20

        log_pattern = re.compile(
            r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+|-) "(.*?)" "(.*?)" (\S+) (\S+)')

        for line in log_data:
            try:
                match = log_pattern.match(line)
                if match:
                    ip, timestamp, method, url, protocol, status, size, referer, user_agent, vhost, server = match.groups()
                    log_time = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

                    if (
                        method == "GET" and
                        url.startswith(url_filter) and
                        200 <= int(status) < 300 and
                        log_time.weekday() == 0 and
                        t_start_hour <= log_time.hour < t_end_hour
                    ):
                        count += 1
            except:
                continue

        return {
            "answer": count
        }

    except Exception as e:
        return {
            "answer": str(e)
        }

# Q52
def q52_apache_bytes(question: str = Form(...), file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            gz_path = f"{temp_dir}/{file.filename}"
            with open(gz_path, "wb") as f_out:
                shutil.copyfileobj(file.file, f_out)

            with gzip.open(gz_path, "rt", encoding="utf-8", errors="ignore") as f:
                log_data = f.readlines()

        ip_data = defaultdict(int)
        date_filter = "07/May/2024"
        url_filter = "/kannada/"

        for line in log_data:
            match = re.match(r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+|-) .*', line)
            if match:
                ip, timestamp, method, url, protocol, status, size = match.groups()
                if date_filter in timestamp and url.startswith(url_filter) and size.isdigit():
                    ip_data[ip] += int(size)

        if ip_data:
            top_ip, max_bytes = max(ip_data.items(), key=lambda x: x[1])
            return {
                "answer": max_bytes,
                "top_ip": top_ip
            }
        else:
            return {"answer": 0, "note": "No matching records"}

    except Exception as e:
        return {
            "answer": "error",
            "error": str(e)
        }


