
// server.js
import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";

// Routes
import authRoutes from "./routes/auth.js";
import journalRoutes from "./routes/journal.js";
import moodRoutes from "./routes/mood.js";
import profileRoutes from "./routes/Profile.js";
import meditationRoutes from "./routes/meditation.js";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("✅ MongoDB connected"))
.catch((err) => console.error("❌ MongoDB connection error:", err));
// Gemini API Check
if (!process.env.GEMINI_API_KEY) {
  console.error("❌ Missing GEMINI_API_KEY in .env");
  process.exit(1);
}
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// 📌 Chatbot Route
app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(userMessage);
    const text = await result.response.text();
    res.json({ reply: text });
  } catch (error) {
    console.error("❌ Gemini API Error:", error);
    res.status(500).json({ reply: "Error generating response." });
  }
});

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/journal", journalRoutes);
app.use("/api/mood", moodRoutes);
app.use("/api/profile", profileRoutes);
app.use("/api/meditations", meditationRoutes);



app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});

// server.js
import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";

// Routes
import authRoutes from "./routes/auth.js";
import journalRoutes from "./routes/journal.js";
import moodRoutes from "./routes/mood.js";
import profileRoutes from "./routes/Profile.js";
import meditationRoutes from "./routes/meditation.js";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("✅ MongoDB connected"))
.catch((err) => console.error("❌ MongoDB connection error:", err));
// Gemini API Check
if (!process.env.GEMINI_API_KEY) {
  console.error("❌ Missing GEMINI_API_KEY in .env");
  process.exit(1);
}
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// 📌 Chatbot Route
app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(userMessage);
    const text = await result.response.text();
    res.json({ reply: text });
  } catch (error) {
    console.error("❌ Gemini API Error:", error);
    res.status(500).json({ reply: "Error generating response." });
  }
});

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/journal", journalRoutes);
app.use("/api/mood", moodRoutes);
app.use("/api/profile", profileRoutes);
app.use("/api/meditations", meditationRoutes);



app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});

