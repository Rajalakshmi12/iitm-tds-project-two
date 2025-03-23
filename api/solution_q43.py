import feedparser
import re

def q43_hacker_points(question: str = None):
    match = re.search(r"\b(\d+)\b",question)
    points = match.group(1)

    url = f"https://hnrss.org/newest?points={points}&q=Hacker%20Culture"
    feed = feedparser.parse(url)
    return {
        "answer": feed['entries'][0]['link']
    }

# Test the function
question = "What is the link to the latest Hacker News post mentioning Hacker Culture having at least 80 points?"
print(q43_hacker_points(question))