import requests

url = "http://localhost:8000/quiz/create"
files = [
    ("files", ("note1.txt", open("../data/note1.txt", "rb"))),
    ("files", ("note2.txt", open("../data/note1.txt", "rb"))),
]
data = {
    "questionType": 1,
    "numberOfQuestions": 10,
    "summaryRequired": True
}

response = requests.post(url, files=files, data=data)
print(response.json())
