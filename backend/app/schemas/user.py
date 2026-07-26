from pydantic import BaseModel
class UserSignup(BaseModel):
    name: str
    mobile: str
    password: str
class UserLogin(BaseModel):
    mobile: str
    password: str
class UserResponse(BaseModel):
    id: str
    name: str
    mobile: str
    online: bool
    class Config:
        from_attributes = True
