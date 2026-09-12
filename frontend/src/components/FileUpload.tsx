import React, { useState } from 'react';

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setStatusMsg('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatusMsg('Please select a file first.');
      return;
    }

    setIsUploading(true);
    setStatusMsg('Extracting text & creating chunks...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setStatusMsg(`Success: ${data.total_chunks} chunks stored.`);
      setSelectedFile(null);
      onUploadSuccess();
    } catch (err: any) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-box">
      <input
        type="file"
        accept=".pdf,.docx,.txt,.md"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      <button
        className="btn"
        style={{ width: '100%' }}
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
      >
        {isUploading ? 'Processing...' : 'Upload Document'}
      </button>
      {statusMsg && (
        <p style={{ marginTop: '8px', fontSize: '0.75rem', color: '#495057' }}>
          {statusMsg}
        </p>
      )}
    </div>
  );
};
