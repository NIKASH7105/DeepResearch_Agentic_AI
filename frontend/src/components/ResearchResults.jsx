import { useQuery } from '@tanstack/react-query';
import { RotateCcw, ExternalLink, Globe, ListChecks, Brain, Download } from 'lucide-react';
import { researchApi } from '../services/api';
import { useState } from 'react';

const TABS = [
  { id: 'report',   label: 'Report',       icon: <Globe size={14} /> },
  { id: 'plan',     label: 'Research Plan', icon: <ListChecks size={14} /> },
  { id: 'log',      label: 'Agent Log',    icon: <Brain size={14} /> },
  { id: 'sources',  label: 'Sources',      icon: <ExternalLink size={14} /> },
];

function LogLine({ line, idx }) {
  const isToolLine = line.includes('TOOL:');
  const isSuccess  = line.includes('✓') || line.includes('✔');
  const isWarning  = line.includes('⚠') || line.includes('⚡');

  const color = isToolLine ? 'var(--emerald)'
    : isSuccess ? '#60a5fa'
    : isWarning  ? 'var(--amber)'
    : 'var(--text-mid)';

  return (
    <div style={{
      display: 'flex',
      gap: '10px',
      padding: '3px 0',
      animation: `fade-up 0.15s ease ${idx * 0.015}s both`,
    }}>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--text-dim)', flexShrink: 0, paddingTop: 2, userSelect: 'none' }}>
        {String(idx + 1).padStart(3, '0')}
      </span>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color, whiteSpace: 'pre-wrap', lineHeight: 1.55, wordBreak: 'break-word' }}>
        {line}
      </span>
    </div>
  );
}

function SourceCard({ source, idx }) {
  return (
    <div style={{
      padding: '1.1rem 1.1rem',
      borderRadius: '14px',
      background: 'rgba(10,13,26,0.6)',
      border: '1px solid var(--border-faint)',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.65rem',
      animation: `fade-up 0.2s ease ${idx * 0.04}s both`,
      transition: 'border-color 0.2s',
    }}
    onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--border-soft)'}
    onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border-faint)'}
    >
      {/* Source header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
        <span style={{
          width: 26, height: 26, borderRadius: '6px', flexShrink: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: 'rgba(99,102,241,0.15)',
          fontFamily: 'var(--font-mono)', fontSize: '0.68rem', fontWeight: 700, color: 'var(--indigo)',
        }}>
          {source.id}
        </span>
        <div>
          <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-bright)', lineHeight: 1.35, letterSpacing: '-0.01em' }}>
            {source.title}
          </h4>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontSize: '0.72rem', color: 'var(--indigo)', textDecoration: 'none',
              display: 'flex', alignItems: 'center', gap: 3, marginTop: 3,
              opacity: 0.8,
            }}
          >
            <Globe size={10} />
            {(() => { try { return new URL(source.url).hostname; } catch { return source.url; } })()}
            <ExternalLink size={9} />
          </a>
        </div>
      </div>

      {/* Evidence */}
      {source.evidence && source.evidence.length > 0 && (
        <div style={{
          padding: '0.6rem 0.75rem',
          borderRadius: '8px',
          background: 'rgba(99,102,241,0.06)',
          border: '1px solid var(--border-faint)',
        }}>
          <div style={{ fontSize: '0.68rem', fontWeight: 700, color: 'var(--text-dim)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '0.45rem' }}>
            Key evidence
          </div>
          <ul style={{ paddingLeft: '1rem', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
            {source.evidence.map((fact, i) => (
              <li key={i} style={{ fontSize: '0.8rem', color: 'var(--text-mid)', lineHeight: 1.5 }}>{fact}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Snippet */}
      {source.snippet && (
        <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', lineHeight: 1.55, margin: 0 }}>
          {source.snippet}
        </p>
      )}
    </div>
  );
}

function ResearchResults({ sessionId, onReset }) {
  const [activeTab, setActiveTab] = useState('report');
  const [downloading, setDownloading] = useState(false);

  const { data: session, isLoading } = useQuery({
    queryKey: ['researchSession', sessionId],
    queryFn: () => researchApi.getSession(sessionId),
    enabled: !!sessionId,
  });

  const { data: sourcesData } = useQuery({
    queryKey: ['researchSources', sessionId],
    queryFn: () => researchApi.getSources(sessionId),
    enabled: !!sessionId,
  });

  const sources = sourcesData?.sources || [];

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/research/${sessionId}/download/pdf`);
      if (!response.ok) throw new Error('Failed to download PDF');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `research_report_${sessionId.substring(0, 8)}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download PDF. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div style={{ width: 32, height: 32, border: '3px solid var(--border-soft)', borderTopColor: 'var(--indigo)', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 1rem' }} />
        <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>Loading report…</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

      {/* ── Heading ── */}
      <div style={{ paddingLeft: '2px' }}>
        <p style={{
          fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.12em',
          textTransform: 'uppercase', color: 'var(--emerald)',
          marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '6px',
        }}>
          <span style={{ display: 'inline-block', width: 18, height: 1, background: 'var(--emerald)', verticalAlign: 'middle' }} />
          Research complete
        </p>
        <h1 style={{ fontSize: 'clamp(1.5rem, 4vw, 2rem)', fontWeight: 800, letterSpacing: '-0.03em', color: 'var(--text-bright)', lineHeight: 1.1 }}>
          Here's what the agent found.
        </h1>
        {session?.user_query && (
          <p style={{
            marginTop: '0.6rem', fontSize: '0.85rem', color: 'var(--text-dim)',
            fontStyle: 'italic', lineHeight: 1.5,
            borderLeft: '2px solid var(--border-soft)', paddingLeft: '0.75rem',
            maxWidth: '580px',
          }}>
            "{session.user_query}"
          </p>
        )}
      </div>

      {/* ── Tab bar ── */}
      <div style={{
        display: 'flex',
        gap: '4px',
        background: 'rgba(10,13,26,0.7)',
        border: '1px solid var(--border-faint)',
        borderRadius: '12px',
        padding: '4px',
      }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            onClick={() => setActiveTab(tab.id)}
            style={{
              flex: 1,
              padding: '0.5rem 0.5rem',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.78rem',
              fontWeight: 700,
              letterSpacing: '-0.01em',
              fontFamily: 'var(--font-sans)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '5px',
              transition: 'all 0.2s ease',
              background: activeTab === tab.id
                ? 'linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.2))'
                : 'transparent',
              color: activeTab === tab.id ? 'var(--text-bright)' : 'var(--text-dim)',
              borderColor: activeTab === tab.id ? 'var(--border-soft)' : 'transparent',
              boxShadow: activeTab === tab.id ? '0 0 12px rgba(99,102,241,0.15)' : 'none',
            }}
          >
            {tab.icon}
            {tab.label}
            {tab.id === 'sources' && sources.length > 0 && (
              <span style={{
                background: 'var(--indigo)', color: '#fff',
                borderRadius: '99px', fontSize: '0.6rem', fontWeight: 700,
                padding: '1px 5px', lineHeight: '14px', fontFamily: 'var(--font-mono)',
              }}>
                {sources.length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* ── Tab content ── */}
      <div key={activeTab} style={{ animation: 'fade-up 0.2s ease both' }}>

        {/* Report tab */}
        {activeTab === 'report' && (
          <div className="card" style={{ padding: '1.75rem 2rem' }}>
            <div style={{
              fontSize: '0.88rem',
              color: 'var(--text-mid)',
              lineHeight: 1.85,
              whiteSpace: 'pre-wrap',
              maxHeight: '60vh',
              overflowY: 'auto',
              paddingRight: '0.5rem',
            }}>
              {session?.research_goal
                ? session.research_goal
                : <span style={{ color: 'var(--text-dim)', fontStyle: 'italic' }}>No report content yet.</span>
              }
            </div>
          </div>
        )}

        {/* Plan tab */}
        {activeTab === 'plan' && (
          <div className="card" style={{ padding: '1.75rem 2rem' }}>
            {session?.research_plan && session.research_plan.length > 0 ? (
              <ol style={{ paddingLeft: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {session.research_plan.map((q, i) => (
                  <li key={i} style={{
                    display: 'flex', gap: '0.85rem', alignItems: 'flex-start',
                    animation: `fade-up 0.2s ease ${i * 0.04}s both`,
                  }}>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '0.68rem', fontWeight: 700,
                      color: 'var(--indigo)', flexShrink: 0,
                      background: 'rgba(99,102,241,0.1)', border: '1px solid var(--border-faint)',
                      borderRadius: '5px', padding: '2px 6px', marginTop: 2,
                    }}>
                      Q{i + 1}
                    </span>
                    <span style={{ fontSize: '0.88rem', color: 'var(--text-mid)', lineHeight: 1.6 }}>{q}</span>
                  </li>
                ))}
              </ol>
            ) : (
              <p style={{ color: 'var(--text-dim)', fontStyle: 'italic', fontSize: '0.88rem' }}>No plan data available.</p>
            )}
          </div>
        )}

        {/* Agent log tab */}
        {activeTab === 'log' && (
          <div className="card" style={{ padding: '1rem 1.25rem' }}>
            <div style={{
              background: 'rgba(6,8,16,0.85)',
              border: '1px solid var(--border-faint)',
              borderRadius: '10px',
              padding: '1rem',
              maxHeight: '60vh',
              overflowY: 'auto',
            }}>
              {/* Terminal top bar */}
              <div style={{ display: 'flex', gap: '6px', marginBottom: '0.85rem', alignItems: 'center' }}>
                {['#f43f5e','#f59e0b','#10b981'].map(c => (
                  <div key={c} style={{ width: 10, height: 10, borderRadius: '50%', background: c, opacity: 0.7 }} />
                ))}
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--text-dim)', marginLeft: '6px' }}>agent.log</span>
              </div>

              {session?.reasoning && session.reasoning.length > 0 ? (
                session.reasoning.map((line, i) => (
                  <LogLine key={i} line={line} idx={i} />
                ))
              ) : (
                <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>No log data.</p>
              )}
            </div>
          </div>
        )}

        {/* Sources tab */}
        {activeTab === 'sources' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {sources.length > 0 ? (
              sources.map((source, i) => (
                <SourceCard key={i} source={source} idx={i} />
              ))
            ) : (
              <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
                <p style={{ color: 'var(--text-dim)', fontSize: '0.88rem', fontStyle: 'italic' }}>No sources found.</p>
              </div>
            )}
          </div>
        )}

      </div>

      {/* ── Bottom action bar ── */}
      <div style={{
        display: 'flex',
        gap: '0.75rem',
        padding: '1rem 1.25rem',
        background: 'rgba(6,8,16,0.85)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        border: '1px solid var(--border-faint)',
        borderRadius: '14px',
        position: 'sticky',
        bottom: '50px',
      }}>
        <button
          id="download-pdf"
          className="btn btn-primary"
          onClick={handleDownloadPDF}
          disabled={downloading}
          style={{ flex: 1, borderRadius: '10px' }}
        >
          {downloading ? (
            <>
              <span style={{ width: 15, height: 15, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'spin 0.7s linear infinite', display: 'inline-block' }} />
              Generating…
            </>
          ) : (
            <>
              <Download size={15} />
              Download PDF
            </>
          )}
        </button>
        <button
          id="new-research"
          className="btn btn-ghost"
          onClick={onReset}
          style={{ flex: 1, borderRadius: '10px' }}
        >
          <RotateCcw size={15} />
          New Research
        </button>
      </div>

    </div>
  );
}

export default ResearchResults;
