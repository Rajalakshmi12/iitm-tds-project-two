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


