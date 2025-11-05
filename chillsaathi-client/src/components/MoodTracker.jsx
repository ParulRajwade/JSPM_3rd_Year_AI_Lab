<<<<<<< HEAD
import React, { useState, useEffect } from "react";
import "./MoodTracker.css";

const moods = [
  { emoji: "😊", label: "Happy" },
  { emoji: "😐", label: "Neutral" },
  { emoji: "😢", label: "Sad" },
  { emoji: "😡", label: "Angry" },
  { emoji: "😍", label: "Loved" },
];

function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState(null);
  const [history, setHistory] = useState([]);

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
    const newHistory = [entry, ...history.slice(0, 9)]; // Keep max 10 entries
    setHistory(newHistory);
    localStorage.setItem("moodHistory", JSON.stringify(newHistory));
    setSelectedMood(mood.label);
  };

  return (
    <div className="mood-tracker fade-in">
      <h2>🌤️ How's your mood today?</h2>
      <div className="mood-options">
        {moods.map((mood, index) => (
          <button
            key={index}
            className={`mood-btn ${selectedMood === mood.label ? "selected" : ""}`}
            onClick={() => handleMoodSelect(mood)}
          >
            {mood.emoji}
            <span>{mood.label}</span>
          </button>
        ))}
      </div>

      <div className="mood-history">
        <h3>📜 Mood History</h3>
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
  );
}

export default MoodTracker;
=======
import React, { useState, useEffect } from "react";
import "./MoodTracker.css";

const moods = [
  { emoji: "😊", label: "Happy" },
  { emoji: "😐", label: "Neutral" },
  { emoji: "😢", label: "Sad" },
  { emoji: "😡", label: "Angry" },
  { emoji: "😍", label: "Loved" },
];

function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState(null);
  const [history, setHistory] = useState([]);

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
    const newHistory = [entry, ...history.slice(0, 9)]; // Keep max 10 entries
    setHistory(newHistory);
    localStorage.setItem("moodHistory", JSON.stringify(newHistory));
    setSelectedMood(mood.label);
  };

  return (
    <div className="mood-tracker fade-in">
      <h2>🌤️ How's your mood today?</h2>
      <div className="mood-options">
        {moods.map((mood, index) => (
          <button
            key={index}
            className={`mood-btn ${selectedMood === mood.label ? "selected" : ""}`}
            onClick={() => handleMoodSelect(mood)}
          >
            {mood.emoji}
            <span>{mood.label}</span>
          </button>
        ))}
      </div>

      <div className="mood-history">
        <h3>📜 Mood History</h3>
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
  );
}

export default MoodTracker;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
