import React, { useState } from 'react';
import axios from 'axios'; // Import axios for making HTTP requests

// to add: 
// 1. add a threadid variable to be sent to the server. It should start out as null, and be populated in the response by the server.

const SweetDreams = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const [summaryComplete, setSummaryComplete] = useState(false); // flag to check if the conversation with the editor in chief is complete

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const currentMessage = message;
    setMessage(''); // Clear input after sending
    
    try {
        // Using axios to make the HTTP POST request
        const response = await axios.post('http://localhost:3001/chat', {
        message: currentMessage
        });
        const responseData = response.data;
        const { reply: botReply, summaryComplete: summaryStatus } = responseData;
        setSummaryComplete(summaryStatus);
        console.log(responseData);

        setChatHistory([...chatHistory, { user: currentMessage, bot: botReply }]);

        if (summaryComplete) {
        // Do something when the conversation is complete
        console.log('Conversation complete');
        }
    } catch (error) {
      console.error('Error sending message:', error);
      // Handle error here, for example, by setting an error message in your state
    }
  };

  return (
    <div className="App">
      <h1>Welcome to SweetDreams</h1>
      <div className="chat-container">
        {chatHistory.map((entry, index) => (
          <div key={index}>
            <p><strong>You:</strong> {entry.user}</p>
            <p><strong>Bot:</strong> {entry.bot}</p>
          </div>
        ))}
        {summaryComplete && (
          <>
            <hr />
            <p>STARTING BOOK OUTLINE</p>
          </>
        )}
      </div>
      {!summaryComplete && (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={message}
            onChange={handleMessageChange}
            placeholder="Type a message..."
          />
          <button type="submit">Send</button>
        </form>
      )}
    </div>
  );
};

export default SweetDreams;
