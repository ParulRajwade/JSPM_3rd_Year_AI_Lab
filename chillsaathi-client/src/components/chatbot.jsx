<<<<<<< HEAD
import React, { useState } from "react";
import "./chatbot.css";

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const botMessage = { type: "bot", text: data.reply };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: "bot", text: "❌ Server error" },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chatbot-container">
      <div className="chatbox fade-in">
        <h2>💬 How are you feeling today?</h2>
        <div id="chat">
          {messages.map((msg, index) => (
            <p
              key={index}
              className={msg.type === "user" ? "user-msg" : "bot-msg"}
            >
              <strong>
                {msg.type === "user" ? "You" : "ChillSaathi"}:
              </strong>{" "}
              {msg.text}
            </p>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chatbox;
=======
import React, { useState } from "react";
import "./chatbot.css";

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const botMessage = { type: "bot", text: data.reply };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: "bot", text: "❌ Server error" },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chatbot-container">
      <div className="chatbox fade-in">
        <h2>💬 How are you feeling today?</h2>
        <div id="chat">
          {messages.map((msg, index) => (
            <p
              key={index}
              className={msg.type === "user" ? "user-msg" : "bot-msg"}
            >
              <strong>
                {msg.type === "user" ? "You" : "ChillSaathi"}:
              </strong>{" "}
              {msg.text}
            </p>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chatbox;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
