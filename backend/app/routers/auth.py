from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
class LoginRequest(BaseModel):
    mobile: str
class OTPRequest(BaseModel):
    mobile: str
    otp: str
@router.post("/login")
def login(data: LoginRequest):
    if len(data.mobile) != 10:
        return {"success": False, "message": "Invalid Mobile Number"}
    return {"success": True, "message": "OTP Sent Successfully", "otp": "1111"}
@router.post("/verify-otp")
def verify_otp(data: OTPRequest):
    if data.otp == "1111":
        return {"success": True, "message": "OTP Verified Successfully"}
    return {"success": False, "message": "Invalid OTP"}
