import { useState, useRef, useEffect } from "react";
import "./App.css";

const STEP_CHIPS = {
  1: [
    "Acme Consulting (Financial Services)",
    "HealthCare Plus (Healthcare)",
    "Apex Realty (Real Estate)",
    "Tech Studio (Technology)",
    "Hope Foundation (Nonprofit)"
  ],
  2: [
    "Just me (1 user)",
    "2-5 people",
    "6-10 people",
    "More than 10 people"
  ],
  3: [
    "Website & Online Forms",
    "Networking Events & Conferences",
    "Client Referrals",
    "Social Media & LinkedIn"
  ],
  4: [
    "Initial call -> Proposal -> Follow up -> Close",
    "Demo -> Trial / POC -> Contract Signed",
    "Property Showing -> Negotiation -> Closing"
  ],
  5: [
    "Send email weekly",
    "Call after 3 days of no response",
    "Check in monthly"
  ]
};

function App() {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      text: "👋 Welcome to NextWave CRM Onboarding Agent!\n\nI will help you set up Salesforce CRM perfectly for your business in just 5 questions!\n\nType 'hello' or click a prompt chip below to begin! 🚀"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [latestMetadata, setLatestMetadata] = useState(null);
  const [showWorkspace, setShowWorkspace] = useState(true);
  const [activeTab, setActiveTab] = useState("kanban"); // "kanban" | "emails" | "json"
  const [isAutoDemo, setIsAutoDemo] = useState(false);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [runningAgentTasks, setRunningAgentTasks] = useState(false);
  const [taskStatus, setTaskStatus] = useState("");
  
  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const autoDemoRef = useRef(false);
  const messagesRef = useRef(messages);
  const loadingRef = useRef(false);

  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  const handleRunAgentTasks = async () => {
    if (runningAgentTasks) return;
    setRunningAgentTasks(true);
    setCompletedTasks([]);
    setTaskStatus("🤖 Agent initiating autonomous task execution...");

    try {
      const res = await fetch("http://localhost:5000/run-agent-tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_name: latestMetadata?.business_info || "Quantum Leap Wealth"
        })
      });
      const data = await res.json();
      const tasksList = data.tasks || [];

      for (let i = 0; i < tasksList.length; i++) {
        await new Promise(r => setTimeout(r, 500));
        setCompletedTasks(prev => [...prev, tasksList[i]]);
      }
      setTaskStatus(data.status || "Agent completed all tasks!");

      // Add agent task completion summary into chat conversation
      setMessages(prev => [
        ...prev,
        {
          role: "agent",
          text: `🤖 **Autonomous Agent Task Execution Complete!**\n\n${tasksList.join("\n")}\n\n🎉 All custom CRM assets generated & configured!`
        }
      ]);
    } catch (err) {
      setTaskStatus("⚠️ Error executing autonomous agent tasks.");
    }
    setRunningAgentTasks(false);
  };

  const stopAutoDemo = () => {
    autoDemoRef.current = false;
    setIsAutoDemo(false);
  };

  const runAutoDemo = async () => {
    if (isAutoDemo) {
      stopAutoDemo();
      return;
    }

    handleReset();
    setIsAutoDemo(true);
    autoDemoRef.current = true;

    await new Promise(r => setTimeout(r, 600));

    const demoAnswers = [
      "Hello",
      "Quantum Leap Wealth - Financial Services",
      "3 team members",
      "Networking events and referrals",
      "First call then proposal then close",
      "Follow up every 3 days"
    ];

    for (let answer of demoAnswers) {
      if (!autoDemoRef.current) break;

      // Simulated character typing animation
      for (let charIdx = 1; charIdx <= answer.length; charIdx++) {
        if (!autoDemoRef.current) break;
        setInput(answer.slice(0, charIdx));
        await new Promise(r => setTimeout(r, 20));
      }

      if (!autoDemoRef.current) break;
      await new Promise(r => setTimeout(r, 300));
      if (!autoDemoRef.current) break;

      // Wait until any active loading finishes before sending next question
      while (loadingRef.current && autoDemoRef.current) {
        await new Promise(r => setTimeout(r, 100));
      }

      if (!autoDemoRef.current) break;

      await sendMessage(answer);
      setInput("");
      await new Promise(r => setTimeout(r, 1500));
    }

    if (autoDemoRef.current) {
      setIsAutoDemo(false);
      autoDemoRef.current = false;
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, latestMetadata, showWorkspace]);

  useEffect(() => {
    if (!loading) {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [loading]);

  const sendMessage = async (textToSend) => {
    const messageText = textToSend || input;
    if (!messageText.trim() || loadingRef.current) return;

    const userMessage = { role: "user", text: messageText };
    const currentMsgs = messagesRef.current;
    const newMessages = [...currentMsgs, userMessage];
    const msgsWithPlaceholder = [...newMessages, { role: "agent", text: "" }];
    
    // Add user message & initial placeholder agent message
    messagesRef.current = msgsWithPlaceholder;
    setMessages(msgsWithPlaceholder);
    setInput("");
    loadingRef.current = true;
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chat-stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: messageText,
          history: newMessages
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let accumulatedText = "";

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunkStr = decoder.decode(value, { stream: true });
          const lines = chunkStr.split("\n\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const parsed = JSON.parse(line.replace("data: ", ""));
                
                // Metadata Header
                if (parsed.meta) {
                  if (parsed.meta.step) setCurrentStep(parsed.meta.step);
                  if (parsed.meta.step === 6 && parsed.meta.pipeline) {
                    setLatestMetadata({
                      pipeline: parsed.meta.pipeline,
                      salesforce_schema: parsed.meta.salesforce_schema,
                      email_templates: parsed.meta.email_templates,
                      business_info: parsed.meta.business_info,
                      industry: parsed.meta.industry,
                      full_text: ""
                    });
                    setShowWorkspace(true);
                  }
                }
                
                // Streamed Text Chunk
                if (parsed.text) {
                  accumulatedText += parsed.text;
                  const currentText = accumulatedText;
                  setMessages(prev => {
                    const updated = [...prev];
                    updated[updated.length - 1] = { role: "agent", text: currentText };
                    messagesRef.current = updated;
                    return updated;
                  });
                  setLatestMetadata(prev => prev ? { ...prev, full_text: currentText } : null);
                }
              } catch (e) {
                // Ignore partial JSON parsing errors
              }
            }
          }
        }
      }
    } catch (error) {
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "agent",
          text: "⚠️ Connection error. Make sure backend is running on port 5000!"
        };
        messagesRef.current = updated;
        return updated;
      });
    } finally {
      loadingRef.current = false;
      setLoading(false);
    }
  };

  const handleReset = () => {
    stopAutoDemo();
    const initialMsgs = [
      {
        role: "agent",
        text: "👋 Session restarted! Welcome to NextWave CRM Onboarding Agent!\n\nI will help you set up Salesforce CRM perfectly for your business in just 5 questions!\n\nType 'hello' or choose an option below to start! 🚀"
      }
    ];
    messagesRef.current = initialMsgs;
    setMessages(initialMsgs);
    setCurrentStep(1);
    setLatestMetadata(null);
    setShowWorkspace(true);
    setInput("");
  };

  const downloadFile = (content, fileName, contentType) => {
    const a = document.createElement("a");
    const file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const exportMarkdownPlan = () => {
    if (!latestMetadata?.full_text) return;
    downloadFile(latestMetadata.full_text, "Salesforce_CRM_Onboarding_Plan.md", "text/markdown");
  };

  const exportJsonSchema = () => {
    if (!latestMetadata?.salesforce_schema) return;
    downloadFile(
      JSON.stringify(latestMetadata.salesforce_schema, null, 2),
      "salesforce_schema.json",
      "application/json"
    );
  };

  return (
    <div className="app">
      {/* ── Top Header ── */}
      <div className="header">
        <div className="header-logo">🤖</div>
        <div className="header-text">
          <h1>NextWave CRM Onboarding Agent</h1>
          <p>⚡ Powered by AWS Strands Agents + Claude AI</p>
        </div>
        <div className="header-actions">
          <button
            onClick={runAutoDemo}
            className={`auto-btn ${isAutoDemo ? "active" : ""}`}
            title="Watch Agent Work Automatically"
          >
            {isAutoDemo ? "⏹️ Stop Auto-Demo" : "▶️ Watch Agent Work Automatically"}
          </button>
          <button className="reset-btn" onClick={handleReset} title="Restart Onboarding">
            🔄 Reset Demo
          </button>
          <div className="header-badge">{isAutoDemo ? "AUTO" : "LIVE"}</div>
        </div>
      </div>

      {/* ── Progress Bar ── */}
      <div className="progress-container">
        <div className="progress-label">
          <span>
            Onboarding Progress
            {isAutoDemo && <span className="auto-demo-badge"> ⚡ Auto-Demo Running...</span>}
          </span>
          <span>{currentStep === 6 ? "Completed ✅" : `Step ${currentStep} of 5`}</span>
        </div>
        <div className="progress-bar-bg">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(100, ((currentStep - 1) / 5) * 100 || 5)}%` }}
          />
        </div>
      </div>

      {/* ── Main Chat Window ── */}
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === "agent" && <div className="avatar">🤖</div>}
            <div className="bubble">
              {msg.role === "agent" && !msg.text ? (
                <div className="typing">
                  <span></span><span></span><span></span>
                </div>
              ) : (
                msg.text.split('\n').map((line, j) => (
                  <span key={j}>{line}<br /></span>
                ))
              )}
            </div>
            {msg.role === "user" && <div className="avatar">👤</div>}
          </div>
        ))}

        {/* ── Interactive Results Workspace Panel ── */}
        {latestMetadata && (
          showWorkspace ? (
            <div className="results-panel">
              <div className="results-header">
                <h3>🎯 Generated CRM Setup Workspace</h3>
                <div className="export-buttons">
                  <button
                    className="export-btn agent-do-all"
                    onClick={handleRunAgentTasks}
                    disabled={runningAgentTasks}
                    title="Execute all autonomous setup tasks"
                  >
                    {runningAgentTasks ? "⏳ Executing Workflows..." : "⚡ Execute Agent Workflows & Tasks"}
                  </button>
                  <button className="export-btn md" onClick={exportMarkdownPlan}>
                    📥 Download Plan (.md)
                  </button>
                  <button className="export-btn json" onClick={exportJsonSchema}>
                    ⚙️ Export SF Schema (.json)
                  </button>
                  <button className="close-panel-btn" onClick={() => setShowWorkspace(false)} title="Close Workspace Panel">
                    ✖
                  </button>
                </div>
              </div>

              {/* Autonomous Agent Task Execution Console */}
              {(runningAgentTasks || completedTasks.length > 0) && (
                <div className="agent-tasks-console">
                  <div className="console-header">
                    <h4>🤖 Autonomous Agent Task Execution Console</h4>
                    {runningAgentTasks && <span className="running-spinner">⚡ Agent Working...</span>}
                  </div>
                  <div className="task-list">
                    {completedTasks.map((t, idx) => (
                      <div key={idx} className="task-item">
                        {t}
                      </div>
                    ))}
                  </div>
                  {taskStatus && <div className="task-status-bar">{taskStatus}</div>}
                </div>
              )}

              {/* Panel Tabs */}
              <div className="tabs">
                <button
                  className={activeTab === "kanban" ? "active" : ""}
                  onClick={() => setActiveTab("kanban")}
                >
                  📊 Visual Stage Pipeline
                </button>
                <button
                  className={activeTab === "emails" ? "active" : ""}
                  onClick={() => setActiveTab("emails")}
                >
                  📧 AI Sales Email Templates
                </button>
                <button
                  className={activeTab === "json" ? "active" : ""}
                  onClick={() => setActiveTab("json")}
                >
                  🛠 Salesforce Schema JSON
                </button>
              </div>

              {/* Tab Content 1: Kanban Board */}
              {activeTab === "kanban" && latestMetadata.pipeline && (
                <div className="kanban-board">
                  {latestMetadata.pipeline.map((stage, idx) => (
                    <div key={idx} className="kanban-card">
                      <div className="card-number">Stage {idx + 1}</div>
                      <div className="card-title">{stage}</div>
                      <div className="card-badge">Active</div>
                    </div>
                  ))}
                </div>
              )}

              {/* Tab Content 2: AI Email Templates */}
              {activeTab === "emails" && latestMetadata.email_templates && (
                <div className="email-templates-grid">
                  {latestMetadata.email_templates.map((tmpl, idx) => (
                    <div key={idx} className="email-card">
                      <h4>{tmpl.title}</h4>
                      <p className="email-subject"><strong>Subject:</strong> {tmpl.subject}</p>
                      <pre className="email-body">{tmpl.body}</pre>
                      <button
                        className="copy-btn"
                        onClick={() => navigator.clipboard.writeText(`Subject: ${tmpl.subject}\n\n${tmpl.body}`)}
                      >
                        📋 Copy Template
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Tab Content 3: JSON Schema */}
              {activeTab === "json" && latestMetadata.salesforce_schema && (
                <div className="json-preview">
                  <pre>{JSON.stringify(latestMetadata.salesforce_schema, null, 2)}</pre>
                </div>
              )}
            </div>
          ) : (
            <div className="workspace-reopen-bar">
              <button className="reopen-btn" onClick={() => setShowWorkspace(true)}>
                📊 Re-open Generated CRM Setup Workspace
              </button>
            </div>
          )
        )}

        <div ref={bottomRef} />
      </div>

      {/* ── Quick Suggestion Chips ── */}
      {currentStep <= 5 && STEP_CHIPS[currentStep] && (
        <div className="suggestion-chips">
          <span className="chips-label">Quick Suggestions:</span>
          {STEP_CHIPS[currentStep].map((chip, idx) => (
            <button
              key={idx}
              className="chip-btn"
              onClick={() => sendMessage(chip)}
              disabled={loading}
            >
              {chip}
            </button>
          ))}
        </div>
      )}

      {/* ── Input Bar ── */}
      <div className="input-area">
        <input
          ref={inputRef}
          type="text"
          autoFocus
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === "Enter" && sendMessage()}
          placeholder={currentStep <= 5 ? `Answer Question ${currentStep} or type a custom answer...` : "Ask any follow-up question..."}
          disabled={loading}
        />
        <button onClick={() => sendMessage()} disabled={loading}>
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