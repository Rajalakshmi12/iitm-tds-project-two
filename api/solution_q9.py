import re
import json

# Given question text
question_text = '''Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines.

[{""name"":""Alice"",""age"":48},{""name"":""Bob"",""age"":69},{""name"":""Charlie"",""age"":27},{""name"":""David"",""age"":26},{""name"":""Emma"",""age"":68},{""name"":""Frank"",""age"":90},{""name"":""Grace"",""age"":78},{""name"":""Henry"",""age"":27},{""name"":""Ivy"",""age"":85},{""name"":""Jack"",""age"":74},{""name"":""Karen"",""age"":43},{""name"":""Liam"",""age"":52},{""name"":""Mary"",""age"":19},{""name"":""Nora"",""age"":36},{""name"":""Oscar"",""age"":5},{""name"":""Paul"",""age"":11}]'''

# Extract JSON part using regex
json_match = re.search(r'\[.*\]', question_text, re.DOTALL)

if json_match:
    json_str = json_match.group(0)
    # Convert JSON string to valid format by replacing double double-quotes with single ones
    json_str = json_str.replace('""', '"')

    # Parse JSON string into a Python object
    json_data = json.loads(json_str)

    # Sorting JSON array by age, then by name
    sorted_json = sorted(json_data, key=lambda x: (x["age"], x["name"]))

    # Converting to JSON format without spaces or newlines
    result_json = json.dumps(sorted_json, separators=(',', ':'))

    # Display the result
    print(result_json)
else:
    print("Error: No JSON data found in the question text.")
