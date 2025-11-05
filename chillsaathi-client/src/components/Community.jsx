<<<<<<< HEAD
import React, { useEffect, useState } from 'react';
import './community.css';

const Community = () => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    setResources([
      {
        name: 'Calm',
        description: 'A leading app for sleep, meditation, and relaxation.',
        link: 'https://www.calm.com',
        logo: 'https://logo.clearbit.com/calm.com'
      },
      {
        name: 'Headspace',
        description: 'Mindfulness and meditation made simple.',
        link: 'https://www.headspace.com',
        logo: 'https://logo.clearbit.com/headspace.com'
      },
      {
        name: 'Sadhguru - YouTube',
        description: 'Guided meditations and talks from the Isha Foundation.',
        link: 'https://www.youtube.com/@sadhguru',
        logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/8/89/YouTube_logo_2017.svg/2560px-YouTube_logo_2017.svg.png'
      },
      {
        name: 'Insight Timer',
        description: 'Free guided meditations and mindfulness courses.',
        link: 'https://www.insighttimer.com',
        logo: 'https://logo.clearbit.com/insighttimer.com'
      },
      {
        name: 'Smiling Mind',
        description: 'Free mindfulness app developed by psychologists.',
        link: 'https://www.smilingmind.com.au',
        logo: 'https://logo.clearbit.com/smilingmind.com.au'
      },
      {
        name: 'Breethe',
        description: 'Meditation app to reduce stress, sleep better, and feel happier.',
        link: 'https://breethe.com',
        logo: 'https://logo.clearbit.com/breethe.com'
      },
      {
        name: 'Ten Percent Happier',
        description: 'Meditation for skeptics and mindfulness learners.',
        link: 'https://www.tenpercent.com',
        logo: 'https://logo.clearbit.com/tenpercent.com'
      },
      {
        name: 'The Honest Guys - YouTube',
        description: 'Popular YouTube channel for sleep and relaxation meditations.',
        link: 'https://www.youtube.com/@TheHonestGuys',
        logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/8/89/YouTube_logo_2017.svg/2560px-YouTube_logo_2017.svg.png'
      },
      {
        name: 'Meditation Oasis',
        description: 'Guided meditations for inner peace and mindfulness.',
        link: 'https://www.meditationoasis.com',
        logo: 'https://logo.clearbit.com/meditationoasis.com'
      },
      {
        name: 'MyLife Meditation',
        description: 'Emotional wellness and guided meditation app.',
        link: 'https://my.life',
        logo: 'https://logo.clearbit.com/my.life'
      },
      {
        name: 'Art of Living',
        description: 'Global foundation promoting stress-free living and yoga.',
        link: 'https://www.artofliving.org',
        logo: 'https://logo.clearbit.com/artofliving.org'
      },
      {
        name: 'Mindful.org',
        description: 'Articles and resources for mindfulness and mental health.',
        link: 'https://www.mindful.org',
        logo: 'https://logo.clearbit.com/mindful.org'
      }
    ]);
  }, []);

  return (
    <div className="community-page">
      <h1>Community & Resources</h1>
      <p>Connect with trusted platforms and influencers in the meditation world.</p>

      <div className="resource-list">
        {resources.map((res, i) => (
          <div key={i} className="resource-card">
            <img src={res.logo} alt={`${res.name} logo`} />
            <div>
              <h3>{res.name}</h3>
              <p>{res.description}</p>
              <a href={res.link} target="_blank" rel="noopener noreferrer">Visit Site</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Community;
=======
import React, { useEffect, useState } from 'react';
import './community.css';

const Community = () => {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    setResources([
      {
        name: 'Calm',
        description: 'A leading app for sleep, meditation, and relaxation.',
        link: 'https://www.calm.com',
        logo: 'https://logo.clearbit.com/calm.com'
      },
      {
        name: 'Headspace',
        description: 'Mindfulness and meditation made simple.',
        link: 'https://www.headspace.com',
        logo: 'https://logo.clearbit.com/headspace.com'
      },
      {
        name: 'Sadhguru - YouTube',
        description: 'Guided meditations and talks from the Isha Foundation.',
        link: 'https://www.youtube.com/@sadhguru',
        logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/8/89/YouTube_logo_2017.svg/2560px-YouTube_logo_2017.svg.png'
      },
      {
        name: 'Insight Timer',
        description: 'Free guided meditations and mindfulness courses.',
        link: 'https://www.insighttimer.com',
        logo: 'https://logo.clearbit.com/insighttimer.com'
      },
      {
        name: 'Smiling Mind',
        description: 'Free mindfulness app developed by psychologists.',
        link: 'https://www.smilingmind.com.au',
        logo: 'https://logo.clearbit.com/smilingmind.com.au'
      },
      {
        name: 'Breethe',
        description: 'Meditation app to reduce stress, sleep better, and feel happier.',
        link: 'https://breethe.com',
        logo: 'https://logo.clearbit.com/breethe.com'
      },
      {
        name: 'Ten Percent Happier',
        description: 'Meditation for skeptics and mindfulness learners.',
        link: 'https://www.tenpercent.com',
        logo: 'https://logo.clearbit.com/tenpercent.com'
      },
      {
        name: 'The Honest Guys - YouTube',
        description: 'Popular YouTube channel for sleep and relaxation meditations.',
        link: 'https://www.youtube.com/@TheHonestGuys',
        logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/8/89/YouTube_logo_2017.svg/2560px-YouTube_logo_2017.svg.png'
      },
      {
        name: 'Meditation Oasis',
        description: 'Guided meditations for inner peace and mindfulness.',
        link: 'https://www.meditationoasis.com',
        logo: 'https://logo.clearbit.com/meditationoasis.com'
      },
      {
        name: 'MyLife Meditation',
        description: 'Emotional wellness and guided meditation app.',
        link: 'https://my.life',
        logo: 'https://logo.clearbit.com/my.life'
      },
      {
        name: 'Art of Living',
        description: 'Global foundation promoting stress-free living and yoga.',
        link: 'https://www.artofliving.org',
        logo: 'https://logo.clearbit.com/artofliving.org'
      },
      {
        name: 'Mindful.org',
        description: 'Articles and resources for mindfulness and mental health.',
        link: 'https://www.mindful.org',
        logo: 'https://logo.clearbit.com/mindful.org'
      }
    ]);
  }, []);

  return (
    <div className="community-page">
      <h1>Community & Resources</h1>
      <p>Connect with trusted platforms and influencers in the meditation world.</p>

      <div className="resource-list">
        {resources.map((res, i) => (
          <div key={i} className="resource-card">
            <img src={res.logo} alt={`${res.name} logo`} />
            <div>
              <h3>{res.name}</h3>
              <p>{res.description}</p>
              <a href={res.link} target="_blank" rel="noopener noreferrer">Visit Site</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Community;
>>>>>>> a4fbcb947aecbcc13342cee25c501fb732435def
