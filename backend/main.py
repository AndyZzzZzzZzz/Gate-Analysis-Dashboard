from fastapi import FastAPI
# Cross-Origin Resource Sharing policies, allow frontend on different domain/porttalk to this api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORS middleware to the app (extra functionalities that runs before and after every request)
app.add_middleware(
    CORSMiddleware,     
    allow_origins=["*"],        # Alow connection from any domain
    allow_credentials=True,     # Alow cookies, authorization headers
    allow_methods=["*"],        # Allow all HTTP method 
    allow_headers=["*"]         # Allow any headers in the request 
)

# Define HTTP Get endpoint
@app.get("/api/data")
async def get_data():
    return {"labels": ["A", "B", "c"], "values": [10, 20, 30]}

# uvicorn main:app --reload --port 8000