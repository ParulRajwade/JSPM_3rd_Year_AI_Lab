<<<<<<< HEAD
import mongoose from "mongoose";
const moodSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  mood: String,
  note: String,
  date: { type: Date, default: Date.now },
});
export default mongoose.model("Mood", moodSchema);
=======
import mongoose from "mongoose";
const moodSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  mood: String,
  note: String,
  date: { type: Date, default: Date.now },
});
export default mongoose.model("Mood", moodSchema);
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
