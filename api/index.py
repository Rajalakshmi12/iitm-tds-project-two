from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import zipfile
import pandas as pd
from io import BytesIO
import os
import importlib

# Function Template import
from api.function_template import *

# Project 2 starts here
app = FastAPI()
function_module = importlib.import_module("api.function_template")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as necessary for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    #Import the `function_template` module at the top (globally)
    available_functions = {name: getattr(function_module, name) for name in dir(function_module) if callable(getattr(function_module, name))}
    return f"Loaded Functions: {list(available_functions.keys())}"

@app.get("/api/")
async def read_api_root():
    return {"message": "Welcome to my FastAPI application!"}


def load_questions(csv_path: str):
    """Load questions from CSV and return as a DataFrame."""
    try:
        df = pd.read_csv(csv_path)
        df['keywords'] = df['keywords'].astype(str)  # Ensure all keywords are strings
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CSV: {e}")

def find_closest_question(input_question: str, df: pd.DataFrame):
    """Find the closest matching question based on maximum keyword matches and return its function name."""
    
    input_keywords = set(input_question.lower().split())  # Extract keywords from the input question
    
    best_match = None
    max_keyword_overlap = 0
    
    for _, row in df.iterrows():
        question_keywords = set(str(row['keywords']).lower().split(', '))  # Ensure keywords are treated as strings
        overlap = len(input_keywords.intersection(question_keywords))
        
        if overlap > max_keyword_overlap:
            max_keyword_overlap = overlap
            best_match = row['function_name']
    
    return best_match

@app.get("/api/ask_question/")
async def ask_question(question: str = Query(..., title="User Question")):
    """Finds the closest question from CSV based on keyword matches and returns the corresponding function name."""
    try:
        module_path = "api.function_template"
        
        df = load_questions("api/question_template.csv")  # Ensure the correct CSV path
        function_name = find_closest_question(question, df)
        
        if not function_name:
            return "No closest match found, try another question."
        else:
            # ✅ Check if function exists and call it dynamically
            if hasattr(function_module, function_name):
                function_to_call = getattr(function_module, function_name)
            
                try:
                    if function_to_call:
                        function_output = function_to_call(question=question)
                        #return {"function_name": function_name, "output": function_output}
                        return {"function_name": function_name, "output": function_output}
                    else:
                        raise HTTPException(status_code=404, detail=f"Function {function_name} {function_to_call} not found in {module_path}")

                except TypeError:
                        return function_to_call

            else:
                return q0_nomatch(question)
                
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))