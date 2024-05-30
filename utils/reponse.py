from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None

class HcError:
    AUTH_FAIL = 1001
    MATCH_TIMEOUT = 1002
    ALREADY_QUEUE = 1003
    ROOM_NOT_FOUND = 1004
    NOT_TURN = 1005
    SYSTEM_ERROR = 1099


def error_msg_map(err_code: int) -> str:
    m = {
        HcError.AUTH_FAIL: "auth failed, please try again later",
        HcError.MATCH_TIMEOUT: "match timeout, please try again later",
        HcError.ALREADY_QUEUE: '"already in queue, please try again later',
        HcError.ROOM_NOT_FOUND: "room not found, please try again later",
        HcError.NOT_TURN: "not your turn, please try again later",
        HcError.SYSTEM_ERROR: "some error occured, please try again later",
    }
    if err_code not in m:
        return "Unknow error"
    return m[err_code]


def create_response(data: any = None, msg: str = "ok", code: int = 0):
    if code != 0:
        return ResponseModel(code=code, msg=error_msg_map(code), data=data)
    return ResponseModel(code=code, msg=msg, data=data)
