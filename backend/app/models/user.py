from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
import uuid
from ..database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    online = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "online": self.online,
            "created_at": self.created_at,
        }
