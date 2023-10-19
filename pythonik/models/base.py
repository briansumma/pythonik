from typing import Any, Optional, Type
from pydantic import BaseModel
import requests


class Response(BaseModel):
    # response: Type[requests.Response]
    response: Any
    data: Any
    # data: Optional[BaseModel] = None
