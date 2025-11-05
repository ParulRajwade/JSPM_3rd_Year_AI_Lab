<<<<<<< HEAD
import React, { useEffect, useState } from 'react';
import './meditation.css';

const Meditation = () => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    setSessions([
      {
        title: 'Mindfulness Meditation',
        description: 'Focus on your breath and allow thoughts to pass without judgment.',
        duration: '10 minutes',
           videolink: "https://www.youtube.com/watch?v=ZToicYcHIOU",
        type: 'Breathing',
      },
      {
        title: 'Guided Relaxation',
        description: 'Listen to a calming voice as you unwind your stress.',
        duration: '15 minutes',
          videolink: 'https://www.youtube.com/watch?v=Jyy0ra2WcQQ',
        type: 'Guided',
      },
      {
        title: 'Yoga Nidra',
        description: 'Deep relaxation for both body and mind, usually practiced lying down.',
        duration: '20 minutes',
           videolink: 'https://www.youtube.com/watch?v=QF1si6HnsFY',
        type: 'Yoga-Based',
      },
      {
        title: 'Loving-Kindness Meditation',
        description: 'Cultivate compassion by silently repeating phrases of goodwill.',
        duration: '12 minutes',
         videolink: 'https://www.youtube.com/watch?v=tY3NnodM3Ww',
        type: 'Emotional Healing',
      },
      {
        title: 'Daily Affirmations',
        description: 'Start your day with positivity and affirmations.',
        duration: '5 minutes',
           videolink: 'https://www.youtube.com/watch?v=efZFARmGyMs',
        type: 'Affirmation'
      },
      {
        title: 'Evening Wind-Down',
        description: 'Relax your body and mind before bedtime.',
        duration: '12 minutes',
        videolink: 'https://www.youtube.com/watch?v=_3fvhTO3pLM',
        type: 'Sleep Preparation'
      }
    ]);
  }, []);

  const handlePlayClick = (link) => {
    window.open(link, '_blank');
  };

  return (
    <div className="meditation-page">
      <h1>Meditation & Wellness</h1>
      <p>Explore calming meditation techniques and yoga for your mind and soul.</p>

      {/* Meditation Sessions Group 1 */}
      <section className="session-list">
        {sessions.slice(0, 3).map((s, i) => (
          <div key={i} className="session-card">
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <p><strong>Duration:</strong> {s.duration}</p>
            <p><strong>Type:</strong> {s.type}</p>
            <button onClick={() => handlePlayClick(s.videolink)} className="play-btn">
              ▶️ Play Session
            </button>
          </div>
        ))}
      </section>

      {/* Meditation Sessions Group 2 */}
      <section className="session-list">
        {sessions.slice(3).map((s, i) => (
          <div key={i + 3} className="session-card">
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <p><strong>Duration:</strong> {s.duration}</p>
            <p><strong>Type:</strong> {s.type}</p>
            <button onClick={() => handlePlayClick(s.videolink)} className="play-btn">
              ▶️ Play Session
            </button>
          </div>
        ))}
      </section>

      {/* Benefits of Meditation */}
      <section className="benefits">
        <h2>🧠 Benefits of Meditation</h2>
        <ul>
          <li>Reduces stress and anxiety</li>
          <li>Improves concentration and focus</li>
          <li>Enhances self-awareness and emotional health</li>
          <li>Improves sleep and overall well-being</li>
          <li>Boosts creativity and mindfulness</li>
        </ul>
      </section>

      {/* Types of Meditation */}
      <section className="types">
        <h2>🧘‍♂️ Types of Meditation</h2>
        <div className="type-grid">
          <div className="type-card">Mindfulness</div>
          <div className="type-card">Guided</div>
          <div className="type-card">Mantra</div>
          <div className="type-card">Movement/Yoga</div>
          <div className="type-card">Loving-Kindness</div>
          <div className="type-card">Visualization</div>
        </div>
      </section>

      {/* Yoga & Breathing Techniques */}
      <section className="yoga-breathing">
        <h2>🌿 Yoga & Breathing Techniques</h2>
        <p>Try these calming practices:</p>
        <ul>
          <li>Alternate Nostril Breathing (Nadi Shodhana)</li>
          <li>4-7-8 Breathing for sleep</li>
          <li>Basic Pranayama (deep belly breathing)</li>
          <li>Cat-Cow Pose to awaken the spine</li>
          <li>Child's Pose for full-body relaxation</li>
        </ul>
      </section>
    </div>
  );
};

export default Meditation; 

=======
import React, { useEffect, useState } from 'react';
import './meditation.css';

const Meditation = () => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    setSessions([
      {
        title: 'Mindfulness Meditation',
        description: 'Focus on your breath and allow thoughts to pass without judgment.',
        duration: '10 minutes',
           videolink: "https://www.youtube.com/watch?v=ZToicYcHIOU",
        type: 'Breathing',
      },
      {
        title: 'Guided Relaxation',
        description: 'Listen to a calming voice as you unwind your stress.',
        duration: '15 minutes',
          videolink: 'https://www.youtube.com/watch?v=Jyy0ra2WcQQ',
        type: 'Guided',
      },
      {
        title: 'Yoga Nidra',
        description: 'Deep relaxation for both body and mind, usually practiced lying down.',
        duration: '20 minutes',
           videolink: 'https://www.youtube.com/watch?v=QF1si6HnsFY',
        type: 'Yoga-Based',
      },
      {
        title: 'Loving-Kindness Meditation',
        description: 'Cultivate compassion by silently repeating phrases of goodwill.',
        duration: '12 minutes',
         videolink: 'https://www.youtube.com/watch?v=tY3NnodM3Ww',
        type: 'Emotional Healing',
      },
      {
        title: 'Daily Affirmations',
        description: 'Start your day with positivity and affirmations.',
        duration: '5 minutes',
           videolink: 'https://www.youtube.com/watch?v=efZFARmGyMs',
        type: 'Affirmation'
      },
      {
        title: 'Evening Wind-Down',
        description: 'Relax your body and mind before bedtime.',
        duration: '12 minutes',
        videolink: 'https://www.youtube.com/watch?v=_3fvhTO3pLM',
        type: 'Sleep Preparation'
      }
    ]);
  }, []);

  const handlePlayClick = (link) => {
    window.open(link, '_blank');
  };

  return (
    <div className="meditation-page">
      <h1>Meditation & Wellness</h1>
      <p>Explore calming meditation techniques and yoga for your mind and soul.</p>

      {/* Meditation Sessions Group 1 */}
      <section className="session-list">
        {sessions.slice(0, 3).map((s, i) => (
          <div key={i} className="session-card">
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <p><strong>Duration:</strong> {s.duration}</p>
            <p><strong>Type:</strong> {s.type}</p>
            <button onClick={() => handlePlayClick(s.videolink)} className="play-btn">
              ▶️ Play Session
            </button>
          </div>
        ))}
      </section>

      {/* Meditation Sessions Group 2 */}
      <section className="session-list">
        {sessions.slice(3).map((s, i) => (
          <div key={i + 3} className="session-card">
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <p><strong>Duration:</strong> {s.duration}</p>
            <p><strong>Type:</strong> {s.type}</p>
            <button onClick={() => handlePlayClick(s.videolink)} className="play-btn">
              ▶️ Play Session
            </button>
          </div>
        ))}
      </section>

      {/* Benefits of Meditation */}
      <section className="benefits">
        <h2>🧠 Benefits of Meditation</h2>
        <ul>
          <li>Reduces stress and anxiety</li>
          <li>Improves concentration and focus</li>
          <li>Enhances self-awareness and emotional health</li>
          <li>Improves sleep and overall well-being</li>
          <li>Boosts creativity and mindfulness</li>
        </ul>
      </section>

      {/* Types of Meditation */}
      <section className="types">
        <h2>🧘‍♂️ Types of Meditation</h2>
        <div className="type-grid">
          <div className="type-card">Mindfulness</div>
          <div className="type-card">Guided</div>
          <div className="type-card">Mantra</div>
          <div className="type-card">Movement/Yoga</div>
          <div className="type-card">Loving-Kindness</div>
          <div className="type-card">Visualization</div>
        </div>
      </section>

      {/* Yoga & Breathing Techniques */}
      <section className="yoga-breathing">
        <h2>🌿 Yoga & Breathing Techniques</h2>
        <p>Try these calming practices:</p>
        <ul>
          <li>Alternate Nostril Breathing (Nadi Shodhana)</li>
          <li>4-7-8 Breathing for sleep</li>
          <li>Basic Pranayama (deep belly breathing)</li>
          <li>Cat-Cow Pose to awaken the spine</li>
          <li>Child's Pose for full-body relaxation</li>
        </ul>
      </section>
    </div>
  );
};

export default Meditation; 

>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
