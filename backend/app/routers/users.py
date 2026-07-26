from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.user import User
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"success": True, "users": [user.to_dict() for user in users]}
@router.post("/")
def add_user(name: str, mobile: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        return {"success": True, "message": "User already exists", "user": user.to_dict()}
    user = User(name=name, mobile=mobile, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": True, "message": "User Added", "user": user.to_dict()}
@router.get("/{mobile}")
def get_user(mobile: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile == mobile).first()
    if not user:
        return {"success": False, "message": "User Not Found"}
    return {"success": True, "user": user.to_dict()}
@router.get("/online")
def get_online_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.online == True).all()
    return {"success": True, "users": [user.to_dict() for user in users]}

