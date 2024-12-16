import React, { useState, useEffect } from 'react';

const ChatPage = () => {
  const [chatText, setChatText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  // Function to fetch the chat history from Flask API
  const pullChat = async () => {
    try {
      const response = await fetch('/chat-history', {
        method: 'GET',
      });
      if (response.ok) {
        const jsonData = await response.json();
        setChatHistory(jsonData); // Set the chat history state
      }
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  // Call pullChat when the component is mounted to fetch chat history
  useEffect(() => {
    pullChat();
  }, []);

  const sendChat = () => {
    if (chatText.trim() !== '') {
      console.log(chatText); // You can log or send the chat text to a server
      setChatText(''); // Clear the input field after sending
    }
  };

  return (
    <div>
      <h1>Welcome, Ask me anything</h1>

      <div id="chat-messages">
        {/* Render the chat history */}
        {chatHistory.map((message, index) => (
          <div key={index}>{message}</div>
        ))}
      </div>

      <div className="chat-form">
        <hr />
        <label>
          Chat:
          <input
            id="chat-text-box"
            type="text"
            value={chatText}
            onChange={(e) => setChatText(e.target.value)}
          />
        </label>
        <button onClick={sendChat}>Send</button>
      </div>
    </div>
  );
};

export default ChatPage;