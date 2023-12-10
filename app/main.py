import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers.quiz import quiz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


app = FastAPI()
app.include_router(quiz)


@app.get("/")
def read_root():
    return {"project": "summsaem"}
