from pydantic import BaseModel


class ImeiRequest(BaseModel):
    imei: str
    token: str


class UserRequest(BaseModel):
    user_id: int
    username: str
    token: str
