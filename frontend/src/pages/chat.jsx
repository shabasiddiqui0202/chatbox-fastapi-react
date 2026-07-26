import { useEffect, useState, useRef } from "react";
import axios from "axios";
import Sidebar from "../components/sidebar";
import ChatBox from "../components/ChatBox";
import { createSocket } from "../services/websocket";
function Chat() {
  const savedUser = JSON.parse(localStorage.getItem("user"));
  const currentUser = savedUser || {
    name: "Guest",
    mobile: "",
  };
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [chats, setChats] = useState({});
  const [message, setMessage] = useState("");
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  const chatsRef = useRef(chats);
  const reconnectTimeoutRef = useRef(null);
  const isConnectingRef = useRef(false);
  useEffect(() => {
    chatsRef.current = chats;
  }, [chats]);
  useEffect(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN || isConnectingRef.current) {
      return;
    }
    isConnectingRef.current = true;
    const ws = createSocket(currentUser.name);
    wsRef.current = ws;
    ws.onopen = () => {
      console.log(" Connected to WebSocket");
      setConnected(true);
      isConnectingRef.current = false;
    };

    ws.onclose = () => {
      console.log(" Disconnected from WebSocket");
      setConnected(false);
      isConnectingRef.current = false;      
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      reconnectTimeoutRef.current = setTimeout(() => {
        if (wsRef.current?.readyState !== WebSocket.OPEN) {
          console.log("🔄 Attempting to reconnect...");
          const newWs = createSocket(currentUser.name);
          wsRef.current = newWs;
          setupWebSocketHandlers(newWs);
        }
      }, 3000);
    };
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setConnected(false);
      isConnectingRef.current = false;
    };
    setupWebSocketHandlers(ws);
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.close();
      }
      wsRef.current = null;
    };
  }, []); 
  const setupWebSocketHandlers = (ws) => {
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "like_update") {
          setChats((prev) => {
            const updated = { ...prev };
            const msgId = data.message_id;
            for (const k of Object.keys(updated)) {
              updated[k] = (updated[k] || []).map((m) =>
                m.id === msgId ? { ...m, likes: data.likes } : m
              );
            }
            return updated;
          });
          return;
        }
        const chatUser =
          data.sender === currentUser.name ? data.receiver : data.sender;
        if (!chatUser) return;
        setChats((prev) => {
          const existing = prev[chatUser] || [];
          if (existing.some((m) => m.id === data.id)) {
            return prev;
          }
          return {
            ...prev,
            [chatUser]: [...existing, data],
          };
        });
      } catch (err) {
        console.error("Error parsing websocket message:", err);
      }
    };
  };
  useEffect(() => {
    loadUsers();
  }, []);
  async function loadUsers() {
    try {
      const res = await axios.get("http://localhost:8001/users/");
      const list = res.data.users.filter((u) => u.name !== currentUser.name);
      setUsers(list);
      if (list.length > 0) {
        setSelectedUser(list[0]);
      }
    } catch (err) {
      console.log(err);
    }
  }
  useEffect(() => {
    if (selectedUser) {
      loadMessages();
    }
  }, [selectedUser]);
  async function loadMessages() {
    try {
      const res = await axios.get("http://localhost:8001/messages/", {
        params: {
          sender: currentUser.name,
          receiver: selectedUser.name,
        },
      });
      setChats((prev) => ({
        ...prev,
        [selectedUser.name]: res.data.messages,
      }));
    } catch (err) {
      console.log(err);
    }
  }
  async function sendMessage() {
    if (!message.trim()) return;
    if (!selectedUser) return;
    const msg = {
      sender: currentUser.name,
      receiver: selectedUser.name,
      message: message.trim(),
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };
    try {
      const res = await axios.post("http://localhost:8001/ws/send", {
        sender: msg.sender,
        receiver: msg.receiver,
        message: msg.message,
      });
      const saved = res.data.data;
      const toShow = { ...msg, id: saved.id, likes: saved.likes || [] };
      setChats((prev) => {
        const existing = prev[selectedUser.name] || [];
        if (existing.some((m) => m.id === saved.id)) {
          return prev;
        }
        return {
          ...prev,
          [selectedUser.name]: [...existing, toShow],
        };
      });
      setMessage("");
    } catch (err) {
      console.log(err);
    }
  }
  return (
    <div className="app-layout">
      <Sidebar
        users={users}
        selectedUser={selectedUser}
        setSelectedUser={setSelectedUser}
      />
      <div className="chat-section">
        <div className="chat-header">
          <div>
            <h2>{selectedUser ? selectedUser.name : "Select User"}</h2>
            <p>{connected ? "Connected" : "Disconnected"}</p>
          </div>
        </div>
        <div className="chat-body">
          <ChatBox
            messages={selectedUser ? chats[selectedUser.name] || [] : []}
            currentUser={currentUser.name}
            onLike={async (messageId) => {
              if (!selectedUser) return;
              try {
                const res = await axios.post(
                  "http://localhost:8001/messages/like",
                  null,
                  {
                    params: { message_id: messageId, user: currentUser.name },
                  }
                );
                const likes = res.data.likes || [];
                setChats((prev) => {
                  const updated = { ...prev };
                  updated[selectedUser.name] = (updated[selectedUser.name] || []).map((m) =>
                    m.id === messageId ? { ...m, likes } : m
                  );
                  return updated;
                });
              } catch (err) {
                console.log(err);
              }
            }}
          />
        </div>
        <div className="chat-footer">
          <input
            type="text"
            value={message}
            placeholder="Type message..."
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            disabled={!selectedUser}
          />
          <button onClick={sendMessage} disabled={!selectedUser}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
export default Chat;
