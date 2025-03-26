import json
import base64
from fastapi import File, Form, UploadFile

# Function to extract necessary information and generate JSON body
def q32_extract_text(question: str = Form(...), file: UploadFile = File(...)):
    model = "gpt-4o-mini"  # The model is fixed as per the question

    # Extract user content from the question text (based on the example)
    user_content = "Extract text from this image"  # We know this from the question

    # Convert the image to base64
    with open(image_file, "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
    # Define the request body
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

# Example usage:
question = """Write just the JSON body (not the URL, nor headers) for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint.
Use gpt-4o-mini as the model.
Send a single user message to the model that has a text and an image_url content (in that order).
The text content should be Extract text from this image.
Send the image_url as a base64 URL of the image above. CAREFUL: Do not modify the image."""

# Provide the image file path (replace this with your actual image path)
image_file = "path/to/your/image.png"

# Generate the request body
request_body = q32_extract_text(question, image_file)

# Print the generated request body
print(request_body)
