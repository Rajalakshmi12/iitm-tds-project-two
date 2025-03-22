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

# Q0
def q0_nomatch(question: str = None):
    return {
        f"answer{question}": "1234567890"
    }
    
# Q38
def q38_ducks_count(question: str = None):
    match = re.search(r'page number (\d+)', question)
    if not match:
        page_number = 1
    else:
        page_number = match.group(1)

    # Step 2: Construct the URL
    url = f"https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return f"Error: Unable to fetch data from URL (HTTP Status Code: {response.status_code})"
    
    # Step 2: Parse the HTML page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find the table in the HTML
    tables = soup.find_all('table', {'class': 'engineTable'})
    
    if len(tables) >= 3:
        third_table = tables[2]  # Get the third table
    else:
        return "Error: Less than 3 tables with the class 'engineTable' found."

    # Step 4: Find the header row
    header_row = third_table.find('tr', class_='headlinks')
    if not header_row:
        return "Error: Header row with class 'headlinks' not found."

    # Extract headers (the <a> tags inside <th> elements)
    headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
    print(headers)
    
    # Columns we care about from Player to 0 (matching the table's relevant columns)
    relevant_columns = ["Player", "Span", "Mat", "Inns", "NO", "Runs", "HS", "Ave", "BF", "SR", "100", "50", "0"]

    # Filter headers to match only the relevant columns
    headers = [header for header in headers if header in relevant_columns]
    print(f"Headers found: {headers}")  # Debugging: Print the filtered headers

    # Step 5: Extract rows and store them in a list
    rows = []
    for row in third_table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        data = [col.get_text(strip=True) for col in cols]
        
        # Only keep the data for the relevant columns
        filtered_data = [data[headers.index(header)] for header in headers if header in relevant_columns]
        rows.append(filtered_data)

    # Debugging: Check the number of columns in the data
    print(f"Number of rows: {len(rows)}")
    print(f"Number of columns in each row: {[len(row) for row in rows]}")

    # Step 6: Check if the number of columns in headers matches the data
    if len(headers) != len(rows[0]):
        return f"Error: Number of columns in data ({len(rows[0])}) does not match number of headers ({len(headers)})."

    # Step 7: Convert data to pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Step 8: Write the DataFrame to a CSV file
    df.to_csv('cricinfo_batting_stats.csv', index=False)
    df['0'] = pd.to_numeric(df['0'], errors='coerce')
    total_ducks = df['0'].sum()

    return total_ducks

# Test the function
print(q38_ducks_count("What is the total number of ducks across players on page number 17 of ESPN Cricinfo's ODI batting stats?"))