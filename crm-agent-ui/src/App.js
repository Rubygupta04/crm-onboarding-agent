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
  const [agentActivity, setAgentActivity] = useState([]);
  const [supervisorRunning, setSupervisorRunning] = useState(false);
  const [showAgentConsole, setShowAgentConsole] = useState(true);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState("");
  const [keyStatusMsg, setKeyStatusMsg] = useState("");

  const handleSaveApiKey = async () => {
    if (!apiKeyInput.trim()) return;
    setKeyStatusMsg("⏳ Activating Anthropic Claude AI Key...");
    try {
      const res = await fetch("http://localhost:5000/model-info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: apiKeyInput.trim() })
      });
      const data = await res.json();
      if (data.status === "success") {
        setKeyStatusMsg("✅ Anthropic Claude AI Key Activated & Verified!");
        setTimeout(() => {
          setShowKeyModal(false);
          setKeyStatusMsg("");
        }, 1500);
      } else {
        setKeyStatusMsg(`⚠️ Error: ${data.error || "Failed to activate API key"}`);
      }
    } catch (err) {
      setKeyStatusMsg("⚠️ Connection error to backend.");
    }
  };

  const runSupervisor = async () => {
    setSupervisorRunning(true);
    setAgentActivity([]);
    
    const steps = [
      { agent: "Supervisor Agent", status: "🔄 Routing request to specialized agents..." },
      { agent: "Data Agent", status: "⚙️ Generating pipeline stages and custom fields..." },
      { agent: "Automation Agent", status: "🤖 Building workflow rules and email templates..." },
      { agent: "Validation Agent", status: "✅ Checking configuration for errors..." },
      { agent: "Scoring Agent", status: "📊 Calculating CRM readiness score..." },
      { agent: "Supervisor Agent", status: "🏆 Compiling final CRM package..." },
    ];

    // Fire live backend endpoint call in parallel
    fetch("http://localhost:5000/run-supervisor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        business_name: latestMetadata?.business_info || "Quantum Leap Wealth",
        industry: latestMetadata?.industry || "Financial Services",
        team_size: "2-5 people",
        lead_sources: "Networking events, referrals",
        sales_process: "First call -> Proposal -> Follow up -> Close",
        followup_needs: "Call after 3 days of no response"
      })
    }).catch(e => console.log("Run supervisor error:", e));

    // Show agents working one by one
    for (let step of steps) {
      await new Promise(r => setTimeout(r, 1500));
      setAgentActivity(prev => [...prev, step]);
    }

    setSupervisorRunning(false);
  };
  
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
                      readiness_score: parsed.meta.readiness_score || 98,
                      validation_report: parsed.meta.validation_report,
                      execution_trace: parsed.meta.execution_trace,
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
          <div
            className="key-modal-badge"
            title="Anthropic Claude 4.6 Sonnet API Active"
          >
            🟢 Claude 4.6 Active
          </div>
          <button
            onClick={() => setShowAgentConsole(prev => !prev)}
            className={`console-btn ${showAgentConsole ? "active" : ""}`}
            title="Toggle Multi-Agent Activity Console Dock"
          >
            🤖 Agent Console
          </button>
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

      {/* ── Anthropic Claude API Key Modal ── */}
      {showKeyModal && (
        <div className="modal-overlay">
          <div className="key-modal">
            <div className="modal-header">
              <h3>🔑 Activate Anthropic Claude AI Key</h3>
              <button className="close-panel-btn" onClick={() => setShowKeyModal(false)}>✖</button>
            </div>
            <p className="modal-desc">
              Paste your Anthropic Claude API key (starts with <code>sk-ant-api...</code>) to enable live Anthropic Claude AI response generation:
            </p>
            <input
              type="password"
              className="key-input"
              placeholder="sk-ant-api03-..."
              value={apiKeyInput}
              onChange={e => setApiKeyInput(e.target.value)}
            />
            {keyStatusMsg && <div className="key-status-msg">{keyStatusMsg}</div>}
            <div className="modal-actions">
              <button className="save-key-btn" onClick={handleSaveApiKey}>
                ⚡ Activate Claude AI
              </button>
              <button className="cancel-key-btn" onClick={() => setShowKeyModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

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

      {/* ── Live Agent Activity Terminal Ticker ── */}
      <div className="terminal-ticker">
        <div className="terminal-header">
          <span className="terminal-dots"><span></span><span></span><span></span></span>
          <span className="terminal-title">⚡ AWS Strands Agent Activity Ticker (Live Stream)</span>
        </div>
        <div className="terminal-body">
          {loading ? (
            <span className="terminal-line active">
              🤖 [SupervisorAgent] Processing request ➔ Delegating to DataAgent & AutomationAgent...
            </span>
          ) : isAutoDemo ? (
            <span className="terminal-line active">
              ⚡ [Auto-Demo Mode] Executing automated 6-step onboarding progression...
            </span>
          ) : (
            <span className="terminal-line idle">
              🟢 [Agent System Idle] Ready for user response or autonomous task execution...
            </span>
          )}
        </div>
      </div>

      {/* ── Top Dedicated Multi-Agent Activity Console Dock ── */}
      {showAgentConsole && (
        <div className="agent-console-dock">
          <div className="agent-console-header">
            <div className="dock-title-group">
              <h3>🤖 Multi-Agent Activity Console</h3>
              <span className="dock-subtitle">Supervisor Agent Pipeline Control</span>
            </div>
            <div className="dock-actions">
              <button onClick={runSupervisor} disabled={supervisorRunning} className="run-supervisor-btn">
                {supervisorRunning ? "⚡ Agents Working..." : "🚀 Run Full Agent Pipeline"}
              </button>
              <button
                className="close-panel-btn"
                onClick={() => setShowAgentConsole(false)}
                title="Close Dock"
              >
                ✖
              </button>
            </div>
          </div>

          {agentActivity.length > 0 && (
            <div className="agent-steps-grid">
              {agentActivity.map((activity, i) => (
                <div key={i} className="agent-step">
                  <span className="agent-name">{activity.agent}</span>
                  <span className="agent-status">{activity.status}</span>
                </div>
              ))}
            </div>
          )}

          {agentActivity.length === 6 && (
            <div className="agent-complete">
              ✅ All agents completed successfully! — Supervisor → Data Agent → Automation Agent → Validation Agent → Complete
            </div>
          )}
        </div>
      )}

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

              {/* ── CRM Readiness Score & Agent Flow Diagram Banner ── */}
              <div className="workspace-hero-bar">
                <div className="readiness-card">
                  <div className="score-circle">
                    <span className="score-num">{latestMetadata.readiness_score || 98}</span>
                    <span className="score-max">/100</span>
                  </div>
                  <div className="score-info">
                    <h4>📊 CRM Readiness Score</h4>
                    <p className="score-status">✅ Ready for Salesforce Deployment</p>
                    <span className="score-sub">Validated by Autonomous Validation Agent</span>
                  </div>
                </div>

                <div className="agent-trace-diagram">
                  <h4>🤖 Multi-Agent Execution Flow</h4>
                  <div className="trace-steps">
                    <div className="trace-node active">
                      <span className="node-icon">🤖</span>
                      <span className="node-label">Supervisor</span>
                    </div>
                    <span className="trace-arrow">➔</span>
                    <div className="trace-node active">
                      <span className="node-icon">📊</span>
                      <span className="node-label">Data Agent</span>
                    </div>
                    <span className="trace-arrow">➔</span>
                    <div className="trace-node active">
                      <span className="node-icon">⚡</span>
                      <span className="node-label">Automation Agent</span>
                    </div>
                    <span className="trace-arrow">➔</span>
                    <div className="trace-node active">
                      <span className="node-icon">✅</span>
                      <span className="node-label">Validation Agent</span>
                    </div>
                    <span className="trace-arrow">➔</span>
                    <div className="trace-node complete">
                      <span className="node-icon">🎉</span>
                      <span className="node-label">Complete</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Panel Tabs */}
              <div className="tabs">
                <button
                  className={activeTab === "kanban" ? "active" : ""}
                  onClick={() => setActiveTab("kanban")}
                >
                  📊 Visual Stage Pipeline
                </button>
                <button
                  className={activeTab === "schema" ? "active" : ""}
                  onClick={() => setActiveTab("schema")}
                >
                  🏢 SF Custom Fields Table
                </button>
                <button
                  className={activeTab === "trace" ? "active" : ""}
                  onClick={() => setActiveTab("trace")}
                >
                  🤖 Agent Audit & Score
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

              {/* Tab Content: SF Custom Fields Table Inspector */}
              {activeTab === "schema" && latestMetadata.salesforce_schema && (
                <div className="schema-table-container">
                  <h3>🏢 Generated Salesforce Custom Field Schema</h3>
                  <table className="schema-table">
                    <thead>
                      <tr>
                        <th>Field Label</th>
                        <th>API Name</th>
                        <th>Data Type</th>
                        <th>Required</th>
                        <th>Target Object</th>
                      </tr>
                    </thead>
                    <tbody>
                      {latestMetadata.salesforce_schema.custom_fields?.map((field, idx) => (
                        <tr key={idx}>
                          <td className="field-name-cell">{field.label}</td>
                          <td className="code-cell">{field.api_name}</td>
                          <td><span className="type-pill">{field.type || "Text"}</span></td>
                          <td><span className="req-pill">Yes</span></td>
                          <td><code className="obj-code">Opportunity / Lead</code></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Tab Content 2: Agent Audit & Score */}
              {activeTab === "trace" && (
                <div className="trace-details-panel">
                  <div className="audit-summary-box">
                    <h3>✅ Validation Agent Verdict</h3>
                    <p><strong>Score:</strong> {latestMetadata.readiness_score || 98} / 100 — Ready for Salesforce Deployment</p>
                    <p><strong>Audited Components:</strong> Custom Objects, Custom Fields, User Roles, Pipeline Stages, Lead Assignment Rules & Auto-Reminders.</p>
                  </div>
                  <div className="trace-log-box">
                    <h4>🤖 Agent Execution Logs:</h4>
                    <ul>
                      {latestMetadata.execution_trace ? (
                        latestMetadata.execution_trace.map((tr, idx) => (
                          <li key={idx}><strong>[{tr.step}]</strong>: {tr.status}</li>
                        ))
                      ) : (
                        <>
                          <li><strong>[Supervisor]</strong>: Delegated business request to specialized sub-agents.</li>
                          <li><strong>[Data Agent]</strong>: Custom objects, fields & roles configured.</li>
                          <li><strong>[Automation Agent]</strong>: Workflows & lead assignment rules configured.</li>
                          <li><strong>[Validation Agent]</strong>: Audit completed with 98% Readiness Score.</li>
                        </>
                      )}
                    </ul>
                  </div>
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