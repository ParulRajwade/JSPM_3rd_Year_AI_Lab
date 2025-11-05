<<<<<<< HEAD
import React, { useState } from "react";
import "./Signup.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:3000/api/auth/signup", form);
      navigate("/login");
    } catch (err) {
      alert(err.response.data.error || "Signup failed");
    }
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-box">
        <h2 className="signup-title">Join ChillSaathi</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} className="signup-input" />
          <input type="email" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} className="signup-input" />
          <input type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} className="signup-input" />
          <button type="submit" className="signup-button">Signup</button>
        </form>
        <p className="signup-footer">Already have an account? <a href="/login">Login</a></p>
      </div>
    </div>
  );
};

export default Signup;

=======
import React, { useState } from "react";
import "./Signup.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:3000/api/auth/signup", form);
      navigate("/login");
    } catch (err) {
      alert(err.response.data.error || "Signup failed");
    }
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-box">
        <h2 className="signup-title">Join ChillSaathi</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} className="signup-input" />
          <input type="email" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} className="signup-input" />
          <input type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} className="signup-input" />
          <button type="submit" className="signup-button">Signup</button>
        </form>
        <p className="signup-footer">Already have an account? <a href="/login">Login</a></p>
      </div>
    </div>
  );
};

export default Signup;

>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
