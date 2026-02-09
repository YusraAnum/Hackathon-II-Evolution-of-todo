// src/components/ChatMessage.js
import React from 'react';

export const ChatMessage = ({ message }) => {
  const { role, content } = message;
  
  return (
    <div className={`message ${role}`}>
      <div className="message-content">
        {content}
      </div>
    </div>
  );
};