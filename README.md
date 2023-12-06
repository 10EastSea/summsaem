# summsaem

## Environment

### Language
- Python 3.10.13

### Library
- FastAPI 0.104.0
- Uvicorn[standard] 0.24.0

### `.env`
```bash
vim app/.env

OPENAI_API_KEY='{openai_api_key}'
```

## Run
```bash
cd app/
uvicorn main:app --reload
```