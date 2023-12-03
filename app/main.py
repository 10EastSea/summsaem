from fastapi import FastAPI
from routers.quiz import quiz

app = FastAPI()
app.include_router(quiz)


@app.get("/")
def read_root():
    return {"project": "summsaem"}
