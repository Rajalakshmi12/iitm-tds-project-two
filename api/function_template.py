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
    return {
        "answer": "q21_github_page"
    }
