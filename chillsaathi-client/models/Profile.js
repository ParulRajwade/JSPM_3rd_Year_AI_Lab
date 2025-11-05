<<<<<<< HEAD
import mongoose from "mongoose";
const profileSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  age: Number,
  gender: String,
  interests: String,
});
export default mongoose.model("Profile", profileSchema);
=======
import mongoose from "mongoose";
const profileSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  age: Number,
  gender: String,
  interests: String,
});
export default mongoose.model("Profile", profileSchema);
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
