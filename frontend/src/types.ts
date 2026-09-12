export interface ChunkSource {
  text: string;
  source: string;
  page: number;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  sources?: ChunkSource[];
}

export interface DocumentInfo {
  name: string;
  chunk_count: number;
}
