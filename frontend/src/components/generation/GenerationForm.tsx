/**
 * Generation Form Component
 *
 * Form for generating textbook outlines with subject, level, and chapter count inputs.
 */

import React, { useState } from 'react';

interface GenerationFormProps {
  onSubmit: (data: GenerationFormData) => void;
  loading?: boolean;
}

export interface GenerationFormData {
  subject: string;
  level: string;
  numChapters: number;
  description?: string;
}

const EDUCATION_LEVELS = [
  'Elementary School',
  'Middle School',
  'High School',
  'Undergraduate',
  'Graduate',
  'Professional',
];

export const GenerationForm: React.FC<GenerationFormProps> = ({
  onSubmit,
  loading = false,
}) => {
  const [subject, setSubject] = useState('');
  const [level, setLevel] = useState('High School');
  const [numChapters, setNumChapters] = useState(10);
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      subject,
      level,
      numChapters,
      description: description || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '600px' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <label
          htmlFor="subject"
          style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}
        >
          Subject *
        </label>
        <input
          id="subject"
          type="text"
          value={subject}
          onChange={e => setSubject(e.target.value)}
          required
          placeholder="e.g., Introduction to Python Programming"
          style={{
            width: '100%',
            padding: '0.75rem',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '1rem',
          }}
        />
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label
          htmlFor="level"
          style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}
        >
          Educational Level *
        </label>
        <select
          id="level"
          value={level}
          onChange={e => setLevel(e.target.value)}
          required
          style={{
            width: '100%',
            padding: '0.75rem',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '1rem',
          }}
        >
          {EDUCATION_LEVELS.map(lvl => (
            <option key={lvl} value={lvl}>
              {lvl}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label
          htmlFor="numChapters"
          style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}
        >
          Number of Chapters: {numChapters}
        </label>
        <input
          id="numChapters"
          type="range"
          min="3"
          max="30"
          value={numChapters}
          onChange={e => setNumChapters(parseInt(e.target.value))}
          style={{ width: '100%' }}
        />
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            fontSize: '0.875rem',
            color: '#666',
            marginTop: '0.25rem',
          }}
        >
          <span>3</span>
          <span>30</span>
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label
          htmlFor="description"
          style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}
        >
          Description (Optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Optional description of the textbook..."
          rows={3}
          style={{
            width: '100%',
            padding: '0.75rem',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '1rem',
            fontFamily: 'inherit',
          }}
        />
      </div>

      <button
        type="submit"
        disabled={loading || !subject}
        style={{
          padding: '0.75rem 2rem',
          backgroundColor: loading || !subject ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          fontSize: '1rem',
          cursor: loading || !subject ? 'not-allowed' : 'pointer',
          fontWeight: 'bold',
        }}
      >
        {loading ? 'Generating...' : 'Generate Textbook Outline'}
      </button>
    </form>
  );
};

export default GenerationForm;
