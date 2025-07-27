from fastapi import FastAPI
# Cross-Origin Resource Sharing policies, allow frontend on different domain/porttalk to this api
from fastapi.middleware.cors import CORSMiddleware
from api import data

app = FastAPI()

# Add CORS middleware to the app (extra functionalities that runs before and after every request)
app.add_middleware(
    CORSMiddleware,     
    allow_origins=["*"],        # Alow connection from any domain
    allow_credentials=True,     # Alow cookies, authorization headers
    allow_methods=["*"],        # Allow all HTTP method 
    allow_headers=["*"]         # Allow any headers in the request 
)

# API routers
app.include_router(data.router, prefix="/api")

# uvicorn main:app --reload --port 8000