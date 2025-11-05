<<<<<<< HEAD
import mongoose from "mongoose";

const journalSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  entry: String,
  date: { type: Date, default: Date.now },
});

export default mongoose.model("Journal", journalSchema);
=======
import mongoose from "mongoose";

const journalSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  entry: String,
  date: { type: Date, default: Date.now },
});

export default mongoose.model("Journal", journalSchema);
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
