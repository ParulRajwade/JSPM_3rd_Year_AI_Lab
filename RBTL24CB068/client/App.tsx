
import React, { useState, useCallback, useEffect } from 'react';
import type { Summary, Flashcard, ChatMessage, View } from './types';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import Header from './components/Header';
import { summarizeText, chatWithContext, generateFlashcards, translateText, rephraseText } from './services/geminiService';
import { LockIcon } from './constants';
import { useLocation, useNavigate } from 'react-router-dom';



const App: React.FC = () => {
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    { role: 'model', content: "Hello! I'm TabMind. Add a summary or ask me about your saved tabs." }
  ]);
  const [activeView, setActiveView] = useState<View>('chat');
  const [selectedSummary, setSelectedSummary] = useState<Summary | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<{ id: string; name: string; email: string; role: 'user' | 'admin' } | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  // Load auth from localStorage
  useEffect(() => {
    try {
      const raw = localStorage.getItem('auth');
      if (raw) {
        const parsed = JSON.parse(raw) as { token: string; user: { id: string; name: string; email: string; role: 'user' | 'admin' } };
        if (parsed?.token && parsed?.user) {
          setAuthToken(parsed.token);
          setCurrentUser(parsed.user);
        }
      }
    } catch {}
  }, []);

  useEffect(() => {
    const path = location.pathname;
    if (path === '/login') {
      setActiveView('login');
    } else if (path === '/signup') {
      setActiveView('signup');
    } else if (path === '/flashcards') {
      setActiveView('flashcards');
    } else {
      setActiveView('chat');
    }
  }, [location.pathname]);

  // Route protection
  useEffect(() => {
    const path = location.pathname;
    const isAuthRoute = path === '/login' || path === '/signup';
    if (!currentUser && !isAuthRoute) {
      navigate('/signup', { replace: true });
      return;
    }
    if (currentUser && isAuthRoute) {
      navigate('/', { replace: true });
    }
  }, [location.pathname, currentUser, navigate]);

  const handleSummarize = useCallback(async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const { summary, title } = await summarizeText(text);
      const newSummary: Summary = {
        id: Date.now().toString(),
        title,
        originalContent: text,
        summary,
        timestamp: new Date().toISOString(),
      };
      setSummaries(prev => [newSummary, ...prev]);
      setSelectedSummary(newSummary);
      setActiveView('summary');
    } catch (e) {
      setError('Failed to generate summary. Please try again.');
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSelectSummary = useCallback((summary: Summary) => {
    setSelectedSummary(summary);
    setActiveView('summary');
  }, []);

  const handleChatSubmit = useCallback(async (message: string) => {
    const userMessage: ChatMessage = { role: 'user', content: message };
    setChatHistory(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    try {
      const modelResponse = await chatWithContext([...chatHistory, userMessage], summaries);
      setChatHistory(prev => [...prev, { role: 'model', content: modelResponse }]);
    } catch (e) {
      const errorMessage = 'Failed to get chat response. Please try again.';
      setError(errorMessage);
      setChatHistory(prev => [...prev, { role: 'model', content: `Error: ${errorMessage}` }]);
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }, [chatHistory, summaries]);

  const handleGenerateFlashcards = useCallback(async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const generatedFlashcards = await generateFlashcards(text);
      setFlashcards(generatedFlashcards);
      setActiveView('flashcards');
    } catch (e) {
      setError('Failed to generate flashcards. Please try again.');
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const handleTranslateSummary = useCallback(async (text: string, language: string) => {
      if (!selectedSummary) return;
      setIsLoading(true);
      setError(null);
      try {
          const translatedText = await translateText(text, language);
          const updatedSummary = { ...selectedSummary, summary: translatedText };
          setSelectedSummary(updatedSummary);
          setSummaries(summaries.map(s => s.id === updatedSummary.id ? updatedSummary : s));
      } catch (e) {
          setError('Failed to translate summary. Please try again.');
          console.error(e);
      } finally {
          setIsLoading(false);
      }
  }, [selectedSummary, summaries]);

  const handleRephraseSummary = useCallback(async (text: string, tone: string) => {
      if (!selectedSummary) return;
      setIsLoading(true);
      setError(null);
      try {
          const rephrasedText = await rephraseText(text, tone);
          const updatedSummary = { ...selectedSummary, summary: rephrasedText };
          setSelectedSummary(updatedSummary);
          setSummaries(summaries.map(s => s.id === updatedSummary.id ? updatedSummary : s));
      } catch (e) {
          setError('Failed to rephrase summary. Please try again.');
          console.error(e);
      } finally {
          setIsLoading(false);
      }
  }, [selectedSummary, summaries]);

  const handleAuthSuccess = useCallback((payload: { token: string; user: { id: string; name: string; email: string; role: 'user' | 'admin' } }) => {
      setAuthToken(payload.token);
      setCurrentUser(payload.user);
      try { localStorage.setItem('auth', JSON.stringify(payload)); } catch {}
      navigate('/');
  }, []);

  const handleLogout = useCallback(() => {
      setAuthToken(null);
      setCurrentUser(null);
      try { localStorage.removeItem('auth'); } catch {}
      navigate('/login');
  }, []);


  return (
    <div className="flex flex-col h-screen font-sans bg-gray-900 text-gray-100">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          summaries={summaries}
          onSummarize={handleSummarize}
          onSelectSummary={handleSelectSummary}
          isLoading={isLoading}
          onNavigate={(view: View) => {
            switch (view) {
              case 'login':
                navigate('/login');
                break;
              case 'signup':
                navigate('/signup');
                break;
              case 'flashcards':
                navigate('/flashcards');
                break;
              case 'admin':
                navigate('/admin');
                break;
              default:
                navigate('/');
            }
            setActiveView(view);
          }}
          activeView={activeView}
          currentUser={currentUser}
          onLogout={handleLogout}
        />
        <MainContent
          activeView={activeView}
          chatHistory={chatHistory}
          onChatSubmit={handleChatSubmit}
          selectedSummary={selectedSummary}
          flashcards={flashcards}
          onGenerateFlashcards={handleGenerateFlashcards}
          onTranslate={handleTranslateSummary}
          onRephrase={handleRephraseSummary}
          isLoading={isLoading}
          onAuthSuccess={handleAuthSuccess}
          currentUser={currentUser}
          authToken={authToken}
        />
      </div>
      {error && (
        <div className="absolute bottom-4 right-4 bg-red-500 text-white p-3 rounded-lg shadow-lg">
          {error}
        </div>
      )}
      <footer className="bg-gray-900/50 border-t border-gray-700/50 text-center p-2 text-xs text-gray-400 backdrop-blur-sm">
        <div className="flex items-center justify-center gap-2">
            <LockIcon className="w-4 h-4 text-green-400" />
            <span>Private by Design: All processing is simulated on-device. No data leaves your browser.</span>
        </div>
      </footer>
    </div>
  );
};

export default App;

