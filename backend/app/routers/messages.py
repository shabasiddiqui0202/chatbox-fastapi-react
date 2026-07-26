from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
import json
import asyncio
from app.database import get_db
from ..models.models import Message
from ..websocket_manager import manager

router = APIRouter(prefix="/messages", tags=["Messages"])
@router.post("/")
async def send_message(
    sender: str,
    receiver: str,
    message: str,
    db: Session = Depends(get_db),
):
    if not sender.strip():
        raise HTTPException(status_code=400, detail="Sender is required")
    if not receiver.strip():
        raise HTTPException(status_code=400, detail="Receiver is required")
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    try:
        new_message = Message(
            sender=sender,
            receiver=receiver,
            message=message.strip(),
            time=datetime.now(),
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        response = {
            "id": new_message.id,
            "sender": new_message.sender,
            "receiver": new_message.receiver,
            "message": new_message.message,
            "time": new_message.time.strftime("%H:%M"),
            "likes": json.loads(new_message.likes) if new_message.likes else [],
        }
        payload = {
            "type": "message",
            **response,
        }
        try:
            if manager.is_online(receiver):
                await manager.send_personal_message(receiver, payload)
            if manager.is_online(sender):
                await manager.send_personal_message(sender, payload)
        except Exception:
            pass
        return {"success": True, "data": response}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/")
def get_messages(
    sender: str,
    receiver: str,
    db: Session = Depends(get_db),
):
    chats = (
        db.query(Message)
        .filter(
            or_(
                and_(
                    Message.sender == sender,
                    Message.receiver == receiver,
                ),
                and_(
                    Message.sender == receiver,
                    Message.receiver == sender,
                ),
            )
        )
        .order_by(Message.time.asc())
        .all()
    )
    return {
        "success": True,
        "messages": [
            {
                "id": chat.id,
                "sender": chat.sender,
                "receiver": chat.receiver,
                "message": chat.message,
                "time": chat.time.strftime("%H:%M"),
                "likes": json.loads(chat.likes) if chat.likes else [],
            }
            for chat in chats
        ],
    }
@router.post("/like")
async def like_message(message_id: str, user: str, db: Session = Depends(get_db)):
    try:
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        likes = json.loads(msg.likes) if msg.likes else []
        if user in likes:
            likes.remove(user)
        else:
            likes.append(user)
        msg.likes = json.dumps(likes)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        payload = {
            "type": "like_update",
            "message_id": msg.id,
            "likes": likes,
            "sender": msg.sender,
            "receiver": msg.receiver,
        }
        try:
            if manager.is_online(msg.sender):
                await manager.send_personal_message(msg.sender, payload)
            if manager.is_online(msg.receiver):
                await manager.send_personal_message(msg.receiver, payload)
        except Exception:
            pass
        return {"success": True, "message": "toggled", "likes": likes}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
