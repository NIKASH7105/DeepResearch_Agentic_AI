import { useState, useEffect, useRef } from 'react';
import { Search, Zap, BookOpen, Layers } from 'lucide-react';
import { researchApi } from '../services/api';

const EXAMPLE_QUERIES = [
  'What is the impact of generative AI on university education?',
  'How does quantum computing affect modern cryptography?',
  'Latest breakthroughs in mRNA vaccine technology',
  'Economic effects of remote work on urban real estate',
  'The future of nuclear fusion energy by 2035',
];

const DEPTH_OPTIONS = [
  {
    id: 'quick',
    icon: <Zap size={18} />,
    label: 'Quick',
    desc: '3–5 sources',
    sub: 'Basic synthesis',
    color: 'var(--amber)',
    colorBg: 'rgba(245,158,11,0.08)',
    colorBorder: 'rgba(245,158,11,0.25)',
  },
  {
    id: 'standard',
    icon: <Search size={18} />,
    label: 'Standard',
    desc: '8–15 sources',
    sub: 'Thorough analysis',
    color: 'var(--indigo)',
    colorBg: 'rgba(99,102,241,0.1)',
    colorBorder: 'rgba(99,102,241,0.3)',
  },
  {
    id: 'deep',
    icon: <Layers size={18} />,
    label: 'Deep',
    desc: '15+ sources',
    sub: 'Comprehensive',
    color: 'var(--violet)',
    colorBg: 'rgba(139,92,246,0.1)',
    colorBorder: 'rgba(139,92,246,0.3)',
  },
];

function ResearchForm({ onSessionStart }) {
  const [query, setQuery] = useState('');
  const [depth, setDepth] = useState('standard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [placeholderIdx, setPlaceholderIdx] = useState(0);
  const [charCount, setCharCount] = useState(0);
  const textareaRef = useRef(null);

  // Cycle placeholder text
  useEffect(() => {
    if (query) return;
    const id = setInterval(() => {
      setPlaceholderIdx(i => (i + 1) % EXAMPLE_QUERIES.length);
    }, 3000);
    return () => clearInterval(id);
  }, [query]);

  const handleTextChange = (e) => {
    setQuery(e.target.value);
    setCharCount(e.target.value.length);
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Drop a question in there first.');
      textareaRef.current?.focus();
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await researchApi.startResearch({
        query: query.trim(),
        research_depth: depth,
      });
      onSessionStart(response.session_id);
    } catch (err) {
      console.error('Error starting research:', err);
      setError(err.response?.data?.detail || 'Could not connect to backend. Make sure it\'s running.');
    } finally {
      setLoading(false);
    }
  };

  const selectedDepth = DEPTH_OPTIONS.find(d => d.id === depth);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

      {/* ── Hero heading ── */}
      <div style={{ paddingLeft: '2px' }}>
        <p style={{
          fontSize: '0.72rem',
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: 'var(--indigo)',
          marginBottom: '0.6rem',
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
        }}>
          <span style={{ display: 'inline-block', width: 18, height: 1, background: 'var(--indigo)', verticalAlign: 'middle' }} />
          Autonomous Research Agent
        </p>
        <h1 style={{
          fontSize: 'clamp(1.8rem, 5vw, 2.6rem)',
          fontWeight: 800,
          letterSpacing: '-0.03em',
          color: 'var(--text-bright)',
          lineHeight: 1.1,
        }}>
          Ask anything.<br />
          <span style={{
            background: 'linear-gradient(120deg, var(--indigo) 0%, var(--violet) 50%, var(--cyan) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            Get real answers.
          </span>
        </h1>
        <p style={{ color: 'var(--text-mid)', marginTop: '0.75rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
          The agent searches, reads, verifies, and synthesizes — then hands you a citable report.
        </p>
      </div>

      {/* ── Main card ── */}
      <div className="card">

        <form onSubmit={handleSubmit}>

          {/* Query textarea */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label className="field-label" htmlFor="query">Your question or topic</label>
            <div style={{ position: 'relative' }}>
              <textarea
                id="query"
                ref={textareaRef}
                className="field-textarea"
                value={query}
                onChange={handleTextChange}
                placeholder={EXAMPLE_QUERIES[placeholderIdx]}
                rows={4}
                maxLength={2000}
                style={{ paddingBottom: '2.2rem' }}
              />
              <span style={{
                position: 'absolute',
                bottom: '0.65rem',
                right: '0.85rem',
                fontSize: '0.72rem',
                color: charCount > 1800 ? 'var(--rose)' : 'var(--text-dim)',
                fontFamily: 'var(--font-mono)',
                pointerEvents: 'none',
              }}>
                {charCount}/2000
              </span>
            </div>
          </div>

          {/* Depth selector */}
          <div style={{ marginBottom: '1.75rem' }}>
            <label className="field-label">Research depth</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.65rem' }}>
              {DEPTH_OPTIONS.map(opt => (
                <button
                  key={opt.id}
                  type="button"
                  id={`depth-${opt.id}`}
                  onClick={() => setDepth(opt.id)}
                  style={{
                    padding: '0.85rem 0.75rem',
                    borderRadius: '12px',
                    border: `1px solid ${depth === opt.id ? opt.colorBorder : 'var(--border-faint)'}`,
                    background: depth === opt.id ? opt.colorBg : 'rgba(10,13,26,0.5)',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '4px',
                  }}
                >
                  <span style={{
                    color: depth === opt.id ? opt.color : 'var(--text-dim)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px',
                    marginBottom: '2px',
                    transition: 'color 0.2s',
                  }}>
                    {opt.icon}
                    <span style={{ fontSize: '0.8rem', fontWeight: 700, color: depth === opt.id ? opt.color : 'var(--text-bright)', letterSpacing: '-0.01em' }}>
                      {opt.label}
                    </span>
                  </span>
                  <span style={{ fontSize: '0.72rem', color: depth === opt.id ? opt.color : 'var(--text-dim)', fontWeight: 600 }}>
                    {opt.desc}
                  </span>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>
                    {opt.sub}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="error-banner" style={{ marginBottom: '1rem' }}>
              <span>⚠</span> {error}
            </div>
          )}

          {/* Submit */}
          <button
            id="submit-research"
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', padding: '0.85rem', fontSize: '0.95rem', letterSpacing: '-0.01em', borderRadius: '12px' }}
          >
            {loading ? (
              <>
                <span style={{ width: 18, height: 18, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'spin 0.7s linear infinite', display: 'inline-block' }} />
                Initializing agent…
              </>
            ) : (
              <>
                <Search size={17} />
                Run Research
              </>
            )}
          </button>

        </form>
      </div>

      {/* ── How it works — horizontal steps ── */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(5, 1fr)',
        gap: '0.4rem',
      }}>
        {[
          { n: '01', label: 'Plan' },
          { n: '02', label: 'Search' },
          { n: '03', label: 'Extract' },
          { n: '04', label: 'Verify' },
          { n: '05', label: 'Report' },
        ].map((step, i) => (
          <div key={i} style={{
            textAlign: 'center',
            padding: '0.75rem 0.4rem',
            borderRadius: '10px',
            background: 'rgba(20,25,41,0.4)',
            border: '1px solid var(--border-faint)',
          }}>
            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              color: 'var(--indigo)',
              marginBottom: '4px',
              fontWeight: 600,
            }}>
              {step.n}
            </div>
            <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-mid)', letterSpacing: '0.02em' }}>
              {step.label}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

export default ResearchForm;
