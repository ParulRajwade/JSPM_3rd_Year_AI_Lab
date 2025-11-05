<<<<<<< HEAD
import React, { useState, useEffect } from "react";
import "./ChatAndMoodPage.css";

const moods = [
  { emoji: "😊", label: "Happy", color: "#ffeaa7" },
  { emoji: "😐", label: "Neutral", color: "#dfe6e9" },
  { emoji: "😢", label: "Sad",  color: "#74b9ff" },
  { emoji: "😡", label: "Angry", color: "#fab1a0" },
  { emoji: "😍", label: "Loved", color: "#ffcccc" },
];

function ChatMoodPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [selectedMood, setSelectedMood] = useState(null);
  const [history, setHistory] = useState([]);
  const [moodInfo, setMoodInfo] = useState(null);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("moodHistory")) || [];
    setHistory(saved);
  }, []);

  const handleMoodSelect = (mood) => {
    const entry = {
      mood: mood.label,
      emoji: mood.emoji,
      timestamp: new Date().toLocaleString(),
    };
    const newHistory = [entry, ...history.slice(0, 9)];
    setHistory(newHistory);
    localStorage.setItem("moodHistory", JSON.stringify(newHistory));
    setSelectedMood(mood.label);
    setMoodInfo(mood);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

     try {
      const res = await fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      })

      const data = await res.json();
      const botMessage = { type: "bot", text: data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "❌ Server error" },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chat-mood-wrapper">
      {/* Chat Section */}
      <div className="chatbox enhanced">
        <h2>💬 Talk to ChillSaathi</h2>
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <p key={index} className={msg.type === "user" ? "user-msg" : "bot-msg"}>
              <strong>{msg.type === "user" ? "You" : "ChillSaathi"}:</strong> {msg.text}
            </p>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type your thoughts..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>

      {/* Mood Tracker */}
      <div className="mood-tracker-panel">
        <h2>🌤️ Mood Tracker</h2>
        <div className="mood-options">
          {moods.map((mood, index) => (
            <button
              key={index}
              className={`mood-btn ${selectedMood === mood.label ? "selected" : ""}`}
              style={{ backgroundColor: selectedMood === mood.label ? mood.color : "#f1f2f6" }}
              onClick={() => handleMoodSelect(mood)}
            >
              <span className="emoji">{mood.emoji}</span>
              <span className="label">{mood.label}</span>
            </button>
          ))}
        </div>

        {moodInfo && (
          <div className="mood-feedback" style={{ backgroundColor: moodInfo.color }}>
            <h4>{moodInfo.emoji} {moodInfo.label}</h4>
            <p>{moodInfo.message}</p>
          </div>
        )}

        <div className="mood-history">
          <h3>📜 Your Mood History</h3>
          <ul>
            {history.length === 0 ? (
              <li>No moods recorded yet.</li>
            ) : (
              history.map((entry, i) => (
                <li key={i}>
                  {entry.emoji} {entry.mood} — <span>{entry.timestamp}</span>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ChatMoodPage;
=======
import React, { useState, useEffect } from "react";
import "./ChatAndMoodPage.css";

const moods = [
  { emoji: "😊", label: "Happy", color: "#ffeaa7" },
  { emoji: "😐", label: "Neutral", color: "#dfe6e9" },
  { emoji: "😢", label: "Sad",  color: "#74b9ff" },
  { emoji: "😡", label: "Angry", color: "#fab1a0" },
  { emoji: "😍", label: "Loved", color: "#ffcccc" },
];

function ChatMoodPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [selectedMood, setSelectedMood] = useState(null);
  const [history, setHistory] = useState([]);
  const [moodInfo, setMoodInfo] = useState(null);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("moodHistory")) || [];
    setHistory(saved);
  }, []);

  const handleMoodSelect = (mood) => {
    const entry = {
      mood: mood.label,
      emoji: mood.emoji,
      timestamp: new Date().toLocaleString(),
    };
    const newHistory = [entry, ...history.slice(0, 9)];
    setHistory(newHistory);
    localStorage.setItem("moodHistory", JSON.stringify(newHistory));
    setSelectedMood(mood.label);
    setMoodInfo(mood);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const botMessage = { type: "bot", text: data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "❌ Server error" },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chat-mood-wrapper">
      {/* Chat Section */}
      <div className="chatbox enhanced">
        <h2>💬 Talk to ChillSaathi</h2>
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <p key={index} className={msg.type === "user" ? "user-msg" : "bot-msg"}>
              <strong>{msg.type === "user" ? "You" : "ChillSaathi"}:</strong> {msg.text}
            </p>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type your thoughts..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>

      {/* Mood Tracker */}
      <div className="mood-tracker-panel">
        <h2>🌤️ Mood Tracker</h2>
        <div className="mood-options">
          {moods.map((mood, index) => (
            <button
              key={index}
              className={`mood-btn ${selectedMood === mood.label ? "selected" : ""}`}
              style={{ backgroundColor: selectedMood === mood.label ? mood.color : "#f1f2f6" }}
              onClick={() => handleMoodSelect(mood)}
            >
              <span className="emoji">{mood.emoji}</span>
              <span className="label">{mood.label}</span>
            </button>
          ))}
        </div>

        {moodInfo && (
          <div className="mood-feedback" style={{ backgroundColor: moodInfo.color }}>
            <h4>{moodInfo.emoji} {moodInfo.label}</h4>
            <p>{moodInfo.message}</p>
          </div>
        )}

        <div className="mood-history">
          <h3>📜 Your Mood History</h3>
          <ul>
            {history.length === 0 ? (
              <li>No moods recorded yet.</li>
            ) : (
              history.map((entry, i) => (
                <li key={i}>
                  {entry.emoji} {entry.mood} — <span>{entry.timestamp}</span>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ChatMoodPage;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
