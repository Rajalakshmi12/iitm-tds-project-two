import os
import hashlib
import subprocess
import re
import requests
import pandas as pd
from io import StringIO
import requests
from bs4 import BeautifulSoup
import json
import feedparser

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
    
    
# Q44
def q44_github_user(question: str = None):
    return {
        "answer": "hardcoded-response"
    }


def q43_hacker_points(question: str = None):
    match = re.search(r"\b(\d+)\b",question)
    points = match.group(1)

    url = f"https://hnrss.org/newest?points={points}&q=Hacker%20Culture"
    feed = feedparser.parse(url)
    return {
        "answer": feed['entries'][0]['link']
    }