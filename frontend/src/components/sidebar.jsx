function Sidebar({ users, selectedUser, setSelectedUser }) {
  return (
    <div className="sidebar">
      <h2 className="logo">ChatBox</h2>
      <input className="search-box" type="text" placeholder="Search user..." />
      <div className="user-list">
        {users.map((user) => (
          <div
            key={user.id}
            className={
              selectedUser && selectedUser.id === user.id
                ? "user-card active-user"
                : "user-card"
            }
            onClick={() => setSelectedUser(user)}
          >
            <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
            <div className="user-info">  
              <h4>{user.name}</h4>
              <p>{user.online ? "🟢 Online" : "⚪ Offline"}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default Sidebar;
