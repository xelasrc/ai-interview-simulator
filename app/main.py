# app/main.py

from fastapi import FastAPI

app = FastAPI(title="AI Interview Simulator")

@app.get("/")
def read_root():
    return {"message": "AI Interview Simulator API is running"}