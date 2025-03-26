import re
import json

# Function to generate the request body based on extracted values
def q31_generate_llm(question):
    # Define regex patterns for extracting values
    model_pattern = r"model\s*=\s*\"([^\"]+)\""
    num_addresses_pattern = r"num_addresses\s*=\s*(\d+)"
    required_fields_pattern = r"required fields:\s*([\w\s\(\),]+)"
    
    # Extract the values using regex
    model_match = re.search(model_pattern, question)
    num_addresses_match = re.search(num_addresses_pattern, question)
    required_fields_match = re.search(required_fields_pattern, question)

    # Extracted values or defaults
    model = model_match.group(1) if model_match else "gpt-4o-mini"  # Default if not found
    num_addresses = int(num_addresses_match.group(1)) if num_addresses_match else 10  # Default if not found
    required_fields = [field.strip() for field in required_fields_match.group(1).split(",")] if required_fields_match else ["zip", "longitude", "city"]  # Default if not found

    # Define specific descriptions for each field
    field_descriptions = {
        "zip": "The zip code, e.g. 10001",
        "longitude": "The longitude, e.g. -87.2564",
        "latitude": "The latitude, e.g. 40.7128",
        "city": "The city, e.g. New York"
    }

    # Create dynamic schema properties based on required fields
    properties = {}
    for field in required_fields:
        description = field_descriptions.get(field, f"The {field}")
        properties[field] = {
            "type": "string" if field == "city" else "number",  # City is a string, others are numbers
            "description": description
        }

    # Define the base structure for the request body
    request_body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"Generate {num_addresses} random addresses in the US"
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "address_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "addresses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": properties,
                                "required": required_fields,
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["addresses"],
                    "additionalProperties": False
                }
            }
        }
    }

    return {
        "answer": json.dumps(request_body, indent=2)
    }

# Input text provided
question = """As part of the integration process, you need to write the body of the request to an OpenAI chat completion call that:

Uses model gpt-4o-mini
Has a system message: Respond in JSON
Has a user message: Generate 10 random addresses in the US
Uses structured outputs to respond with an object addresses which is an array of objects with required fields: zip (number) longitude (number) city (string) .
Sets additionalProperties to false to prevent additional properties.
Note that you don't need to run the request or use an API key; your task is simply to write the correct JSON body.

What is the JSON body we should send to https://api.openai.com/v1/chat/completions for this? (No need to run it or to use an API key. Just write the body of the request below.)"""
    
# Generate the request body
request_body = q31_generate_llm(question)

# Print the generated request body
print(request_body)
