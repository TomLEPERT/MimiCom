from pydantic import BaseModel

class LoginPayload(BaseModel):
    username: str
    password: str

class UpdateCredsPayload(BaseModel):
    current_username: str
    current_password: str
    new_username: str
    new_password:str
