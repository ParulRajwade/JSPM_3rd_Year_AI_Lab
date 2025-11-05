<<<<<<< HEAD
import React, { useEffect, useState } from "react";
import "./Home.css";
import { motion } from "framer-motion";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const cards = [
  { title: "Meditation", text: "Calm your mind and soul.", path: "/meditation" },
  { title: "Mood Tracker", text: "Track your emotional journey.", path: "/chatbot" },
  { title: "Journal", text: "Write and reflect daily.", path: "/Community" },
  { title: "Relaxing Music", text: "Listen and unwind peacefully.", path: "/meditation" },
  { title: "Chatbot", text: "Talk to your ChillSaathi anytime.", path: "/chatbot" },
];

const Homepage = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("http://localhost:3000/api/profile", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setUserData(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleCardClick = (path) => {
    navigate(path);
  };

  return (
    <div className="home-background">
      <div className="home-container">
        {userData && (
          <motion.div
            className="welcome-box"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <h2>Hello, {userData.name} 👋</h2>
            <p>Welcome back to ChillSaathi!</p>
            {userData.mood && (
              <p>🌈 Last Mood: <strong>{userData.mood}</strong></p>
            )}
          </motion.div>
        )}

        <motion.h1
          className="main-heading"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          Welcome to ChillSaathi
        </motion.h1>
        <motion.p
          className="sub-heading"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          Your partner in mental wellness 🌿
        </motion.p>

        <div className="cards-container">
          {cards.map((card, index) => (
            <motion.div
              className="card"
              key={index}
              whileHover={{ scale: 1.05 }}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2, duration: 0.6 }}
              onClick={() => handleCardClick(card.path)}
              style={{ cursor: "pointer" }}
            >
              <h2>{card.title}</h2>
              <p>{card.text}</p>
            </motion.div>
          ))}
        </div>

        {/* Quote Section */}
        <div className="quote-section">
          <h3 className="quote-title">🧠 Thought for Today</h3>
          <blockquote className="quote-text">
            "The mind is everything. What you think you become."
          </blockquote>
        </div>

        {/* Daily Habits */}
        <div className="daily-habits-section">
          <h3>🌱 Power of Daily Wellness Habits</h3>
          <p>Small, consistent mental wellness habits can lead to big life changes. Whether it’s 5 minutes of mindful breathing, writing down your feelings, or listening to calming sounds before bed — it all adds up.</p>
          <ul>
            <li>🕯️ Start your day with positive affirmations</li>
            <li>📓 Use a gratitude journal to shift your mindset</li>
            <li>🌿 Meditate for clarity, peace, and resilience</li>
            <li>🌙 Wind down with soothing music or Yoga Nidra</li>
          </ul>
          <p>ChillSaathi helps you build these habits with tools tailored for your journey — one day at a time.</p>
        </div>

        {/* Testimonials */}
        <div className="testimonials">
          <h3>💬 What Our Users Say</h3>
          <div className="testimonial">
            <p>"ChillSaathi helped me manage stress during exams. Love the journaling feature!" – Ananya</p>
          </div>
          <div className="testimonial">
            <p>"Daily mood tracker keeps me aware of my emotions. Beautiful design!" – Raj</p>
          </div>
        </div>

        {/* Meditation Info */}
        <div className="blog-section">
          <h3>🧘 Why Meditation Matters</h3>
          <p>Meditation is a scientifically proven way to reduce stress, improve focus, enhance emotional health, and promote better sleep. Just 10 minutes a day can make a big difference in your mental wellness.</p>
          <ul>
            <li>💗 Mindfulness</li>
            <li>🌬️ Breath awareness</li>
            <li>💞 Loving-kindness</li>
            <li>🛌 Yoga Nidra</li>
          </ul>
        </div>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <p>🌐 Developed & Designed by <strong>Chinmay Deshmukh</strong></p>
            <p>📍 JSPM's Rajarshi Shahu College of Engineering | Department:-CSBS </p>
            <p>🎨 Passionate about UI/UX ,web development,genAI,</p>
            <p>📧 Contact: <a href="mailto:chinmaydeshmukh12345@gmail.com">chinmaydeshmukh12345@gmail.com</a></p>
            <p>🔗 Connect: <a href="https://www.linkedin.com/in/chinmay-deshmukh-69aba22a1/" target="_blank" rel="noopener noreferrer">LinkedIn</a> | <a href="https://github.com/chinmay4411" target="_blank" rel="noopener noreferrer">GitHub</a></p>
            <p> ChillSaathi</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Homepage;
=======
import React, { useEffect, useState } from "react";
import "./Home.css";
import { motion } from "framer-motion";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const cards = [
  { title: "Meditation", text: "Calm your mind and soul.", path: "/meditation" },
  { title: "Mood Tracker", text: "Track your emotional journey.", path: "/chatbot" },
  { title: "Journal", text: "Write and reflect daily.", path: "/Community" },
  { title: "Relaxing Music", text: "Listen and unwind peacefully.", path: "/meditation" },
  { title: "Chatbot", text: "Talk to your ChillSaathi anytime.", path: "/chatbot" },
];

const Homepage = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("http://localhost:3000/api/profile", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setUserData(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleCardClick = (path) => {
    navigate(path);
  };

  return (
    <div className="home-background">
      <div className="home-container">
        {userData && (
          <motion.div
            className="welcome-box"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <h2>Hello, {userData.name} 👋</h2>
            <p>Welcome back to ChillSaathi!</p>
            {userData.mood && (
              <p>🌈 Last Mood: <strong>{userData.mood}</strong></p>
            )}
          </motion.div>
        )}

        <motion.h1
          className="main-heading"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          Welcome to ChillSaathi
        </motion.h1>
        <motion.p
          className="sub-heading"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          Your partner in mental wellness 🌿
        </motion.p>

        <div className="cards-container">
          {cards.map((card, index) => (
            <motion.div
              className="card"
              key={index}
              whileHover={{ scale: 1.05 }}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2, duration: 0.6 }}
              onClick={() => handleCardClick(card.path)}
              style={{ cursor: "pointer" }}
            >
              <h2>{card.title}</h2>
              <p>{card.text}</p>
            </motion.div>
          ))}
        </div>

        {/* Quote Section */}
        <div className="quote-section">
          <h3 className="quote-title">🧠 Thought for Today</h3>
          <blockquote className="quote-text">
            "The mind is everything. What you think you become."
          </blockquote>
        </div>

        {/* Daily Habits */}
        <div className="daily-habits-section">
          <h3>🌱 Power of Daily Wellness Habits</h3>
          <p>Small, consistent mental wellness habits can lead to big life changes. Whether it’s 5 minutes of mindful breathing, writing down your feelings, or listening to calming sounds before bed — it all adds up.</p>
          <ul>
            <li>🕯️ Start your day with positive affirmations</li>
            <li>📓 Use a gratitude journal to shift your mindset</li>
            <li>🌿 Meditate for clarity, peace, and resilience</li>
            <li>🌙 Wind down with soothing music or Yoga Nidra</li>
          </ul>
          <p>ChillSaathi helps you build these habits with tools tailored for your journey — one day at a time.</p>
        </div>

        {/* Testimonials */}
        <div className="testimonials">
          <h3>💬 What Our Users Say</h3>
          <div className="testimonial">
            <p>"ChillSaathi helped me manage stress during exams. Love the journaling feature!" – Ananya</p>
          </div>
          <div className="testimonial">
            <p>"Daily mood tracker keeps me aware of my emotions. Beautiful design!" – Raj</p>
          </div>
        </div>

        {/* Meditation Info */}
        <div className="blog-section">
          <h3>🧘 Why Meditation Matters</h3>
          <p>Meditation is a scientifically proven way to reduce stress, improve focus, enhance emotional health, and promote better sleep. Just 10 minutes a day can make a big difference in your mental wellness.</p>
          <ul>
            <li>💗 Mindfulness</li>
            <li>🌬️ Breath awareness</li>
            <li>💞 Loving-kindness</li>
            <li>🛌 Yoga Nidra</li>
          </ul>
        </div>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <p>🌐 Developed & Designed by <strong>Chinmay Deshmukh</strong></p>
            <p>📍 JSPM's Rajarshi Shahu College of Engineering | Department:-CSBS </p>
            <p>🎨 Passionate about UI/UX ,web development,genAI,</p>
            <p>📧 Contact: <a href="mailto:chinmaydeshmukh12345@gmail.com">chinmaydeshmukh12345@gmail.com</a></p>
            <p>🔗 Connect: <a href="https://www.linkedin.com/in/chinmay-deshmukh-69aba22a1/" target="_blank" rel="noopener noreferrer">LinkedIn</a> | <a href="https://github.com/chinmay4411" target="_blank" rel="noopener noreferrer">GitHub</a></p>
            <p> ChillSaathi</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Homepage;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
