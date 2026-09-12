import React from 'react';
import { DocumentInfo } from '../types';

interface DocumentListProps {
  documents: DocumentInfo[];
  onDeleteSuccess: () => void;
}

export const DocumentList: React.FC<DocumentListProps> = ({ documents, onDeleteSuccess }) => {
  const handleDelete = async (docName: string) => {
    if (!confirm(`Are you sure you want to delete ${docName}?`)) return;

    try {
      await fetch(`http://localhost:8000/api/documents/${encodeURIComponent(docName)}`, {
        method: 'DELETE',
      });
      onDeleteSuccess();
    } catch (err) {
      alert('Failed to delete document');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
      <h2 style={{ marginBottom: '12px' }}>Active Documents ({documents.length})</h2>
      {documents.length === 0 ? (
        <p style={{ fontSize: '0.85rem', color: '#6c757d' }}>No documents uploaded yet.</p>
      ) : (
        <ul className="doc-list">
          {documents.map((doc) => (
            <li key={doc.name} className="doc-item">
              <div className="doc-info">
                <span className="doc-name" title={doc.name}>{doc.name}</span>
                <span className="doc-chunks">{doc.chunk_count} chunks in DB</span>
              </div>
              <button
                className="delete-btn"
                onClick={() => handleDelete(doc.name)}
                title="Delete document"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
