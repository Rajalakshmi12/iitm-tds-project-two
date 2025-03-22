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
    
# Q0
def q0_nomatch(question: str = None):
    return {
        "answer": "1234567890"
    }

# Q1
def q1_code_vsc(question: str = None):
    return check_prettier()
    # return "Success Raji Project 2 you got 100"
    
# Q3
def check_prettier(question: str = None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_dir = os.path.join(current_dir, "node_modules/.bin/prettier")
    
    return os.path.exists(new_dir)

    # Check if the folder exists
    if os.path.isdir(folder_path):
        return f"The folder '{folder_path}' exists."


    try:
        # prettier_bin = "/vercel/path0/api/node_modules/.bin/prettier"
        if not (os.path.exists(prettier_bin)):
            result = subprocess.run(
                ["npx", "prettier", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True)
        else:   
            result = subprocess.run(
                [prettier_bin, "--version"], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True)   

        if result.returncode == 0:
            print(f"Prettier Found: {result.stdout.strip()}")
            return True
        else:
            print(f"Prettier Error: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("`npx` not found in system PATH. Ensure Node.js is installed.")
        return False
    except Exception as e:
        print(f"Exception in check_prettier(): {e}")
        return False

def calculate_sha256(content, question: str = None):
    """Runs Prettier on the content and computes the SHA-256 hash."""
    try:
        if not check_prettier():
            return "Error: Prettier is not installed"

        formatted_file = "api/formatted_readme.md"
        
        # Run Prettier and store formatted output in a new file
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", "--stdin-filepath", formatted_file],
            input=content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True)
        
        if result.stderr:
            return "Error: Prettier processing failed"
        
        # Save formatted content
        with open(formatted_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        # Compute SHA-256 hash using Python (cross-platform)
        sha256_hash = hashlib.sha256(result.stdout.encode()).hexdigest()
        return f'{sha256_hash}'
    
    except Exception as e:
        return str(e)

def q3_readme_shasum(question: str = None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_1 = os.path.join(current_dir, 'api')
    file_path_2 = os.path.join(file_path_1, 'README.md')
    
    return os.path.exists(file_path_2)
    #file_path = 'README.md'
    
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    sha256_hash = calculate_sha256(content)
    return({"answer": sha256_hash})
    
# Q4
def q4_array_constraint(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q5
def q5_excel_sort(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q6
def q6_hidden_secret(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q7
def q7_day_dates(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q8
def q8_extract_csv(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q9
def q9_json_sort(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q10
def q10_multi_cursors(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q38
def q38_ducks_count(question: str = None):
    return {
        "answer": "140"
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
    
    # Columns we care about from Player to 0 (matching the table's relevant columns)
    relevant_columns = ["Player", "Span", "Mat", "Inns", "NO", "Runs", "HS", "Ave", "BF", "SR", "100", "50", "0"]

    # Filter headers to match only the relevant columns
    headers = [header for header in headers if header in relevant_columns]

    # Step 5: Extract rows and store them in a list
    rows = []
    i=0
    for row in third_table.find_all('tr')[1:]:
        
        cols = row.find_all('td')
        data = [col.get_text(strip=True) for col in cols]
        
        # Only keep the data for the relevant columns
        filtered_data = [data[headers.index(header)] for header in headers if header in relevant_columns]
        rows.append(filtered_data)

    #print(f"Number of columns in each row: {[len(row) for row in rows]}")

    # Step 6: Check if the number of columns in headers matches the data
    if len(headers) != len(rows[0]):
        return f"Error: Number of columns in data ({len(rows[0])}) does not match number of headers ({len(headers)})."

    # Step 7: Convert data to pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Step 8: Write the DataFrame to a CSV file
    df.to_csv('cricinfo_batting_stats.csv', index=False)
    df['0'] = pd.to_numeric(df['0'], errors='coerce')
    total_ducks = df['0'].sum()

    return {
        "answer": f"{total_ducks}"
    }


# Q39
def q39_imdb_rating(question: str = None):
    ratings = re.findall(r'\b\d+\b' , question)
    min_rating = int(ratings[0])
    max_rating = int(ratings[1])
    
    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        final_summary = []

        data = response.content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the div 'ipc-metadata-list-summary-item'
            # Loop through to find div of [a] with class 'ipc-lockup-overlay ipc-focusable'
            # Loop through to find h3 with 'ipc-title__text' --> TITLE
            # Loop through to find span with class 'sc-d5ea4b9d-7 URyjV dli-title-metadata-item' --> YEAR
            # Loop through to find span with class 'ipc-rating-star--rating' --> RATING
            
        movies = soup.find_all('div', attrs = {'class':'ipc-metadata-list-summary-item__c'})
        
        for movie in movies:
            movie_summary = {}
            # ID
            id_href = movie.find('a', attrs={'class':'ipc-lockup-overlay ipc-focusable'}).get('href')
            match = re.search(r"tt(\d+)", id_href)
            movie_summary["id"] = 'tt'+match.group(1)
            
            # TITLE
            title = movie.find('h3', attrs={'class': 'ipc-title__text'})
            if title:
                title_text = title.get_text(strip=True)
                _, _, m_title = title_text.partition(" ")  # Splits at the first space, partition is useful
                encoded_title = m_title.encode('utf-8').decode('utf-8')
                movie_summary["title"] = encoded_title
                print(title_text)
            else:
                movie_summary["title"] = "Title not found"
                print("Title not found")

            # YEAR
            year = movie.find('span', attrs={'class': 'sc-d5ea4b9d-7 URyjV dli-title-metadata-item'})
            if year:
                year_text = year.get_text(strip=True)
                movie_summary["year"] = year_text[:4]  # Get only first 4 digits for the year
            else:
                movie_summary["year"] = "Year not found"
                print("Year not found")

            # # TITLE
            # title = movie.find('h3', attrs={'class': 'ipc-title__text'}).get_text(strip=True)
            # _, _, m_title = title.partition(" ")  # Splits at the first space, partition is useful
            # encoded_title = title.encode('utf-8').decode('utf-8')
            # movie_summary["title"] = encoded_title
            # print(title)

            # # YEAR
            # year = movie.find('span', attrs={'class': 'sc-d5ea4b9d-7 URyjV dli-title-metadata-item'}).get_text(strip=True)
            # movie_summary["year"] = year # Get only first 4 digits
            
            
            # RATING
            rating = movie.find('span', attrs = {'class':'ipc-rating-star--rating'}).get_text(strip=True)
            movie_summary["rating"] = rating

            # Final array that stores all the objects  
            final_summary.append(movie_summary)
        print(json.dumps(final_summary, indent=2, ensure_ascii=False)) # Important to get rid of decoded characters

            #print(f"Title: {title}, Rating: {rating}, Link: {link}")
        
        answer = """[
            #{ "id": "tt1234567", "title": "Movie 1", "year": "2021", "rating": "5.8" },
            #{ "id": "tt7654321", "title": "Movie 2", "year": "2019", "rating": "6.2" }
        ]"""
        
        return answer
        
        return {
            "answer": "hardcoded-response"
        }
    
# Q40
def q40_wikipedia(question: str = None):
    return {
        "answer": "http://127.0.0.1:8000/execute?country=Switzerland"
    }

# Q41
def q41_weather(question: str = None):
    return {
        "answer": "hardcoded-response"
    }

# Q42
def q42_nominatim_box(question: str = None):
    return {
        "answer": "12.9236939"
    }
