from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import zipfile
import pandas as pd
from io import BytesIO
import difflib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as necessary for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/api/")
async def read_api_root():
    return {"message": "Read from API root /api!"}

def create_github_repo(token, repo_name):
    if not token:
        token_to_use = os.getenv("GITHUB_TOKEN")
        
    headers = {
        "Authorization": f"token {token_to_use}",
        "Accept": "application/json"
    }

    # Create a new repository
    create_repo_url = 'https://api.github.com/user/repos'
    repo_data = {
        "name": repo_name,
        "description": "A repository created via the GitHub API",
        "private": False
    }

    response = requests.post(create_repo_url, headers=headers, json=repo_data)

    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.post("/api/create-repo/")
async def create_repo(token: str, repo_name: str):
    try:
        repo_info = create_github_repo(token, repo_name)
        return {"message": f"Repository '{repo_name}' created successfully.", "repository_url": repo_info['html_url']}
    except HTTPException as e:
        return {"error": e.detail}

def read_questions(file_path):
    with open(file_path, 'r') as file:
        questions = file.read().split('\n\n')
    return questions

def find_closest_question(input_question, questions):
    closest_match = difflib.get_close_matches(input_question, questions, n=1)
    return closest_match[0] if closest_match else None

@app.get("/api/handle_file/")
async def handle_file_upload(question: str = Form(...), file: UploadFile = File(...)):
    try:
        questions = read_questions('app/Questions.md')
        closest_question = find_closest_question(question, questions)
        if not closest_question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Read the uploaded zip file
        with zipfile.ZipFile(BytesIO(await file.read())) as zip_file:
            # Extract the CSV file
            with zip_file.open('extract.csv') as csv_file:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file)
                # Get the value in the "answer" column
                answer_value = df['answer'].iloc[0]
                return {"question": closest_question, "answer": answer_value}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# # Commenting out the commit part
# def create_github_repo_and_commit_file(username, token, repo_name, file_path, file_content):
#     headers = {
#         "Authorization": f"token {token}",
#         "Accept": "application/json"
#     }

#     # Create a new repository
#     create_repo_url = 'https://api.github.com/user/repos'
#     repo_data = {
#         "name": repo_name,
#         "description": "A repository created via the GitHub API",
#         "private": False
#     }

#     response = requests.post(create_repo_url, headers=headers, json=repo_data)

#     if response.status_code == 201:
#         print(f"Repository '{repo_name}' created successfully.")
#     else:
#         print(f"Failed to create repository: {response.json()}")
#         return

#     # Get the URL for the new repository
#     repo_url = response.json()['html_url']
#     print(f"Repository URL: {repo_url}")

#     # Create a new file in the repository
#     create_file_url = f'https://api.github.com/repos/{username}/{repo_name}/contents/{file_path}'
#     file_data = {
#         "message": "Initial commit",
#         "content": file_content.encode('utf-8').decode('utf-8')
#     }

#     response = requests.put(create_file_url, headers=headers, json=file_data)

#     if response.status_code == 201:
#         print(f"File '{file_path}' created successfully.")
#     else:
#         print(f"Failed to create file: {response.json()}")