/**
 * Generation API service.
 *
 * Handles API calls for textbook outline generation.
 */

import apiClient from './api';
import { GenerationFormData } from '../components/generation/GenerationForm';

export interface TextbookResponse {
  id: number;
  user_id: number;
  title: string;
  subject: string;
  level: string;
  description?: string;
  chapters: Chapter[];
  created_at: string;
  updated_at: string;
}

export interface Chapter {
  chapter_number: number;
  title: string;
  objectives?: string;
  sections: Section[];
}

export interface Section {
  section_number: number;
  title: string;
}

export const generationService = {
  /**
   * Generate a textbook outline.
   */
  async generateOutline(data: GenerationFormData): Promise<TextbookResponse> {
    const payload = {
      subject: data.subject,
      level: data.level,
      num_chapters: data.numChapters,
      description: data.description,
    };

    return await apiClient.post<TextbookResponse>(
      '/api/v1/generation/generate-outline',
      payload
    );
  },

  /**
   * Get current user's textbook.
   */
  async getMyTextbook(): Promise<TextbookResponse | null> {
    return await apiClient.get<TextbookResponse | null>('/api/v1/textbooks/me');
  },

  /**
   * Get textbook by ID.
   */
  async getTextbook(id: number): Promise<TextbookResponse> {
    return await apiClient.get<TextbookResponse>(`/api/v1/textbooks/${id}`);
  },

  /**
   * Delete textbook.
   */
  async deleteTextbook(id: number): Promise<void> {
    return await apiClient.delete(`/api/v1/textbooks/${id}`);
  },
};

export default generationService;
