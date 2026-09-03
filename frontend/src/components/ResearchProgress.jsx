import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { CheckCircle, XCircle, X } from 'lucide-react';
import { researchApi } from '../services/api';

const STAGES = [
  { key: 'planning',     label: 'Planning',     sub: 'Building research strategy' },
  { key: 'researching',  label: 'Searching',    sub: 'Querying web & academic sources' },
  { key: 'analyzing',    label: 'Analyzing',    sub: 'Extracting key evidence' },
  { key: 'verifying',    label: 'Verifying',    sub: 'Cross-checking claims' },
  { key: 'synthesizing', label: 'Synthesizing', sub: 'Composing final report' },
];

const STATUS_TO_STAGE = {
  pending: -1,
  planning: 0,
  researching: 1,
  analyzing: 2,
  verifying: 3,
  synthesizing: 4,
  generating: 4,
  completed: 5,
  failed: -2,
};

function ResearchProgress({ sessionId, onComplete, onReset }) {
  const [progress, setProgress] = useState(0);
  const [localTask, setLocalTask] = useState('');

  const { data: status, isError } = useQuery({
    queryKey: ['researchStatus', sessionId],
    queryFn: () => researchApi.getStatus(sessionId),
    refetchInterval: 2000,
    enabled: !!sessionId,
  });

  useEffect(() => {
    if (!status) return;
    setProgress(status.progress || 0);
    if (status.current_task) setLocalTask(status.current_task);
    if (status.status === 'completed') {
      setTimeout(() => onComplete(), 1000);
    }
  }, [status, onComplete]);

  const stageIndex = STATUS_TO_STAGE[status?.status ?? 'pending'] ?? -1;
  const failed = isError || status?.status === 'failed';

  // Build an arc for the circular progress
  const r = 54;
  const circ = 2 * Math.PI * r;
  const dash = ((progress / 100) * circ).toFixed(1);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

      {/* ── Status label ── */}
      <div style={{ paddingLeft: '2px' }}>
        <p style={{
          fontSize: '0.72rem', fontWeight: 700,
          letterSpacing: '0.12em', textTransform: 'uppercase',
          color: failed ? 'var(--rose)' : 'var(--indigo)',
          marginBottom: '0.5rem',
          display: 'flex', alignItems: 'center', gap: '6px',
        }}>
          <span style={{ display: 'inline-block', width: 18, height: 1, background: failed ? 'var(--rose)' : 'var(--indigo)', verticalAlign: 'middle' }} />
          {failed ? 'Research failed' : 'Working on it'}
        </p>
        <h1 style={{ fontSize: 'clamp(1.5rem, 4vw, 2rem)', fontWeight: 800, letterSpacing: '-0.03em', color: 'var(--text-bright)', lineHeight: 1.1 }}>
          {failed ? 'Something went wrong.' : 'Agent is researching…'}
        </h1>
        <p style={{ color: 'var(--text-mid)', marginTop: '0.5rem', fontSize: '0.9rem' }}>
          {failed ? 'An error occurred during the research session.' : 'Sit back — this usually takes 1–3 minutes.'}
        </p>
      </div>

      {/* ── Progress card ── */}
      <div className="card" style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>

        {/* Circular arc */}
        <div style={{ position: 'relative', flexShrink: 0, width: 128, height: 128, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <svg width="128" height="128" style={{ position: 'absolute', top: 0, left: 0, transform: 'rotate(-90deg)' }}>
            <circle cx="64" cy="64" r={r} fill="none" stroke="var(--surface-3)" strokeWidth="8" />
            <circle
              cx="64" cy="64" r={r}
              fill="none"
              stroke="url(#arcGrad)"
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={`${dash} ${circ}`}
              style={{ transition: 'stroke-dasharray 0.5s cubic-bezier(0.4,0,0.2,1)' }}
            />
            <defs>
              <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="var(--indigo)" />
                <stop offset="100%" stopColor="var(--cyan)" />
              </linearGradient>
            </defs>
          </svg>
          {/* Center content */}
          <div style={{ textAlign: 'center', position: 'relative', zIndex: 1 }}>
            {failed ? (
              <XCircle size={28} color="var(--rose)" />
            ) : stageIndex >= 5 ? (
              <CheckCircle size={28} color="var(--emerald)" />
            ) : (
              <>
                <div style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '1.4rem',
                  fontWeight: 700,
                  color: 'var(--text-bright)',
                  letterSpacing: '-0.03em',
                  lineHeight: 1,
                }}>
                  {Math.round(progress)}
                </div>
                <div style={{ fontSize: '0.65rem', color: 'var(--text-dim)', letterSpacing: '0.06em', marginTop: 2 }}>%</div>
              </>
            )}
          </div>
        </div>

        {/* Stage timeline */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.55rem' }}>
          {STAGES.map((stage, i) => {
            const done    = i < stageIndex;
            const active  = i === stageIndex;
            const pending = i > stageIndex;
            return (
              <div key={stage.key} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                {/* Step dot */}
                <div style={{
                  width: 28, height: 28, borderRadius: '50%', flexShrink: 0,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  background: done ? 'rgba(16,185,129,0.15)' : active ? 'rgba(99,102,241,0.15)' : 'var(--surface-3)',
                  border: `2px solid ${done ? 'var(--emerald)' : active ? 'var(--indigo)' : 'var(--border-faint)'}`,
                  boxShadow: active ? '0 0 12px rgba(99,102,241,0.5)' : 'none',
                  animation: active ? 'pulse-ring 2s ease infinite' : 'none',
                  transition: 'all 0.3s ease',
                }}>
                  {done ? (
                    <CheckCircle size={13} color="var(--emerald)" />
                  ) : (
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '0.6rem', fontWeight: 700,
                      color: active ? 'var(--indigo)' : 'var(--text-dim)',
                    }}>
                      {String(i + 1).padStart(2, '0')}
                    </span>
                  )}
                </div>
                {/* Label */}
                <div>
                  <div style={{
                    fontSize: '0.82rem', fontWeight: 700,
                    color: done ? 'var(--emerald)' : active ? 'var(--text-bright)' : 'var(--text-dim)',
                    transition: 'color 0.3s',
                    letterSpacing: '-0.01em',
                  }}>
                    {stage.label}
                  </div>
                  {active && (
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: 1, animation: 'fade-up 0.2s ease' }}>
                      {stage.sub}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

      </div>

      {/* ── Terminal task box ── */}
      {localTask && !failed && (
        <div style={{
          background: 'rgba(10,13,26,0.8)',
          border: '1px solid var(--border-faint)',
          borderRadius: '12px',
          padding: '0.85rem 1rem',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.8rem',
          color: 'var(--cyan)',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '8px',
          animation: 'fade-up 0.2s ease',
        }}>
          <span style={{ color: 'var(--indigo)', flexShrink: 0, marginTop: 1 }}>›</span>
          <span style={{ color: 'var(--text-mid)', wordBreak: 'break-word', lineHeight: 1.5 }}>{localTask}</span>
          <span style={{ animation: 'blink 1s step-end infinite', color: 'var(--cyan)', flexShrink: 0 }}>▋</span>
        </div>
      )}

      {/* ── Cancel ── */}
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button
          id="cancel-research"
          className="btn btn-ghost"
          onClick={onReset}
          style={{ gap: '6px', fontSize: '0.8rem' }}
        >
          <X size={14} />
          Cancel
        </button>
      </div>

    </div>
  );
}

export default ResearchProgress;
