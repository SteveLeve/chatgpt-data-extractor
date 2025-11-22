import React, { useEffect, useState } from 'react';
import { Activity, CheckCircle, XCircle, Loader2 } from 'lucide-react';

export default function Stats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error(e);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, []);

  if (!stats) return null;

  return (
    <div className="card" style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Activity size={20} color="var(--accent)" />
        <span>Status: <span style={{ color: stats.ingestion_status === 'running' ? 'var(--accent)' : 'var(--text-secondary)' }}>{stats.ingestion_status.toUpperCase()}</span></span>
      </div>
      
      {stats.ingestion_status === 'running' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Loader2 className="spin" size={20} />
          <span>Ingesting...</span>
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        {stats.agent_initialized ? (
          <CheckCircle size={20} color="var(--success)" />
        ) : (
          <XCircle size={20} color="var(--text-secondary)" />
        )}
        <span>Agent Ready</span>
      </div>
      
      {stats.ingestion_message && (
        <div style={{ marginLeft: 'auto', color: 'var(--text-secondary)' }}>
          {stats.ingestion_message}
        </div>
      )}
    </div>
  );
}
