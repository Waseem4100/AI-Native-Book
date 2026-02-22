import React from 'react';
import Chatbot from './Chatbot';
import './chatbot.css';

export default function Root({ children }) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
