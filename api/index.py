from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Function to answer a hardcoded question
def process_question(question):
    if "add two hardcoded numbers" in question.lower():
        return str(10 + 20)  # Hardcoded sum
    return "I can only answer predefined questions."

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        question = request.form.get('question', '')
        if question:
            answer = process_question(question)
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

# Save requirements.txt for dependencies
requirements = """
flask
"""
with open("requirements.txt", "w") as f:
    f.write(requirements)

# Create a basic HTML template
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Question Solver</title>
</head>
<body>
    <h1>Simple Question Solver</h1>
    <form method="post">
        <label for="question">Enter Question:</label>
        <input type="text" id="question" name="question" required>
        <button type="submit">Submit</button>
    </form>
    {% if answer is not none %}
        <h2>Answer: {{ answer }}</h2>
    {% endif %}
</body>
</html>
"""
with open("templates/index.html", "w") as f:
    f.write(html_content)