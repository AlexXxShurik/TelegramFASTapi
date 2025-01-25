from pydantic import BaseModel

class ImeiRequest(BaseModel):
    imei: str
    token: str
