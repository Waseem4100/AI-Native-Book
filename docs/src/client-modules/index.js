import React from 'react';
import { ChatbotWrapper } from './theme/ChatbotWrapper';

export function onRouteDidUpdate({ location, previousLocation }) {
  // Don't execute if we're still on the same page
  if (location.pathname !== previousLocation?.pathname) {
    // Inject chatbot into the page
    const existingChatbot = document.getElementById('docusaurus-chatbot');
    if (!existingChatbot) {
      const chatbotContainer = document.createElement('div');
      chatbotContainer.id = 'docusaurus-chatbot';
      document.body.appendChild(chatbotContainer);

      // Use React to render the chatbot
      const root = document.createElement('div');
      chatbotContainer.appendChild(root);
      
      // This is a simple approach - in production, you'd want to use
      // a proper Docusaurus theme component
    }
  }
}
