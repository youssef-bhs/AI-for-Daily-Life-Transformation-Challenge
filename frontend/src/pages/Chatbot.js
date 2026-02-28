import React, { useState, useRef, useEffect } from 'react';
import { chatAPI } from '../api';

const WELCOME = {
  role: 'assistant',
  content:
    '👋 Salut! Je suis SmartStudent AI.\n\nJe peux t\'aider avec :\n• Stratégies de révision et planning\n• Gestion du budget en TND\n• Gestion du stress académique\n• Conseils sur le temps de travail\n\nPose-moi ta question !',
};

const SUGGESTIONS = [
  'Comment préparer mes examens efficacement ?',
  'Aide-moi à économiser de l\'argent en TND',
  'Technique Pomodoro – comment ça marche ?',
  'Je procrastine, aide-moi !',
];

export default function Chatbot() {
  const [open, setOpen]       = useState(false);
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput]     = useState('');
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);
  const [provider, setProvider] = useState('');
  const bottomRef             = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    if (open) bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  const buildHistory = () =>
    messages
      .filter(m => m.role !== 'assistant' || m !== WELCOME)
      .slice(-10)
      .map(m => ({ role: m.role, content: m.content }));

  const sendMessage = async (text) => {
    const question = text || input.trim();
    if (!question || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setLoading(true);
    setSources([]);

    try {
      const { data } = await chatAPI.ask({
        question,
        conversation_history: buildHistory(),
        top_k_docs: 3,
      });
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
      setSources(data.retrieved_docs || []);
      setProvider(data.provider || '');
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: '❌ Erreur de connexion. Vérifie que le backend est lancé et que ta clé API est configurée dans backend/.env.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([WELCOME]);
    setSources([]);
  };

  return (
    <>
      {/* ── Floating toggle button ── */}
      <button
        className={`chat-fab ${open ? 'chat-fab-open' : ''}`}
        onClick={() => setOpen(o => !o)}
        title="AI Chat"
      >
        {open ? '✕' : '🤖'}
        {!open && <span className="chat-fab-badge">AI</span>}
      </button>

      {/* ── Chat panel ── */}
      {open && (
        <div className="chatbot-panel">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-info">
              <span className="chat-header-icon">🎓</span>
              <div>
                <div className="chat-header-title">SmartStudent AI</div>
                <div className="chat-header-sub">
                  {provider ? `${provider} · RAG activé` : 'RAG activé'}
                </div>
              </div>
            </div>
            <button className="chat-clear-btn" onClick={clearChat} title="Effacer la conversation">
              🗑
            </button>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`chat-bubble-wrap ${msg.role}`}>
                {msg.role === 'assistant' && (
                  <div className="chat-avatar">🤖</div>
                )}
                <div className={`chat-bubble ${msg.role}`}>
                  {msg.content.split('\n').map((line, j) => (
                    <span key={j}>{line}<br /></span>
                  ))}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="chat-bubble-wrap assistant">
                <div className="chat-avatar">🤖</div>
                <div className="chat-bubble assistant chat-typing">
                  <span /><span /><span />
                </div>
              </div>
            )}

            {/* Sources */}
            {sources.length > 0 && !loading && (
              <div className="chat-sources">
                <span className="chat-sources-label">📚 Sources :</span>
                {sources.map((s, i) => (
                  <span key={i} className="chat-source-pill">{s}</span>
                ))}
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Quick suggestions (only at start) */}
          {messages.length === 1 && (
            <div className="chat-suggestions">
              {SUGGESTIONS.map((s, i) => (
                <button key={i} className="chat-suggestion-btn" onClick={() => sendMessage(s)}>
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <div className="chat-input-row">
            <textarea
              className="chat-input"
              rows={1}
              placeholder="Pose ta question…"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
              disabled={loading}
            />
            <button
              className="chat-send-btn"
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
            >
              {loading ? '…' : '➤'}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
