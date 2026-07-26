from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserSignup

router = APIRouter(prefix="/signup", tags=["Signup"])
@router.post("/")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.mobile == user.mobile).first()
    if existing_user:
        return {"success": False, "message": "User already exists"}
    new_user = User(
        name=user.name,
        mobile=user.mobile,
        password=user.password,
        online=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "Signup successful", "user": new_user.to_dict()}
