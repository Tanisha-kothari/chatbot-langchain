import { useState } from "react";
import "./App.css";

function App() {
  // 🔹 State 1: input box
  const [message, setMessage] = useState("");

  // 🔹 State 2: chat history
  const [chat, setChat] = useState([]);

  const sessionID = localStorage.getItem("SID") || crypto.randomUUID();
  localStorage.setItem("SID", sessionID);

  // 🔹 Send message to backend
  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };

    // add user message first
    setChat((prev) => [...prev, userMsg]);



    try {
      const res = await fetch("https://chatbot-langchain-edl0.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
          "message": message,
          "SID" : sessionID })
      });

      const data = await res.json();

      const botMsg = { role: "bot", text: data.response };

      // add bot response
      setChat((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
    }

    setMessage("");
  };

  return (
    <div className="app">
      <h1>💬 AI Chatbot</h1>

      <div className="chat-box">
        {chat.map((msg, index) => (
          <div
            key={index}
            className={msg.role === "user" ? "user-msg" : "bot-msg"}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;