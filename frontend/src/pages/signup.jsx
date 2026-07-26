import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../services/api";
function Signup() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  async function handleSignup() {
    if (!name || !mobile || !password) {
      alert("Please fill all fields");
      return;
    }
    if (mobile.length !== 10) {
      alert("Enter a valid mobile number");
      return;
    }
    try {
      setLoading(true);
      const response = await API.post("/signup/", {
        name,
        mobile,
        password,
      });
      setLoading(false);
      if (response.data.success) {
        alert("Account created successfully");
        navigate("/");
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      setLoading(false);
      console.log(error);
      alert("Unable to connect to server");
    }
  }
  return (
    <div className="login-page">
      <div className="login-box">
        <h1>Create Account</h1>
        <p>Create your ChatBox account</p>
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Mobile Number"
          maxLength={10}
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleSignup}>
          {loading ? "Creating..." : "Create Account"}
        </button>
        <p className="bottom-text">
          Already have an account?
          <Link to="/"> Login</Link>
        </p>
      </div>
    </div>
  );
}
export default Signup;
