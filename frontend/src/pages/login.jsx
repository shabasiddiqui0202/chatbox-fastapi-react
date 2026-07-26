import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
function Login() {
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  async function handleLogin() {
    if (!mobile || !password) {
      alert("Please fill all fields");
      return;
    }
    try {
      setLoading(true);
      const response = await API.post("/login/", {
        mobile,
        password,
      });
      setLoading(false);
      if (response.data.success) {
        localStorage.setItem("user", JSON.stringify(response.data.user));

        navigate("/chat");
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error(error);
      setLoading(false);
      alert("Server Error");
    }
  }
  return (
    <div className="login-page">
      <div className="login-box">
        <h1>ChatBox</h1>
        <p>Login to continue</p>
        <input
          type="text"
          placeholder="Mobile Number"
          value={mobile}
          maxLength={10}
          onChange={(e) => setMobile(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>
          {loading ? "Please Wait..." : "Login"}
        </button>
        <p className="bottom-text">
          Don't have an account?
          <Link to="/signup"> Sign Up</Link>
        </p>
      </div>
    </div>
  );
}
export default Login;
