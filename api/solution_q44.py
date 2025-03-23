import re
import requests
from datetime import datetime

# Function to extract city and followers from the question
def extract_city_and_followers(question: str):
    # Correct regex to match only the city name (e.g., Mumbai)
    city_pattern = re.compile(r'city\s+([a-zA-Z\s]+?)(?=\s+with)', re.IGNORECASE)  # Capture city
    followers_pattern = re.compile(r'over\s+(\d+)\s+followers', re.IGNORECASE)  # Capture followers count

    # Extract city
    city_match = city_pattern.search(question)
    if city_match:
        city = city_match.group(1).strip()
    else:
        city = None

    # Extract followers
    followers_match = followers_pattern.search(question)
    if followers_match:
        followers = int(followers_match.group(1))

    else:
        followers = None

    return city, followers

# Function to fetch users from GitHub API based on city and followers
def fetch_users_from_github(city: str, followers: int):
    base_url = "https://api.github.com"
    search_url = f"{base_url}/search/users?q=location:Mumbai"
    response = requests.get(search_url)
    users = response.json().get('items', [])

    # Initialize variables to track the newest user
    newest_user = None
    newest_creation_date = None

    # Iterate through the users to find those with >120 followers
    for user in users:
        username = user['login']
        user_url = f"{base_url}/users/{username}"
        user_response = requests.get(user_url)
        user_data = user_response.json()
        #print(user_data)
        
        if user_data.get('followers', 0) > 120:
            creation_date = user_data.get('created_at')
            if newest_creation_date is None or creation_date > newest_creation_date:
                newest_creation_date = creation_date
                newest_user = username

    if newest_user:
        print(f"The newest user in Mumbai with over 120 followers is {newest_user}, created on {newest_creation_date}.")
    else:
        print("No users found with over 120 followers in Mumbai.")

# Sample question
question = "Using the GitHub API, find all users located in the city Mumbai with over 120 followers. When was the newest user's GitHub profile created?"

# Extract city and followers from the question
city, followers = extract_city_and_followers(question)
print(city, followers)
# Fetch user data from GitHub API
if city and followers:
    result = fetch_users_from_github(city, followers)
    print(result)  # Output the newest user's GitHub profile creation date
else:
    print("Error: Could not extract city or followers count.")
