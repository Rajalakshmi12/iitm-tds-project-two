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
    country_pattern = re.compile(r'country\s+([a-zA-Z\s]+)(?=\s+on)', re.IGNORECASE)
    city_pattern = re.compile(r'city\s+([a-zA-Z\s]+?)(?=\s+in)', re.IGNORECASE)
    direction_pattern = re.compile(r'(minimum|maximum)\s+(latitude|longitude)', re.IGNORECASE)

    # Extract country
    country_match = country_pattern.search(question)
    if country_match:
        country = country_match.group(1).strip()
    else:
        country = None

    # Extract city
    city_match = city_pattern.search(question)
    if city_match:
        city = city_match.group(1).strip()
    else:
        city = None

    # Extract direction and term (latitude or longitude)
    direction_match = direction_pattern.search(question)
    if direction_match:
        direction = direction_match.group(1).lower()  # 'minimum' or 'maximum'
        term = direction_match.group(2).lower()  # 'latitude' or 'longitude'
    else:
        direction = None
        term = None

    params = {
        'country': country,
        'city': city,
        'direction': direction,
        'term': term
    }

    url = f"https://nominatim.openstreetmap.org/search?city={params['city']}&country={params['country']}&format=json"
    headers = {
        "User-Agent": "TdsProjectTwo/1.0"
    }
    
    response = requests.get(url, params=params, headers=headers)
    nominatim_response = response.json()
    
    if nominatim_response:
        if params['direction'] == 'minimum':
            latitude = nominatim_response[0]['boundingbox'][0]
        else:
            latitude = nominatim_response[0]['boundingbox'][1]
        
    return {
        "answer": latitude
    }
