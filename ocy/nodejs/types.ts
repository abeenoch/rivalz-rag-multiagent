export interface KnowledgeBase {
  id: string;
  name: string;
  status: "processing" | "ready" | "failed";
  created_at: string;
  documents: Document[];
}

export interface Document {
  id: string;
  name: string;
  ipfs_hash: string;
  created_at: string;
}

export interface ChatSession {
  session_id: string;
  knowledge_base_id: string;
  created_at: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  session_id: string;
  answer: string;
  sources?: string[];
}

export interface UploadHistoryItem {
  _id: string;
  uploadHash: string;
  userId: string;
  fileName: string;
  fileSize: number;
  createdAt: string;
  updatedAt: string;
  __v: number;
}

export interface UploadHistoryResponse {
  uploadHistories: UploadHistoryItem[];
  // Add any pagination fields if they exist in the response
}
