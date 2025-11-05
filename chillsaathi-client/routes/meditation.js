<<<<<<< HEAD
import express from "express";
import Meditation from "../models/Meditation.js";
const router = express.Router();

router.get("/", async (req, res) => {
  const list = await Meditation.find();
  res.json(list);
});

router.post("/", async (req, res) => {
  const { title, description, url } = req.body;
  const m = await Meditation.create({ title, description, url });
  res.json(m);
});

export default router;
=======
import express from "express";
import Meditation from "../models/Meditation.js";
const router = express.Router();

router.get("/", async (req, res) => {
  const list = await Meditation.find();
  res.json(list);
});

router.post("/", async (req, res) => {
  const { title, description, url } = req.body;
  const m = await Meditation.create({ title, description, url });
  res.json(m);
});

export default router;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
