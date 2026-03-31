import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  // ------------------ State ------------------
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  // ------------------ Stable Session ID ------------------
  const [sessionID] = useState(() => {
    const existing = localStorage.getItem("SID");
    if (existing) return existing;

    const newID = crypto.randomUUID();
    localStorage.setItem("SID", newID);
    return newID;
  });

  // ------------------ Auto Scroll ------------------
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  // ------------------ Send Message ------------------
  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };

    setChat((prev) => [...prev, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("https://chatbot-langchain-edl0.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message,
          sid: sessionID   // ✅ fixed key
        })
      });

      const data = await res.json().catch(() => null);

      if (!data || !data.response) {
        throw new Error("Invalid response");
      }

      const botMsg = { role: "bot", text: data.response };

      setChat((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error(error);

      setChat((prev) => [
        ...prev,
        { role: "bot", text: "Something went wrong 😅" }
      ]);
    }

    setLoading(false);
  };

  // ------------------ UI ------------------
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

        {loading && <div className="bot-msg">Typing...</div>}

        <div ref={chatEndRef} />
      </div>

      <div className="input-box">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;