import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './App.css';
import ResearchForm from './components/ResearchForm';
import ResearchProgress from './components/ResearchProgress';
import ResearchResults from './components/ResearchResults';

const queryClient = new QueryClient();

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleReset = () => {
    setSessionId(null);
    setShowResults(false);
  };

  const currentScreen = !sessionId ? 'form' : !showResults ? 'progress' : 'results';

  return (
    <QueryClientProvider client={queryClient}>
      <div className="app">

        {/* ── Top nav ── */}
        <nav className="app-nav">
          <a className="nav-brand" href="/">
            <div className="nav-brand-icon">🔬</div>
            <span className="nav-brand-text">Deep<span>Research</span></span>
          </a>
          <div className="nav-pill">v1.0</div>
        </nav>

        {/* ── Main content ── */}
        <main className="app-main">
          <div className="screen-container screen-enter" key={currentScreen}>
            {currentScreen === 'form' && (
              <ResearchForm onSessionStart={setSessionId} />
            )}
            {currentScreen === 'progress' && (
              <ResearchProgress
                sessionId={sessionId}
                onComplete={() => setShowResults(true)}
                onReset={handleReset}
              />
            )}
            {currentScreen === 'results' && (
              <ResearchResults
                sessionId={sessionId}
                onReset={handleReset}
              />
            )}
          </div>
        </main>

        {/* ── Footer ── */}
        <footer className="app-footer">
          Powered by <span>&nbsp;LangGraph + Ollama&nbsp;</span> · Autonomous AI Research
        </footer>

      </div>
    </QueryClientProvider>
  );
}

export default App;
