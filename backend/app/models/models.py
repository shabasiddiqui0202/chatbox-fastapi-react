from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime
import json
from ..database import Base

def generate_uuid():
    return str(uuid.uuid4())
class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=generate_uuid)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="sent")
    likes = Column(Text, default="[]")
    time = Column(DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "message": self.message,
            "status": self.status,
            "time": self.time.strftime("%H:%M"),
            "likes": json.loads(self.likes) if self.likes else [],
        }
