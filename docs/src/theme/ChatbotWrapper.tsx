import React, { useEffect, useState } from 'react';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// Only load chatbot on client side
if (ExecutionEnvironment.canUseDOM) {
  // Dynamically import chatbot styles
  import('../css/chatbot.css');
}

// Chatbot styles embedded for Docusaurus
const chatbotStyles = `
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  font-family: var(--ifm-font-family-base);
}

.chatbot-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--ifm-color-primary);
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.chatbot-toggle:hover {
  background: var(--ifm-color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chatbot-window {
  width: 380px;
  height: 550px;
  background: var(--ifm-background-color);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--ifm-toc-border-color);
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--ifm-color-primary);
  color: white;
}

.chatbot-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.chatbot-actions {
  display: flex;
  gap: 8px;
}

.chatbot-clear,
.chatbot-close {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.chatbot-clear:hover,
.chatbot-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 14px;
}

.message.user {
  align-self: flex-end;
  background: var(--ifm-color-primary);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant {
  align-self: flex-start;
  background: var(--ifm-background-surface-color);
  border: 1px solid var(--ifm-toc-border-color);
  border-bottom-left-radius: 4px;
}

.message p {
  margin: 0;
}

.message p + p {
  margin-top: 8px;
}

.message-time {
  font-size: 11px;
  opacity: 0.6;
  margin-top: 4px;
  text-align: right;
}

.message-sources {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid var(--ifm-toc-border-color);
  font-size: 12px;
}

.message-sources strong {
  display: block;
  margin-bottom: 4px;
  color: var(--ifm-color-primary);
}

.source {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 0;
  flex-wrap: wrap;
}

.source-chapter {
  background: var(--ifm-color-primary-lightest);
  color: var(--ifm-color-primary-darkest);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.source-section {
  opacity: 0.7;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: var(--ifm-color-primary);
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

.chatbot-input-form {
  display: flex;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--ifm-toc-border-color);
  background: var(--ifm-background-surface-color);
}

.chatbot-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--ifm-toc-border-color);
  border-radius: 20px;
  font-size: 14px;
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  outline: none;
  transition: border-color 0.2s;
}

.chatbot-input:focus {
  border-color: var(--ifm-color-primary);
}

.chatbot-input::placeholder {
  color: var(--ifm-color-content-secondary);
}

.chatbot-send {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: var(--ifm-color-primary);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.chatbot-send:hover:not(:disabled) {
  background: var(--ifm-color-primary-dark);
  transform: scale(1.05);
}

.chatbot-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .chatbot-window {
    width: calc(100vw - 40px);
    height: calc(100vh - 100px);
  }
}

[data-theme='dark'] .message.assistant {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme='dark'] .source-chapter {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}
`;

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    chapter_id: string;
    section_id: string;
  }>;
  timestamp: Date;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

const API_BASE_URL = process.env.DOCUSARUS_APP_API_URL || 'http://localhost:8000/api';

export function ChatbotWrapper(): JSX.Element {
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hello! I'm your AI textbook assistant. I can answer questions about Physical AI & Humanoid Robotics based on the textbook content. What would you like to know?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState<ChatMessage[]>([]);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_history: conversationHistory,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationHistory(data.conversation_history);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: "I'm sorry, I encountered an error while processing your question. Please make sure the backend service is running and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: "Chat cleared. How can I help you?",
        timestamp: new Date(),
      },
    ]);
    setConversationHistory([]);
  };

  if (!ExecutionEnvironment.canUseDOM) {
    return <></>;
  }

  return (
    <>
      <style>{chatbotStyles}</style>
      <div className="chatbot-container">
        {!isExpanded ? (
          <button className="chatbot-toggle" onClick={() => setIsExpanded(true)} aria-label="Open chatbot">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V17C3 16.4696 2.78929 15.9609 2.41421 15.5858C2.03914 15.2107 1.82843 14.702 1.82843 14.1716V7C1.82843 5.93913 2.25086 4.92172 3.00289 4.16971C3.75493 3.4177 4.77234 2.99526 5.83321 2.99526H19C19.5304 2.99526 20.0391 3.20598 20.4142 3.58105C20.7893 3.95613 21 4.46487 21 4.99526V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span>Ask AI</span>
          </button>
        ) : (
          <div className="chatbot-window">
            <div className="chatbot-header">
              <div className="chatbot-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V17C3 16.4696 2.78929 15.9609 2.41421 15.5858C2.03914 15.2107 1.82843 14.702 1.82843 14.1716V7C1.82843 5.93913 2.25086 4.92172 3.00289 4.16971C3.75493 3.4177 4.77234 2.99526 5.83321 2.99526H19C19.5304 2.99526 20.0391 3.20598 20.4142 3.58105C20.7893 3.95613 21 4.46487 21 4.99526V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Textbook AI Assistant</span>
              </div>
              <div className="chatbot-actions">
                <button onClick={clearChat} className="chatbot-clear" title="Clear chat">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 6H5H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <button onClick={() => setIsExpanded(false)} className="chatbot-close" aria-label="Close chatbot">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>

            <div className="chatbot-messages">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  <div className="message-content">
                    {message.content.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <strong>Sources:</strong>
                      {message.sources.map((source, i) => (
                        <div key={i} className="source">
                          <span className="source-chapter">{source.chapter_id}</span>
                          {source.section_id && <span className="source-section"> • {source.section_id}</span>}
                        </div>
                      ))}
                    </div>
                  )}
                  <div className="message-time">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message assistant loading">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
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
                placeholder="Ask a question about the textbook..."
                disabled={isLoading}
                className="chatbot-input"
              />
              <button type="submit" disabled={isLoading || !input.trim()} className="chatbot-send">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </form>
          </div>
        )}
      </div>
    </>
  );
}

export default ChatbotWrapper;
