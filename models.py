from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None