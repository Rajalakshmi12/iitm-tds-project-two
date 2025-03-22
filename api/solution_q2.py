import requests
import re

def extract_latitude_direction(question: str):
    # Check if the question contains the word "latitude" and the direction (min or max)
    match = re.search(r"(minimum|maximum)\s+latitude", question, re.IGNORECASE)
    if match:
        return match.group(1).lower()  # 'minimum' or 'maximum'
    else:
        return None  # If no match is found

def get_latitude_of_chennai(direction: str = 'minimum'):
    # Construct the Nominatim API URL for Chennai, India
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': 'Chennai, India',  # Query for Chennai in India
        'format': 'json',       # Response format as JSON
        'addressdetails': 1,    # Include address details in the response
        'limit': 1              # Limit to the top 1 result to avoid unnecessary data
    }

    # Make the GET request to Nominatim API
    response = requests.get(url, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()

        # If results are returned
        if data:
            # Extract the bounding box (min_latitude, max_latitude, min_longitude, max_longitude)
            bounding_box = data[0].get('boundingbox')

            if bounding_box:
                min_latitude = bounding_box[0]  # First element is the minimum latitude
                max_latitude = bounding_box[1]  # Second element is the maximum latitude

                # Return the appropriate latitude based on the direction (min/max)
                if direction == 'minimum':
                    return min_latitude
                elif direction == 'maximum':
                    return max_latitude
                else:
                    return "Invalid direction. Use 'minimum' or 'maximum'."
            else:
                return "Bounding box not found."
        else:
            return "No results found for Chennai, India."
    else:
        return f"Error fetching data from Nominatim API. Status code: {response.status_code}"

# Example of how to use this
question = "What is the minimum latitude of the bounding box of the city Chennai in the country India on the Nominatim API?"
direction = extract_latitude_direction(question)  # Extract direction (minimum/maximum)
latitude = get_latitude_of_chennai(direction)  # Get the appropriate latitude
print(latitude)
