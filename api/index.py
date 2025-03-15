from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return """
        <html>
            <head>
                <title>Test FastAPI on Vercel</title>
            </head>
            <body>
                <h1>Hello, World!</h1>
                <p>Welcome to the FastAPI app deployed on Vercel.</p>
            </body>
        </html>
        """
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")