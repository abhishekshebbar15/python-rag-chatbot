import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Automatically scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async (text = message) => {
    if (!text.trim() || loading) return;

    const userMessage = text.trim();
    const lowerMessage = userMessage.toLowerCase();

    const greetings = {
      hello: "Hello! 👋",
      hi: "Hi! 👋",
      hey: "Hey! 👋",
      "good morning": "Good morning! ☀️",
      "good afternoon": "Good afternoon! 🌤️",
      "good evening": "Good evening! 🌆",
      bye: "Bye! 👋",
      goodbye: "Goodbye! 👋",
    };

    // Handle greetings locally
    if (greetings[lowerMessage]) {
      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: userMessage,
        },
        {
          role: "assistant",
          content: greetings[lowerMessage],
        },
      ]);

      setMessage("");
      return;
    }

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      // CONNECT TO DEPLOYED FASTAPI BACKEND
      const response = await fetch(
        "https://python-rag-chatbot.vercel.app/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Backend request failed: ${response.status}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error("Backend error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ Unable to connect to the RAG backend. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const suggestions = [
    "What is inheritance?",
    "What is polymorphism?",
    "What is encapsulation?",
  ];

  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">🐍</div>

          <div>
            <h2>Python RAG</h2>
            <span>Knowledge Assistant</span>
          </div>
        </div>

        <button
          className="new-chat"
          onClick={clearChat}
        >
          <span>＋</span>
          New Chat
        </button>

        <div className="sidebar-section">
          <p className="section-title">KNOWLEDGE BASE</p>

          <div className="knowledge-card">
            <div className="knowledge-icon">📚</div>

            <div>
              <strong>Python Documentation</strong>
              <span>RAG Knowledge Base</span>
            </div>
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="status">
            <span className="status-dot"></span>
            RAG Online
          </div>

          <p>Powered by FAISS + Ollama</p>
        </div>

      </aside>


      {/* ================= MAIN ================= */}
      <main className="main">

        {/* HEADER */}
        <header className="topbar">

          <div className="mobile-brand">
            <div className="brand-icon">🐍</div>

            <div>
              <h2>Python RAG</h2>
              <span>Knowledge Assistant</span>
            </div>
          </div>

          <div className="topbar-info">

            <div className="online-indicator">
              <span></span>
              RAG Online
            </div>

            <button
              className="clear-button"
              onClick={clearChat}
              title="Clear conversation"
            >
              🗑️
            </button>

          </div>

        </header>


        {/* CHAT AREA */}
        <section className="chat-area">

          {messages.length === 0 ? (

            /* ================= WELCOME SCREEN ================= */
            <div className="welcome">

              <div className="welcome-icon">
                🤖
              </div>

              <h1>
                Welcome to <span>Python RAG</span>
              </h1>

              <p>
                Ask questions about Python using information
                retrieved from your knowledge base.
              </p>

              <div className="suggestions">

                {suggestions.map((question, index) => (

                  <button
                    key={index}
                    className="suggestion"
                    onClick={() => sendMessage(question)}
                  >

                    <span>
                      {index === 0
                        ? "🧬"
                        : index === 1
                        ? "🔄"
                        : "🔒"}
                    </span>

                    {question}

                    <b>→</b>

                  </button>

                ))}

              </div>

            </div>

          ) : (

            /* ================= CHAT ================= */
            <div className="messages">

              {messages.map((msg, index) => (

                <div
                  key={index}
                  className={`message-row ${
                    msg.role === "user"
                      ? "user-row"
                      : "assistant-row"
                  }`}
                >

                  {msg.role === "assistant" && (
                    <div className="avatar assistant-avatar">
                      🤖
                    </div>
                  )}

                  <div
                    className={`message-bubble ${
                      msg.role === "user"
                        ? "user-bubble"
                        : "assistant-bubble"
                    }`}
                  >
                    {msg.content}
                  </div>

                  {msg.role === "user" && (
                    <div className="avatar user-avatar">
                      👤
                    </div>
                  )}

                </div>

              ))}


              {/* LOADING */}
              {loading && (

                <div className="message-row assistant-row">

                  <div className="avatar assistant-avatar">
                    🤖
                  </div>

                  <div className="message-bubble assistant-bubble loading-bubble">

                    <span>Thinking</span>

                    <div className="typing">
                      <i></i>
                      <i></i>
                      <i></i>
                    </div>

                  </div>

                </div>

              )}

              <div ref={messagesEndRef}></div>

            </div>

          )}

        </section>


        {/* INPUT AREA */}
        <footer className="input-area">

          <div className="input-container">

            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something about Python..."
              rows="1"
              disabled={loading}
            />

            <button
              className="send-button"
              onClick={() => sendMessage()}
              disabled={!message.trim() || loading}
            >
              {loading ? "..." : "➤"}
            </button>

          </div>

          <p className="input-hint">
            Enter to send • Shift + Enter for new line
          </p>

        </footer>

      </main>

    </div>
  );
}

export default App;