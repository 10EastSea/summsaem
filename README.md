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
# NCP_APIGW_API_KEY_ID='{client_id}'  # fadeout
# NCP_APIGW_API_KEY='{client_secret}' # fadeout
```

## Run
```bash
cd app/
uvicorn main:app --reload
```