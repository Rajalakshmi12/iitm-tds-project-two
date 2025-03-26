import json
import base64
import tempfile
import shutil
import os
from fastapi import File, Form, UploadFile

# Function to handle file upload, process the image and generate JSON body
def q32_extract_text(question: str = Form(...), file: UploadFile = File(...)):
    # Fixed model and user content
    model = "gpt-4o-mini"
    user_content = "Extract text from this image"

    # Step 1: Create a temporary directory to save the uploaded file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Step 2: Write the uploaded file to the temporary directory
        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 3: Read the image from the temporary location
        with open(temp_file_path, 'rb') as img_file:
            image_bytes = img_file.read()

        # Step 4: Base64 encode the image
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # Step 5: Construct the JSON body with the base64 encoded image
    request_body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }
    
    return json.dumps(request_body, indent=2)