from fastapi import WebSocket
from typing import Dict
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        if username in self.active_connections:
            try:
                await self.active_connections[username].close()
            except Exception:
                pass
        self.active_connections[username] = websocket
        print(f"{username} connected")
        print("Online Users:", list(self.active_connections.keys()))
    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
        print(f"{username} disconnected")
        print("Online Users:", list(self.active_connections.keys()))
    async def send_personal_message(self, username: str, message: dict):
        websocket = self.active_connections.get(username)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending message to {username}: {e}")
                self.disconnect(username)
    async def broadcast(self, message: dict):
        disconnected_users = []
        for username, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {username}: {e}")
                disconnected_users.append(username)

        for username in disconnected_users:
            self.disconnect(username)
    def is_online(self, username: str):
        return username in self.active_connections
    def get_online_users(self):
        return list(self.active_connections.keys())
manager = ConnectionManager()
