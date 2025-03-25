import os
import re
import json
import tempfile
from fastapi import File, Form, UploadFile

def q9_json_sort(question: str = Form(...), file: UploadFile = File(...)):
    try:
        # Save the zip file:
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, file.filename)
        return temp_dir.name
    except Exception as e:
        return {}

question = "Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines"
print(q9_json_sort(question))
