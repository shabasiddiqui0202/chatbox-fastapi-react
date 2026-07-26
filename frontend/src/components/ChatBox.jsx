import { useEffect, useRef } from "react";
import Message from "./Message";
function ChatBox({ messages, currentUser, onLike }) {
  const bottomRef = useRef(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);
  return (
    <div className="chat-box">
      {messages.length === 0 ? (
        <div className="empty-chat">
          <h3>Welcome to ChatBox 👋</h3>
          <p>Start a conversation by sending your first message.</p>
        </div>
      ) : (
        <>
          {messages.map((msg) => (
            <Message
              key={msg.id}
              id={msg.id}
              sender={msg.sender}
              text={msg.message}
              time={msg.time}
              status={msg.status}
              likes={msg.likes || []}
              currentUser={currentUser}
              isMe={msg.sender === currentUser}
              onLike={(messageId) => onLike && onLike(messageId)}
            />
          ))}

          <div ref={bottomRef} />
        </>
      )}
    </div>
  );
}
export default ChatBox;
