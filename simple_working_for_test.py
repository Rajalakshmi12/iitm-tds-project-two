from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return "yes"


# vercel file
# {
#     "version": 2,
#     "routes": [
#       {
#         "src": "/(.*)",
#         "dest": "/api/index.py"
#       }
#     ]
#   }
  