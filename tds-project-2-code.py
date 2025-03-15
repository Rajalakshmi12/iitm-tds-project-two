from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import openai
import subprocess
import requests
import json
import pandas as pd
import shutil
import zipfile
import os

# Initialize FastAPI app
app = FastAPI()

# Load OpenAI API key (replace with your actual key or fetch from environment variables)
OPENAI_API_KEY = "your-openai-api-key"
openai.api_key = OPENAI_API_KEY

# Define request model
class QuestionRequest(BaseModel):
    question: str

# Function to generate LLM-based answer
def generate_llm_answer(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an AI assistant trained to answer graded assignment questions."},
                      {"role": "user", "content": question}],
            max_tokens=200
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Function to execute shell commands if applicable
def execute_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Function to fetch data from APIs if needed
def fetch_api_data(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching API data: {str(e)}"

# Function to process uploaded files
def process_uploaded_file(file: UploadFile) -> str:
    try:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                extracted_files = zip_ref.namelist()
                csv_file = next((f for f in extracted_files if f.endswith(".csv")), None)
                if csv_file:
                    csv_path = os.path.join(temp_dir, csv_file)
                    df = pd.read_csv(csv_path)
                    if "answer" in df.columns:
                        return str(df["answer"].iloc[0])
        
        return "File processed successfully but no answer found."
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Main route to answer assignment questions
@app.post("/api/")
def get_answer(question: str = Form(...), file: Optional[UploadFile] = File(None)):
    try:
        if file:
            return {"answer": process_uploaded_file(file)}
        
        # Example: Identify if it's a command-based question
        if "run" in question.lower() or "execute" in question.lower():
            command = question.split("run")[-1].strip()
            return {"answer": execute_command(command)}
        
        # Example: Identify if it's an API fetch question
        if "fetch" in question.lower() or "scrape" in question.lower():
            url = question.split("fetch")[-1].strip()
            return {"answer": fetch_api_data(url)}
        
        # Default to LLM response
        return {"answer": generate_llm_answer(question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run locally for testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)