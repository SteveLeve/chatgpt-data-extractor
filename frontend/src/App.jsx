import React from 'react';
import Stats from './components/Stats';
import Upload from './components/Upload';
import Chat from './components/Chat';
import { MessageSquare } from 'lucide-react';

function App() {
  return (
    <div className="container">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <MessageSquare size={32} color="var(--accent)" />
          <h1 style={{ margin: 0, fontSize: '1.5rem' }}>ChatGPT Data Extractor</h1>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem', flex: 1, minHeight: 0 }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <Stats />
          <Upload />
          <div className="card" style={{ flex: 1 }}>
            <h3>Instructions</h3>
            <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              <li>Upload your <code>source-data.zip</code> if you haven't already.</li>
              <li>Wait for ingestion to complete (check status above).</li>
              <li>Start chatting with your data!</li>
            </ul>
          </div>
        </div>
        
        <Chat />
      </div>
    </div>
  );
}

export default App;
