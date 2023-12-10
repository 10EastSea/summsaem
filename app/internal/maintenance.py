import datetime
import traceback
from app.internal.model import ResponseModel
from app.internal.variables import *


def get_log(io_type: str, target_name: str, content: any):
    return LOG_TEMPLATE.replace("{DATE_TIME}", str(datetime.datetime.now())) \
                      .replace("{IO_TYPE}", io_type) \
                      .replace("{TARGET_NAME}", target_name) \
                      .replace("{CONTENT}", str(content))
    
def print_log(io_type: str, target_name: str, content: any):
    print(get_log(io_type, target_name, content))


def get_failure_response_model():
    traceback_text = traceback.format_exc()
    print_log("ERROR", "failure", traceback_text)

    reason = traceback_text.split("\n")[-2]
    message = FAIL_MESSAGE_TEPLATE.replace("{REASON}", reason)
    return ResponseModel(success=False, summary=None, questions=None, message=message)
