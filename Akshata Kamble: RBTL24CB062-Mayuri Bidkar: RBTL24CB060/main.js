let selectedTheme = 'Adventure';

function $(id){ return document.getElementById(id); }

window.addEventListener('DOMContentLoaded', () => {
  // UI theme toggle (light/dark)
  const toggle = document.getElementById('themeToggle');
  const applyTheme = (mode) => {
    const b = document.body;
    if (mode === 'dark') {
      b.classList.add('theme-dark');
      if (toggle) toggle.textContent = '☀️ Light';
    } else {
      b.classList.remove('theme-dark');
      if (toggle) toggle.textContent = '🌙 Dark';
    }
  };
  try {
    const saved = localStorage.getItem('uiTheme');
    applyTheme(saved === 'dark' ? 'dark' : 'light');
  } catch {}
  if (toggle) {
    toggle.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('theme-dark');
      const mode = isDark ? 'dark' : 'light';
      try { localStorage.setItem('uiTheme', mode); } catch {}
      applyTheme(mode);
    });
  }
  // Theme selection
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      selectedTheme = btn.dataset.theme;
      const span = document.querySelector('#selectedTheme');
      if (span) span.textContent = selectedTheme;
      document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // Mic / SpeechRecognition
  const micBtn = $('micBtn');
  if (micBtn) {
    let recognizing = false;
    let recognition;
    if ('webkitSpeechRecognition' in window) {
      recognition = new webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        $('wordsInput').value = transcript;
      };
      recognition.onend = () => { recognizing = false; micBtn.classList.remove('btn-danger'); };
      micBtn.addEventListener('click', () => {
        if (recognizing) { recognition.stop(); return; }
        recognizing = true;
        micBtn.classList.add('btn-danger');
        recognition.start();
      });
    } else {
      micBtn.disabled = true;
      micBtn.title = 'SpeechRecognition not supported on this browser';
    }
  }

  // Background music removed per request

  // Generate story
  const genBtn = $('genBtn');
  if (genBtn) {
    genBtn.addEventListener('click', async () => {
      const raw = $('wordsInput').value.trim();
      if (!raw) { alert('Please enter 2–5 words.'); return; }
      // Normalize: split by commas or spaces, de-duplicate case-insensitively, keep order
      const tokens = raw
        .split(/[\s,]+/)
        .map(w => w.trim())
        .filter(Boolean);
      const uniq = [];
      const seen = new Set();
      for (const t of tokens) {
        const k = t.toLowerCase();
        if (!seen.has(k)) { seen.add(k); uniq.push(t); }
      }
      if (uniq.length < 2 || uniq.length > 5) {
        alert('Please provide 2–5 distinct keywords. Example: "dragon, moon" or "compass river lantern star"');
        return;
      }
      const words = uniq.join(', ');
      // Stop any ongoing speech
      try { speechSynthesis.cancel(); } catch {}
      $('loading').classList.remove('d-none');
      const loader = $('loading');
      if (loader) loader.querySelector('div:last-child').textContent = '🪄 Creating your magical story… please wait';
      $('storyCard').classList.add('d-none');
      try {
        const res = await fetch('/generate_story', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ words, theme: selectedTheme })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed');
        $('storyText').textContent = data.story;
        $('storyCard').classList.remove('d-none');
        $('saveBtn').onclick = () => saveStory(data.story, data.theme, data.words);
        $('readBtn').onclick = () => readAloud(data.story);
      } catch (e) {
        alert(e.message || 'Oops! Could not generate story. Please try again in a moment.');
      } finally {
        $('loading').classList.add('d-none');
      }
    });
  }

  // Delete saved story (on My Stories page)
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.getAttribute('data-id');
      if (!id) return;
      if (!confirm('Delete this story?')) return;
      try {
        const res = await fetch(`/delete_story/${id}`, { method: 'POST' });
        const data = await res.json();
        if (data && data.ok) {
          const card = document.getElementById(`story-card-${id}`);
          if (card) card.remove();
        } else {
          alert('Could not delete story.');
        }
      } catch {
        alert('Could not delete story.');
      }
    });
  });
});

function readAloud(text) {
  try {
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1.05; utter.pitch = 1.02;
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
  } catch {}
}

async function saveStory(content, theme, words){
  try {
    const res = await fetch('/save_story', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, theme, words })
    });
    const data = await res.json();
    if (data.ok) alert('Story saved! Find it under My Stories.');
    else alert('Could not save story.');
  } catch { alert('Could not save story.'); }
}
