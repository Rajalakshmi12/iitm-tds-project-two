import os
import hashlib
import subprocess
import re
import requests
import pandas as pd
from io import StringIO
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
    
#Q40
def q40_wikipedia(question: str = None):
    return {
        "answer": "http://127.0.0.1:8000/execute?country=Switzerland"
    }
