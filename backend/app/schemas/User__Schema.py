from pydantic import BaseModel
class LoginRequest(BaseModel):
    mobile: str
class OTPRequest(BaseModel):
    mobile: str
    otp: str
class MessageRequest(BaseModel):
    sender: str
    message: str
