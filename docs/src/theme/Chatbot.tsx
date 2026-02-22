import React from 'react';
import { useLocation } from '@docusaurus/router';
import { useEffect } from 'react';

// Inline chatbot component for Docusaurus
function Chatbot() {
  const location = useLocation();
  const [isExpanded, setIsExpanded] = React.useState(false);
  const [messages, setMessages] = React.useState([
    {
      role: 'assistant',
      content: "Hello! I'm your AI textbook assistant. I can answer questions about Physical AI & Humanoid Robotics based on the textbook content. What would you like to know?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [conversationHistory, setConversationHistory] = React.useState([]);
  const messagesEndRef = React.useRef(null);

  const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : 'https://ai-native-book-backend.herokuapp.com/api';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/rag/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_history: conversationHistory,
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      }]);
      setConversationHistory(data.conversation_history);
    } catch (error) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I encountered an error. Please ensure the backend service is running.",
        timestamp: new Date(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([{
      role: 'assistant',
      content: "Chat cleared. How can I help you?",
      timestamp: new Date(),
    }]);
    setConversationHistory([]);
  };

  return (
    <div className="chatbot-container">
      {!isExpanded ? (
        <button className="chatbot-toggle" onClick={() => setIsExpanded(true)}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V17C3 16.4696 2.78929 15.9609 2.41421 15.5858C2.03914 15.2107 1.82843 14.702 1.82843 14.1716V7C1.82843 5.93913 2.25086 4.92172 3.00289 4.16971C3.75493 3.4177 4.77234 2.99526 5.83321 2.99526H19C19.5304 2.99526 20.0391 3.20598 20.4142 3.58105C20.7893 3.95613 21 4.46487 21 4.99526V15Z" stroke="currentColor" strokeWidth="2"/>
          </svg>
          <span>Ask AI</span>
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V17C3 16.4696 2.78929 15.9609 2.41421 15.5858C2.03914 15.2107 1.82843 14.702 1.82843 14.1716V7C1.82843 5.93913 2.25086 4.92172 3.00289 4.16971C3.75493 3.4177 4.77234 2.99526 5.83321 2.99526H19C19.5304 2.99526 20.0391 3.20598 20.4142 3.58105C20.7893 3.95613 21 4.46487 21 4.99526V15Z" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Textbook AI</span>
            </div>
            <div className="chatbot-actions">
              <button onClick={clearChat} className="chatbot-clear">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M3 6H5H21" stroke="currentColor" strokeWidth="2"/>
                  <path d="M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </button>
              <button onClick={() => setIsExpanded(false)} className="chatbot-close">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18" stroke="currentColor" strokeWidth="2"/>
                  <path d="M6 6L18 18" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="message-content">
                  {msg.content.split('\n').map((line, j) => <p key={j}>{line}</p>)}
                </div>
                {msg.sources?.length > 0 && (
                  <div className="message-sources">
                    <strong>Sources:</strong>
                    {msg.sources.map((s, j) => (
                      <div key={j} className="source">
                        <span className="source-chapter">{s.chapter_id}</span>
                        {s.section_id && <span> • {s.section_id}</span>}
                      </div>
                    ))}
                  </div>
                )}
                <div className="message-time">{msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant loading">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about the textbook..."
              disabled={isLoading}
              className="chatbot-input"
            />
            <button type="submit" disabled={isLoading || !input.trim()} className="chatbot-send">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
