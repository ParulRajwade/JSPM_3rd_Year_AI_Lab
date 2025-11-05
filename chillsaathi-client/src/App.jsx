import React from "react";
import Navbar from "./components/navbar";
import Meditation from './components/Meditation';
import Community from './components/Community';
import Homepage from "./components/Homepage"; // ✅ CORRECT import
import Profile from './components/profile';
import Login from "./components/Login";
import Signup from "./components/signup";
import ChatAndMoodPage from "./components/ChatAndMoodPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

function App() {
  return ( 
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/Home" element={<Homepage />} />
        <Route path="/chatbot" element={<ChatAndMoodPage/>} />
     <Route path="/meditation" element={<Meditation />} />
<Route path="/community" element={<Community />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;
