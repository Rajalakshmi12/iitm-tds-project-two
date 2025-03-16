import httpx
import os
from typing import Dict, Any

print(os.getenv('OPENAI_API_KEY'))

def query_gpt():
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        },
    json = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the weather like?"}
        ]
    },
    )
    return response.json()

WEATHER_TOOL = {
    "type": "function",
    "function":{
        
    },
}

if __name__ == "__main__":
    response = query_gpt()
    print(response)