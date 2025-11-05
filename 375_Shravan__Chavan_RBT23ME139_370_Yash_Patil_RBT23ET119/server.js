// server.js
import express from "express";
import fetch from "node-fetch";
import dotenv from "dotenv";
dotenv.config();

const app = express();
app.use(express.json());
app.use(express.static("public")); // to serve your HTML/CSS/JS

// 🧠 AI Chat Route
app.post("/api/chat", async (req, res) => {
  const userMessage = req.body.message;

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini", // fast + smart model
        messages: [
          {
            role: "system",
            content:
              "You are a certified fitness and workout planner AI. Answer user questions about gym, exercises, diet, supplements, and recovery with accurate, motivating, and simple explanations.",
          },
          { role: "user", content: userMessage },
        ],
      }),
    });

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content?.trim() || "Sorry, I couldn’t generate a reply.";

    res.json({ reply });
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ reply: "Error connecting to AI server." });
  }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => console.log(`🤖 AI Chatbot running at http://localhost:${PORT}`));
