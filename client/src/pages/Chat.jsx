import { useState, useEffect } from 'react';

const ChatPage = () => {
  const [chatText, setChatText] = useState('');
  const [chatHistory, setChatHistory] = useState([]); // Store chat history
  const [selectedFile, setSelectedFile] = useState(null); // Track selected file

  // Fetch chat history from the database
  const pullChat = async () => {
    try {
      const response = await fetch('/chat-history', {
        method: 'GET',
      });
      if (response.ok) {
        const jsonData = await response.json();
        setChatHistory(jsonData); // Update chat history state, this will replace the old history
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

  // Send a new chat message with a file (if selected) to the database
  const sendChat = async () => {
    if (chatText.trim() !== '') {
      try {
        const formData = new FormData();
        formData.append('message', chatText);

        if (selectedFile) {
          formData.append('file', selectedFile); // Append the file if selected
        }

        const response = await fetch('/send-chat', {
          method: 'POST',
          body: formData, // Send the FormData containing both message and file
        });

        if (response.ok) {
          console.log('Chat sent successfully');
          setChatText(''); // Clear chat text after sending
          setSelectedFile(null); // Clear the selected file
          pullChat(); // Refresh chat history
        } else {
          console.error('Failed to send chat message');
        }
      } catch (error) {
        console.error('Error sending chat message:', error);
      }
    }
  };

  // Handle file upload
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]); // Set the selected file
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Welcome, Ask me anything</h1>

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
        {chatHistory.length > 0 ? (
          chatHistory.map((message, index) => (
            <div
              key={message.chat + index} // Use a unique key to avoid duplicate renders
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

      <div className="chat-form" style={{ marginTop: '20px' }}>
        <label
          htmlFor="chat-text-box"
          style={{ fontSize: '16px', marginRight: '10px' }}
        >
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

      <div className="file-upload" style={{ marginTop: '20px' }}>
        <input
          type="file"
          onChange={handleFileChange} // Handle file change event
          style={{
            marginBottom: '10px',
          }}
        />
      </div>
    </div>
  );
};

export default ChatPage;
