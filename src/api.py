from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (shorten,)

app = FastAPI(title="URL Shortening Service",)

origins = [
    "http://localhost:3000", # React default for if I create a frontend for this project in the future.
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shorten.router)

@app.get("/")
async def root():
    return {"Detail": "This is a URL shortening service."}