from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from app.database import Base, engine
from app.routers.login import router as login_router
from app.routers.signup import router as signup_router
from app.routers.users import router as users_router
from app.routers.messages import router as messages_router
from app.routers.websocket import router as websocket_router

app = FastAPI(title="ChatBox Backend")
Base.metadata.create_all(bind=engine)
try:
    inspector = inspect(engine)
    cols = [c["name"] for c in inspector.get_columns("messages")] if inspector.has_table("messages") else []
    if "status" not in cols:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE messages ADD COLUMN status VARCHAR DEFAULT 'sent'"))
            conn.execute(text("UPDATE messages SET status='sent' WHERE status IS NULL"))
    if "likes" not in cols:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE messages ADD COLUMN likes TEXT DEFAULT '[]'"))
            conn.execute(text("UPDATE messages SET likes='[]' WHERE likes IS NULL"))
except Exception:
    pass
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(users_router)
app.include_router(messages_router)
app.include_router(websocket_router)

@app.get("/")
def home():
    return {"message": "ChatBox Backend Running"}
