import { useState } from "react";
import { api } from "../services/api";

type LoginProps = {
  onLogin: (username: string) => void;
};

export default function Login({ onLogin }: LoginProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await api.post("/login", {
        username,
        password,
      });

      if (response.data.success) {
        localStorage.setItem("biw_logged_in", "true");
        localStorage.setItem("biw_username", response.data.username);
        onLogin(response.data.username);
      } else {
        alert("Invalid username or password");
      }
    } catch (error) {
      console.error(error);
      alert("Login failed");
    }
  };

  const handleRegister = async () => {
    if (!username || !password) {
      alert("Name and password are required");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      const response = await api.post("/register", {
        username,
        password,
      });

      if (response.data.success) {
        alert("Account created. Please login.");
        setMode("login");
        setPassword("");
        setConfirmPassword("");
      } else {
        alert(response.data.message || "Registration failed");
      }
    } catch (error) {
      console.error(error);
      alert("Registration failed");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-brand">
          <h1>BIW Digital Twin</h1>
          <p>Shop Floor Monitoring System</p>
        </div>

        <div className="login-form">
          <div>
            <label>Name</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter name"
            />
          </div>

          <div>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
            />
          </div>

          {mode === "register" && (
            <div>
              <label>Confirm Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm password"
              />
            </div>
          )}

          {mode === "login" ? (
            <button onClick={handleLogin}>Login</button>
          ) : (
            <button onClick={handleRegister}>Create Account</button>
          )}

          {mode === "login" ? (
            <p className="new-user-text">
              New user?{" "}
              <span onClick={() => setMode("register")}>Create account</span>
            </p>
          ) : (
            <p className="new-user-text">
              Already have an account?{" "}
              <span onClick={() => setMode("login")}>Login</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}