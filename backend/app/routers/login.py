from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin

router = APIRouter(prefix="/login", tags=["Login"])
@router.post("/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    check_user = db.query(User).filter(User.mobile == user.mobile).first()
    if check_user is None:
        return {"success": False, "message": "User is not found"}

    if check_user.password != user.password:
        return {"success": False, "message": "this password is wrong"}
    check_user.online = True
    db.commit()
    return {
        "success": True,
        "message": " ",
        "user": {
            "id": check_user.id,
            "name": check_user.name,
            "mobile": check_user.mobile,
            "online": check_user.online,
        },
    }
@router.get("/users")
def logged_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.online == True).all()
    data = []
    for user in users:
        data.append({"id": user.id, "name": user.name, "mobile": user.mobile})
    return data
@router.post("/logout")
def logout(mobile: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        user.online = False
        db.commit()
    return {"success": True, "message": "Logout Successful"}
