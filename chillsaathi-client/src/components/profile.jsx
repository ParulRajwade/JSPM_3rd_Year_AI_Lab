<<<<<<< HEAD
import React, { useState } from "react";
import "./profile.css";

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);

  // Profile state
  const [name, setName] = useState("Chinmay Deshmukh");
  const [email, setEmail] = useState("chinmay@example.com");
  const [mood, setMood] = useState("Happy");
  const [bio, setBio] = useState("Passionate about mental wellness.");
  const [image, setImage] = useState(null);

  // Additional info
  const [age, setAge] = useState("21");
  const [gender, setGender] = useState("Male");
  const [location, setLocation] = useState("Pune, India");
  const [interests, setInterests] = useState("Yoga, Music, Journaling");
  const [memberSince, setMemberSince] = useState("March 2024");

  const handleSave = (e) => {
    e.preventDefault();
    alert("Profile updated successfully!");
    setIsEditing(false);
  };

  return (
    <div className="profile-container">
      {!isEditing ? (
        <div className="profile-card">
          <img
            src={
              image
                ? URL.createObjectURL(image)
                : "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            }
            alt="User Avatar"
            className="profile-avatar"
          />
          <h2 className="profile-name">{name}</h2>
          <p className="profile-email">{email}</p>

          <div className="profile-stats">
            <div className="stat">
              <h4>📝 Journals</h4>
              <p>15 entries</p>
            </div>
            <div className="stat">
              <h4>📊 Mood Logs</h4>
              <p>28 entries</p>
            </div>
          </div>

          <div className="profile-mood">
            <h4>
              🌈 Current Mood: <span>{mood} 😊</span>
            </h4>
          </div>

          <div className="profile-details">
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Gender:</strong> {gender}</p>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Interests:</strong> {interests}</p>
            <p><strong>Member Since:</strong> {memberSince}</p>
          </div>

          <button className="edit-button" onClick={() => setIsEditing(true)}>
            Edit Profile
          </button>
        </div>
      ) : (
        <form className="edit-profile-form" onSubmit={handleSave}>
          <h2>Edit Your Profile</h2>

          <label>Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Mood</label>
          <select
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            required
          >
            <option value="">Select Mood</option>
            <option value="Happy">😊 Happy</option>
            <option value="Sad">😢 Sad</option>
            <option value="Stressed">😰 Stressed</option>
            <option value="Calm">😌 Calm</option>
          </select>

          <label>Short Bio</label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Write a short bio..."
          />

          <label>Upload Profile Picture</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
          />

          {/* Additional Info */}
          <label>Age</label>
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />

          <label>Gender</label>
          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>

          <label>Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />

          <label>Interests</label>
          <input
            type="text"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            placeholder="e.g., Yoga, Music"
          />

          <label>Member Since</label>
          <input
            type="text"
            value={memberSince}
            onChange={(e) => setMemberSince(e.target.value)}
            disabled
          />

          <button type="submit" className="save-btn">
            Save Changes
          </button>
        </form>
      )}
    </div>
  );
};

export default Profile;

=======
import React, { useState } from "react";
import "./profile.css";

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);

  // Profile state
  const [name, setName] = useState("Chinmay Deshmukh");
  const [email, setEmail] = useState("chinmay@example.com");
  const [mood, setMood] = useState("Happy");
  const [bio, setBio] = useState("Passionate about mental wellness.");
  const [image, setImage] = useState(null);

  // Additional info
  const [age, setAge] = useState("21");
  const [gender, setGender] = useState("Male");
  const [location, setLocation] = useState("Pune, India");
  const [interests, setInterests] = useState("Yoga, Music, Journaling");
  const [memberSince, setMemberSince] = useState("March 2024");

  const handleSave = (e) => {
    e.preventDefault();
    alert("Profile updated successfully!");
    setIsEditing(false);
  };

  return (
    <div className="profile-container">
      {!isEditing ? (
        <div className="profile-card">
          <img
            src={
              image
                ? URL.createObjectURL(image)
                : "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            }
            alt="User Avatar"
            className="profile-avatar"
          />
          <h2 className="profile-name">{name}</h2>
          <p className="profile-email">{email}</p>

          <div className="profile-stats">
            <div className="stat">
              <h4>📝 Journals</h4>
              <p>15 entries</p>
            </div>
            <div className="stat">
              <h4>📊 Mood Logs</h4>
              <p>28 entries</p>
            </div>
          </div>

          <div className="profile-mood">
            <h4>
              🌈 Current Mood: <span>{mood} 😊</span>
            </h4>
          </div>

          <div className="profile-details">
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Gender:</strong> {gender}</p>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Interests:</strong> {interests}</p>
            <p><strong>Member Since:</strong> {memberSince}</p>
          </div>

          <button className="edit-button" onClick={() => setIsEditing(true)}>
            Edit Profile
          </button>
        </div>
      ) : (
        <form className="edit-profile-form" onSubmit={handleSave}>
          <h2>Edit Your Profile</h2>

          <label>Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Mood</label>
          <select
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            required
          >
            <option value="">Select Mood</option>
            <option value="Happy">😊 Happy</option>
            <option value="Sad">😢 Sad</option>
            <option value="Stressed">😰 Stressed</option>
            <option value="Calm">😌 Calm</option>
          </select>

          <label>Short Bio</label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Write a short bio..."
          />

          <label>Upload Profile Picture</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
          />

          {/* Additional Info */}
          <label>Age</label>
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />

          <label>Gender</label>
          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>

          <label>Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />

          <label>Interests</label>
          <input
            type="text"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            placeholder="e.g., Yoga, Music"
          />

          <label>Member Since</label>
          <input
            type="text"
            value={memberSince}
            onChange={(e) => setMemberSince(e.target.value)}
            disabled
          />

          <button type="submit" className="save-btn">
            Save Changes
          </button>
        </form>
      )}
    </div>
  );
};

export default Profile;

>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
