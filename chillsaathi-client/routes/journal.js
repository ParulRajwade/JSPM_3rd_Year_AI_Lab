<<<<<<< HEAD
import express from "express";
import jwt from "jsonwebtoken";
import Journal from "../models/Journal.js";
const router = express.Router();
function auth(req, res, next) {
  const token = req.header("Authorization");
  try {
    req.userId = jwt.verify(token, process.env.JWT_SECRET).userId;
    next();
  } catch {
    return res.status(401).json({ error: "Unauthorized" });
  }
}
router.post("/", auth, async (req, res) => {
  const { entry } = req.body;
  const j = await Journal.create({ userId: req.userId, entry });
  res.json(j);
});
router.get("/", auth, async (req, res) => {
  const entries = await Journal.find({ userId: req.userId });
  res.json(entries);
});
export default router;
=======
import express from "express";
import jwt from "jsonwebtoken";
import Journal from "../models/Journal.js";
const router = express.Router();
function auth(req, res, next) {
  const token = req.header("Authorization");
  try {
    req.userId = jwt.verify(token, process.env.JWT_SECRET).userId;
    next();
  } catch {
    return res.status(401).json({ error: "Unauthorized" });
  }
}
router.post("/", auth, async (req, res) => {
  const { entry } = req.body;
  const j = await Journal.create({ userId: req.userId, entry });
  res.json(j);
});
router.get("/", auth, async (req, res) => {
  const entries = await Journal.find({ userId: req.userId });
  res.json(entries);
});
export default router;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
