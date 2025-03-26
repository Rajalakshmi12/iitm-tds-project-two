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
import tiktoken

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }


#Q32
def q32_extract_text(question: str = Form(...), file: UploadFile = File(...)):
    return {
        "111111111111111"
    }
