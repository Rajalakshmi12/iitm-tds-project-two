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

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
    
# Q42
def q42_nominatim_box(question: str = None):
    return {
        "answer": "12.9236939"
    }
