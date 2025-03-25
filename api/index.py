from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import zipfile
import pandas as pd
from io import BytesIO
import os
import importlib
import tempfile

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
    return f"GET Loaded Functions: {list(available_functions.keys())}"

@app.post("/vercel/")
async def read_api_root():
    return {"message": "Welcome to Vercel POST!"}

