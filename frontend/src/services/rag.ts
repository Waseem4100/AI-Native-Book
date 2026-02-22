/**
 * RAG Chatbot service for communicating with the backend API.
 */

import axios from 'axios';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface SourceDocument {
  content: string;
  chapter_id: string;
  section_id: string;
  score: number;
}

export interface ChatRequest {
  message: string;
  conversation_history: ChatMessage[];
  chapter_id?: string;
  section_id?: string;
  selected_text?: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceDocument[];
  conversation_history: ChatMessage[];
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Send a chat message to the RAG chatbot.
 */
export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>('/rag/chat', request);
  return response.data;
}

/**
 * Index a document chunk for RAG search.
 */
export async function indexDocument(content: string, chapterId: string, sectionId?: string): Promise<void> {
  await api.post('/rag/index', {
    content,
    chapter_id: chapterId,
    section_id: sectionId,
  });
}

/**
 * Index multiple document chunks in batch.
 */
export async function indexDocumentsBatch(documents: Array<{
  content: string;
  chapter_id: string;
  section_id?: string;
}>): Promise<void> {
  await api.post('/rag/index/batch', { documents });
}

/**
 * Check the health of the RAG service.
 */
export async function checkRagHealth(): Promise<{
  status: string;
  qdrant_connected: boolean;
  openai_connected: boolean;
}> {
  const response = await api.get('/rag/health');
  return response.data;
}
