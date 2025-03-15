from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)

# Landing page with input and output fields for question and answer
@app.get("/api/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Question Answering App</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI Question Answering App!</h1>
            <form action="/get_answer/" method="get">
                <label for="question">Enter your question:</label><br>
                <input type="text" id="question" name="question" required><br><br>
                <input type="submit" value="Get Answer">
            </form>
        </body>
    </html>
    """

# Endpoint to process the question and return an answer
@app.get("/api/get_answer/", response_class=HTMLResponse)
async def get_answer(question: str = Query(..., title="Your Question")):
    # For now, return a simple placeholder answer
    answer = f"You asked: {question}. This is a placeholder answer."
    return {"answer": "1234567890"}