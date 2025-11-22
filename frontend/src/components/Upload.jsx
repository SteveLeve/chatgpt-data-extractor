import React, { useState } from 'react';
import { Upload as UploadIcon, FileArchive } from 'lucide-react';

export default function Upload() {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setMessage('');

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!res.ok) throw new Error('Upload failed');
      
      setMessage('Upload successful!');
      
      // Trigger ingest
      await fetch('/api/ingest', { method: 'POST' });
      setMessage('Upload successful! Ingestion started.');
      
    } catch (err) {
      setMessage('Error uploading file.');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h3 style={{ marginTop: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <FileArchive size={20} />
        Data Upload
      </h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        Upload your <code>source-data.zip</code> to start ingestion.
      </p>
      
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label className="btn" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: uploading ? 'wait' : 'pointer' }}>
          <UploadIcon size={18} />
          {uploading ? 'Uploading...' : 'Select Zip File'}
          <input 
            type="file" 
            accept=".zip" 
            onChange={handleUpload} 
            style={{ display: 'none' }} 
            disabled={uploading}
          />
        </label>
        {message && <span>{message}</span>}
      </div>
    </div>
  );
}
