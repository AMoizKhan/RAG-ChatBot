import React, { useState } from 'react';
import { ChatMessage, ChunkSource } from '../types';

interface ChatBoxProps {
  messages: ChatMessage[];
  onSendMessage: (question: string) => Promise<void>;
  isLoading: boolean;
}

export const ChatBox: React.FC<ChatBoxProps> = ({ messages, onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');
  const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});

  const toggleSource = (msgId: string) => {
    setExpandedSources((prev) => ({
      ...prev,
      [msgId]: !prev[msgId],
    }));
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const query = input;
    setInput('');
    await onSendMessage(query);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        Document Q&A Assistant (RAG)
      </div>

      <div className="messages-area">
        {messages.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#6c757d', marginTop: '40px', fontSize: '0.95rem' }}>
            Upload a document and ask questions about its content.
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.sender}`}>
              <div className="message-bubble">{msg.text}</div>

              {/* Show Sources Toggle for AI messages */}
              {msg.sender === 'ai' && msg.sources && msg.sources.length > 0 && (
                <>
                  <button
                    className="sources-toggle"
                    onClick={() => toggleSource(msg.id)}
                  >
                    {expandedSources[msg.id] ? 'Hide Sources ▲' : `View Sources (${msg.sources.length} chunks used) ▼`}
                  </button>

                  {expandedSources[msg.id] && (
                    <div className="sources-box">
                      {msg.sources.map((s: ChunkSource, idx: number) => (
                        <div key={idx} className="source-item">
                          <div className="source-meta">
                            Source: {s.source} | Page: {s.page}
                          </div>
                          <div>"{s.text}"</div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="message ai">
            <div className="message-bubble" style={{ color: '#6c757d' }}>
              Searching vector DB and generating answer...
            </div>
          </div>
        )}
      </div>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          placeholder="Ask anything about your uploaded documents..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
        />
        <button className="btn" type="submit" disabled={!input.trim() || isLoading}>
          Send
        </button>
      </form>
    </div>
  );
};
