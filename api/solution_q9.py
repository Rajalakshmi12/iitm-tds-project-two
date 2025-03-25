def q9_json_sort(question_text):

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

        return result_json
    else:
        return "Error: No JSON data found in the question text."

question = "Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines"
print(q9_json_sort(question))
