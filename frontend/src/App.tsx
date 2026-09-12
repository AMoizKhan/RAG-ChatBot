import React, { useState, useEffect } from 'react';
import { FileUpload } from './components/FileUpload';
import { DocumentList } from './components/DocumentList';
import { ChatBox } from './components/ChatBox';
import { ChatMessage, DocumentInfo } from './types';

export const App: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchDocuments = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/documents');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error('Failed to load documents:', err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleSendMessage = async (question: string) => {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: question,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error('Failed to get answer from server');
      }

      const data = await res.json();

      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: `Error: ${err.message}. Make sure the backend server is running on port 8000.`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      {/* Left Sidebar */}
      <aside className="sidebar">
        <div>
          <h2>Document Upload</h2>
          <p style={{ fontSize: '0.8rem', color: '#6c757d', margin: '6px 0 12px 0' }}>
            Supports PDF, Word (.docx), and Text (.txt)
          </p>
          <FileUpload onUploadSuccess={fetchDocuments} />
        </div>

        <DocumentList
          documents={documents}
          onDeleteSuccess={fetchDocuments}
        />
      </aside>

      {/* Right Chat View */}
      <main style={{ flex: 1, display: 'flex' }}>
        <ChatBox
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
};

export default App;
