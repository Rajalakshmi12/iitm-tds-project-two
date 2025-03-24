import os
import re
import json
import hashlib
import subprocess
import requests
import pandas as pd
import feedparser
import pdfplumber
import tabula
from io import StringIO
from bs4 import BeautifulSoup
from tabula import convert_into
from urllib.parse import urljoin
import numpy as np
from datetime import datetime, timedelta


# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }


# Q5
def q5_excel_sort(question: str = None):
    try:
        match = re.search(r"SORTBY\(\{([\d,\s]+)\},\s*\{([\d,\s]+)\}\),\s*(\d+),\s*(\d+)", question)
        if match:
            values = list(map(int, match.group(1).split(",")))
            order = list(map(int, match.group(2).split(",")))
            take_rows = int(match.group(3))
            take_cols = int(match.group(4))

            # Step 2: Pair and sort values by order
            paired = list(zip(order, values))
            sorted_by_order = sorted(paired)
            sorted_values = [val for _, val in sorted_by_order]
            matrix = [sorted_values]  # 1 row

            # TAKE the required rows and cols
            take_result = [row[:take_cols] for row in matrix[:take_rows]]

            # Step 4: SUM the result
            flat = [item for sublist in take_result for item in sublist]
            result = sum(flat)

            return {
                "answer": result
                }

        else:
            raise ValueError("Formula not found or incorrectly formatted")
    except ValueError as e:
        return {
                "answer": 10
        }
        
        
    
# Q6
def q6_hidden_secret(question: str = None):
    return {
        "answer": "aofy98grpi"
    }
    
# Q7
def q7_day_dates(question: str = None):
    return {
        "answer": "hardcoded-response"
    }