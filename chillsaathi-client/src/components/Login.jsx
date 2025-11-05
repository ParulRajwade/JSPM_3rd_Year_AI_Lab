<<<<<<< HEAD
import React, { useState } from "react";
import "./LoginSignup.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:3000/api/auth/login", { email, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("userId", res.data.userId);
      localStorage.setItem("name", res.data.name);
      navigate("/profile");
    } catch (err) {
      alert(err.response.data.error || "Login failed");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2 className="auth-title">ChillSaathi Login</h2>
        <form onSubmit={handleLogin}>
          <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} className="auth-input" />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} className="auth-input" />
          <button type="submit" className="auth-btn">Login</button>
        </form>
        <p className="auth-link">Don’t have an account? <a href="/signup">Signup</a></p>
      </div>
    </div>
  );
};

export default Login;
=======
import React, { useState } from "react";
import "./LoginSignup.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:3000/api/auth/login", { email, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("userId", res.data.userId);
      localStorage.setItem("name", res.data.name);
      navigate("/profile");
    } catch (err) {
      alert(err.response.data.error || "Login failed");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2 className="auth-title">ChillSaathi Login</h2>
        <form onSubmit={handleLogin}>
          <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} className="auth-input" />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} className="auth-input" />
          <button type="submit" className="auth-btn">Login</button>
        </form>
        <p className="auth-link">Don’t have an account? <a href="/signup">Signup</a></p>
      </div>
    </div>
  );
};

export default Login;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
