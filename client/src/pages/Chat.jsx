import { useState } from "react";
import axios from 'axios'

const ChatPage = () => {
    const [chatText, setChatText] = useState('');

    async function pullChat(){
        try {
          const response = await fetch('/chat-history', {
            method: 'GET',
        });
        if(response.ok){
          const jsonData = await response.json();
          setChat(jsonData);
        }
      } catch (error) {
        console.error('Error fetching chat history:', error)
        }
      }
  
    const sendChat = () => {
      if (chatText.trim() !== '') {
        console.log(chatText); // You can log or send the chat text to a server
        setChatText(''); // Clear the input field after sending
      }
    };
  
    return (
      <div>
        <h1>Welcome, Ask me anything</h1>
        
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