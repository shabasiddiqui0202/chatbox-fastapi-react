import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
function VerifyOTP() {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const mobile = localStorage.getItem("mobile");
  const handleVerifyOTP = async () => {
    if (otp.length !== 4) {
      alert("Please enter a valid OTP.");
      return;
    }
    try {
      setLoading(true);
      const response = await API.post(
        `/login/verify?mobile=${mobile}&otp=${otp}`,
      );
      setLoading(false);
      if (response.data.success) {
        alert("OTP Verified Successfully");
        localStorage.setItem("isLoggedIn", "true");
        navigate("/chat");
      } else {
        alert(response.data.message || "Invalid OTP");
      }
    } catch (error) {
      console.error(error);
      setLoading(false);
      alert("Verification Failed");
    }
  };
  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Verify OTP</h1>

        <input
          className="input"
          type="text"
          placeholder="Enter OTP"
          maxLength={4}
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
        <button className="button" onClick={handleVerifyOTP} disabled={loading}>
          {loading ? "Verifying..." : "Verify OTP"}
        </button>
      </div>
    </div>
  );
}

export default VerifyOTP;
