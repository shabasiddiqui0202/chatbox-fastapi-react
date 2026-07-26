import { useRef } from "react";
function OTPInput({ otp, setOtp }) {
  const inputRefs = useRef([]);
  const handleChange = (value, index) => {
    if (!/^[0-9]?$/.test(value)) {
      return;
    }
    const otpArray = otp.split("");
    otpArray[index] = value;
    const newOtp = otpArray.join("");
    setOtp(newOtp);
    if (value && index < 3) {
      inputRefs.current[index + 1].focus();
    }
  };
  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1].focus();
    }
  };
  return (
    <div className="otp-container">
      {[0, 1, 2, 3].map((index) => (
        <input
          key={index}
          ref={(element) => (inputRefs.current[index] = element)}
          className="otp-input"
          type="number"
          maxLength="1"
          value={otp[index] || ""}
          onChange={(e) => handleChange(e.target.value, index)}
          onKeyDown={(e) => handleKeyDown(e, index)}
        />
      ))}
    </div>
  );
}
export default OTPInput;
