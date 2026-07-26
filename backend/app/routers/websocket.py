from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from pydantic import BaseModel
from app.database import get_db
from ..models.models import Message
from ..websocket_manager import manager
import json
router = APIRouter()
class WSMessagePayload(BaseModel):
    sender: str
    receiver: str
    message: str
@router.post("/ws/send")
async def websocket_send_message(payload: WSMessagePayload, db: Session = Depends(get_db)):
    if not payload.sender.strip():
        raise HTTPException(status_code=400, detail="Sender is required")
    if not payload.receiver.strip():
        raise HTTPException(status_code=400, detail="Receiver is required")
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    try:
        new_message = Message(
            sender=payload.sender,
            receiver=payload.receiver,
            message=payload.message.strip(),
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
        payload_data = {
            "type": "message",
            **response,
        }
        try:
            if manager.is_online(payload.receiver):
                await manager.send_personal_message(payload.receiver, payload_data)
            if manager.is_online(payload.sender):
                await manager.send_personal_message(payload.sender, payload_data)
        except Exception:
            pass
        return {"success": True, "data": response}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/ws/messages")
def websocket_get_messages(sender: str, receiver: str, db: Session = Depends(get_db)):
    if not sender.strip() or not receiver.strip():
        raise HTTPException(status_code=400, detail="Sender and receiver are required")
    chats = (
        db.query(Message)
        .filter(
            or_(
                and_(Message.sender == sender, Message.receiver == receiver),
                and_(Message.sender == receiver, Message.receiver == sender),
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
@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                try:
                    message = json.loads(data)
                except Exception as e:
                    print(f"Error parsing JSON from {username}: {e}")
                    continue
                receiver = message.get("receiver")
                if receiver and manager.is_online(receiver):
                    await manager.send_personal_message(receiver, message)

                await manager.send_personal_message(username, message)
            except WebSocketDisconnect:
                raise
            except Exception as e:
                print(f"Error processing message from {username}: {e}")
                continue
    except WebSocketDisconnect:
        manager.disconnect(username)
        print(f"✅ {username} disconnected")
    except Exception as e:
        print(f"WebSocket error for {username}: {e}")
        manager.disconnect(username)
