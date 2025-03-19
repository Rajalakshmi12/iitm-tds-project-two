from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>FastAPI on Vercel</title></head>
        <body>
            <h1>🚀 FastAPI is Running on Vercel!</h1>
            <p>If you see this message, your deployment was successful.</p>
        </body>
    </html>
    """