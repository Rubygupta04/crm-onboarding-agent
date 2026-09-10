import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      text: "👋 Welcome to NextWave CRM Onboarding Agent!\n\nI will help you set up Salesforce CRM perfectly for your business in just 5 questions!\n\nType 'hello' to begin! 🚀"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          history: newMessages
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, {
        role: "agent",
        text: data.response
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: "agent",
        text: "⚠️ Connection error. Make sure backend is running on port 5000!"
      }]);
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <div className="header">
        <div className="header-logo">🤖</div>
        <div className="header-text">
          <h1>NextWave CRM Onboarding Agent</h1>
          <p>⚡ Powered by AWS Strands Agents + Claude AI</p>
        </div>
        <div className="header-badge">LIVE</div>
      </div>

      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === "agent" && <div className="avatar">🤖</div>}
            <div className="bubble">
              {msg.text.split('\n').map((line, j) => (
                <span key={j}>{line}<br /></span>
              ))}
            </div>
            {msg.role === "user" && <div className="avatar">👤</div>}
          </div>
        ))}
        {loading && (
          <div className="message agent">
            <div className="avatar">🤖</div>
            <div className="bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === "Enter" && sendMessage()}
          placeholder="Type your message here..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send →"}
        </button>
      </div>

      <div className="footer">
        NextWave Tech Studio • dnextwave.com • Agents for Humans Hackathon 2026
      </div>
    </div>
  );
}

export default App;