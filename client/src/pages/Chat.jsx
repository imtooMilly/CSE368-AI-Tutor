import { useState, useEffect } from 'react';

const ChatPage = () => {
  const [chatText, setChatText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);  // Store chat history

  // Fetch chat history from the database
  const pullChat = async () => {
    try {
      const response = await fetch('/chat-history', {
        method: 'GET',
      });
      if (response.ok) {
        const jsonData = await response.json();
        setChatHistory(jsonData);  // Update chat history state, this will replace the old history
      } else {
        console.error('Failed to fetch chat history');
      }
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  // Call pullChat when the component is mounted
  useEffect(() => {
    pullChat();
  }, []);

  // Send a new chat message to the database
  const sendChat = async () => {
    if (chatText.trim() !== '') {
      try {
        const response = await fetch('/send-chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: chatText }),
        });
        if (response.ok) {
          console.log("Chat sent successfully");
          setChatText(''); 
          pullChat(); 
        } else {
          console.error('Failed to send chat message');
        }
      } catch (error) {
        console.error('Error sending chat message:', error);
      }
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Welcome, Ask me anything</h1>

      {/* Chat messages section */}
      <div
        id="chat-messages"
        style={{
          marginBottom: '20px',
          padding: '10px',
          maxWidth: '600px',
          margin: '0 auto',
          border: '1px solid #ccc',
          borderRadius: '4px',
          height: '300px',
          overflowY: 'auto',
        }}
      >
        {/* Render each chat message */}
        {chatHistory.length > 0 ? (
          chatHistory.map((message, index) => (
            <div
              key={message.chat + index}  // Use a unique key to avoid duplicate renders
              style={{
                marginBottom: '10px',
                padding: '5px',
                borderBottom: '1px solid #ddd',
                fontSize: '14px',
              }}
            >
              <strong>{message.creatorID}:</strong>
              <p>{message.chat}</p>
            </div>
          ))
        ) : (
          <p>No chat history found</p>
        )}
      </div>

      {/* Input field and Send button */}
      <div className="chat-form" style={{ marginTop: '20px' }}>
        <label htmlFor="chat-text-box" style={{ fontSize: '16px', marginRight: '10px' }}>
          Chat:
        </label>
        <input
          id="chat-text-box"
          type="text"
          value={chatText}
          onChange={(e) => setChatText(e.target.value)}
          style={{
            padding: '10px',
            fontSize: '16px',
            marginRight: '10px',
            width: '300px',
            border: '1px solid #ccc',
            borderRadius: '4px',
          }}
        />
        <button
          onClick={sendChat}
          style={{
            padding: '10px 20px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatPage;