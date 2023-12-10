import json
import os
import requests
from internal.maintenance import *
from internal.variables import *

CLOVA_SUMMARY_API = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"

LIMIT_CLOVA_SUMMARY_API_CHARACTER = 2000 - ONE_CHARACTER_BUFFER


async def run_summary_with_clova_api(content: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    - API docs: https://api.ncloud-docs.com/docs/ai-naver-clovasummary-api
    """
    content = content[:LIMIT_CLOVA_SUMMARY_API_CHARACTER]
    
    headers = {
        "X-NCP-APIGW-API-KEY-ID": os.getenv("NCP_APIGW_API_KEY_ID"),
        "X-NCP-APIGW-API-KEY": os.getenv("NCP_APIGW_API_KEY"),
        "Content-Type": "application/json"
    }
    data = {
        "document": {
            "content": content
        },
        "option": {
            "language": "ko",
            "model": "general",
            "tone": 0,
            "summaryCount": 5
        }
    }
    print_log("INPUT", "summary request.data", data)

    response = requests.post(url=CLOVA_SUMMARY_API, headers=headers, json=data)
    print_log("OUTPUT", "summary response.text", response.text)

    summary = json.loads(response.text)["summary"]
    return summary
