/**
 * Textbook Outline Component
 *
 * Displays textbook chapter structure with expand/collapse functionality.
 */

import React, { useState } from 'react';

interface Section {
  section_number: number;
  title: string;
}

interface Chapter {
  chapter_number: number;
  title: string;
  objectives?: string;
  sections: Section[];
}

interface TextbookOutlineProps {
  chapters: Chapter[];
  title?: string;
}

export const TextbookOutline: React.FC<TextbookOutlineProps> = ({
  chapters,
  title,
}) => {
  const [expandedChapters, setExpandedChapters] = useState<Set<number>>(
    new Set([1])
  );

  const toggleChapter = (chapterNumber: number) => {
    setExpandedChapters(prev => {
      const newSet = new Set(prev);
      if (newSet.has(chapterNumber)) {
        newSet.delete(chapterNumber);
      } else {
        newSet.add(chapterNumber);
      }
      return newSet;
    });
  };

  if (!chapters || chapters.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>
        No chapters yet. Generate a textbook outline to get started.
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '800px' }}>
      {title && (
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>{title}</h2>
      )}

      <div>
        {chapters.map(chapter => {
          const isExpanded = expandedChapters.has(chapter.chapter_number);

          return (
            <div
              key={chapter.chapter_number}
              style={{
                marginBottom: '1rem',
                border: '1px solid #ddd',
                borderRadius: '4px',
                overflow: 'hidden',
              }}
            >
              <button
                onClick={() => toggleChapter(chapter.chapter_number)}
                style={{
                  width: '100%',
                  padding: '1rem',
                  backgroundColor: isExpanded ? '#f0f0f0' : 'white',
                  border: 'none',
                  textAlign: 'left',
                  cursor: 'pointer',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: '1rem',
                }}
              >
                <span style={{ fontWeight: 'bold' }}>
                  Chapter {chapter.chapter_number}: {chapter.title}
                </span>
                <span>{isExpanded ? '▼' : '▶'}</span>
              </button>

              {isExpanded && (
                <div style={{ padding: '1rem', backgroundColor: '#fafafa' }}>
                  {chapter.objectives && (
                    <div style={{ marginBottom: '1rem' }}>
                      <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                        Learning Objectives:
                      </strong>
                      <p style={{ margin: 0, color: '#555' }}>
                        {chapter.objectives}
                      </p>
                    </div>
                  )}

                  <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                    Sections:
                  </strong>
                  <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
                    {chapter.sections.map(section => (
                      <li
                        key={section.section_number}
                        style={{ marginBottom: '0.5rem' }}
                      >
                        {section.section_number}. {section.title}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TextbookOutline;
