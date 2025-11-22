import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content }),
      });

      if (!response.ok) throw new Error('Chat failed');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMsg = { role: 'assistant', content: '' };
      
      setMessages(prev => [...prev, assistantMsg]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value);
        assistantMsg.content += text;
        
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = { ...assistantMsg };
          return newMessages;
        });
      }

    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not get response.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
      <div style={{ flex: 1, overflowY: 'auto', paddingRight: '0.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ 
            display: 'flex', 
            gap: '1rem', 
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '80%',
            backgroundColor: msg.role === 'user' ? 'var(--accent)' : 'var(--bg-primary)',
            padding: '1rem',
            borderRadius: '0.75rem',
            borderBottomRightRadius: msg.role === 'user' ? 0 : '0.75rem',
            borderBottomLeftRadius: msg.role === 'assistant' ? 0 : '0.75rem',
          }}>
            <div style={{ marginTop: '0.25rem' }}>
              {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>{msg.content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something about your data..."
          disabled={loading}
        />
        <button type="submit" className="btn" disabled={loading || !input.trim()}>
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}
