function Message({ id, sender, text, time, status = "sent", isMe, likes = [], currentUser, onLike }) {
  const getStatus = () => {
    switch (status) {
      case "sent":
        return "✓";
      case "delivered":
        return "✓✓";
      case "read":
        return "✓✓";
      default:
        return "";
    }
  };
  const hasLiked = likes.includes(currentUser);
  return (
    <div className={isMe ? "message my-message" : "message other-message"}>
      {!isMe && <p className="sender-name">{sender}</p>}
      <div className="message-box">
        <p>{text}</p>
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            alignItems: "center",
            gap: "6px",
            marginTop: "6px",
            fontSize: "11px",
            opacity: 0.7,
          }}
        >
          <span>{time}</span>
          {isMe && (
            <span
              style={{
                color: status === "read" ? "#2196F3" : "inherit",
                fontWeight: "bold",
              }}
            >
              {getStatus()}
            </span>
          )}
          <button
            onClick={() => onLike && onLike(id)}
            style={{
              border: "none",
              background: "transparent",
              cursor: "pointer",
              marginLeft: 8,
              color: hasLiked ? "#e0245e" : "#999",
              fontSize: "14px",
              opacity: hasLiked ? 1 : 0.6,
              transition: "all 0.2s",
              padding: "2px 4px",
              borderRadius: "4px",
            }}
            title="Like message"
          >
            {hasLiked ? "❤️" : "🤍"} {likes.length}
          </button>
        </div>
      </div>
    </div>
  );
}
export default Message;
