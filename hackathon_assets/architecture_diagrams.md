# 📊 Architecture & Workflow Diagrams

## NextWave Autonomous CRM Onboarding Platform
**Agents for Humans Hackathon 2026 Presentation Package**

---

## 1. Multi-Agent Orchestration Flowchart

This diagram illustrates how the **Supervisor Agent** coordinates work between specialized sub-agents and produces validated Salesforce configurations with human oversight.

```mermaid
flowchart TD
    User([👤 User / Business Owner]) -->|Answers 5 Guided Questions| AppUI[💻 React 19 Command Center]
    AppUI -->|POST /chat-stream| Backend[🐍 Flask + AWS Strands Engine]
    
    subgraph MultiAgentEngine["🤖 Multi-Agent Orchestration Core"]
        Supervisor["🤖 SUPERVISOR AGENT\n(AWS Strands SDK + Claude AI)"]
        
        Supervisor -->|1. Request Schema & Pipeline| DataAgent["📊 Data Agent\n(Objects, Fields, Roles)"]
        Supervisor -->|2. Request Workflows & Reminders| AutoAgent["⚡ Automation Agent\n(Rules, Email Templates)"]
        Supervisor -->|3. Request Quality Audit| ValAgent["✅ Validation Agent\n(Quality Audit & Verification)"]
        Supervisor -->|4. Request Readiness Assessment| ScoreAgent["📈 Scoring Agent\n(CRM Readiness Score /100)"]
        
        DataAgent -->|Return Custom Fields & Stages| Supervisor
        AutoAgent -->|Return Workflows & Templates| Supervisor
        ValAgent -->|Return Audit Report & Verification| Supervisor
        ScoreAgent -->|Return Score 98/100| Supervisor
    end
    
    Backend --> MultiAgentEngine
    MultiAgentEngine -->|Streamed Plan + Schema JSON| AppUI
    
    AppUI -->|Interactive Review| HumanApproval{👤 Human Approval & Review}
    HumanApproval -->|⚡ Execute Agent Tasks| SalesforcePackage["📦 Salesforce Deployment Package\n(JSON Schema / CSV / Markdown Plan)"]
```

---

## 2. System Architecture Diagram

This diagram shows the complete full-stack architecture of the platform, from the front-end dashboard down to AWS Bedrock and evaluation benchmarks.

```mermaid
graph TB
    subgraph Frontend["💻 Frontend Layer (React 19 + Vanilla CSS)"]
        UI["App.js Command Dashboard"]
        Ticker["⚡ Live Terminal Ticker"]
        ScoreCard["📊 98/100 Readiness Card"]
        Inspector["🏢 SF Custom Fields Inspector"]
        Dock["🤖 Top Agent Console Dock"]
    end

    subgraph API["🔌 API Layer (Flask Server - Port 5000)"]
        ChatStream["POST /chat-stream (Server-Sent Events)"]
        AgentTasks["POST /run-agent-tasks"]
        SupervisorEndpoint["POST /run-supervisor"]
    end

    subgraph AgentCore["⚡ AWS Strands Agent Engine (crm_engine.py / supervisor.py)"]
        StrandsSupervisor["Supervisor Agent"]
        DataSubAgent["Data Architecture Agent"]
        AutoSubAgent["Automation & Rules Agent"]
        ValSubAgent["Validation & Quality Agent"]
        ScoreSubAgent["Scoring Agent"]
        Hooks["CRMAgentHooks (Lifecycle Events)"]
    end

    subgraph AICloud["☁️ Cloud AI Foundation (AWS Bedrock)"]
        Bedrock["Amazon Bedrock\n(Anthropic Claude Sonnet 3.5 / 4.0)"]
    end

    subgraph Benchmarks["🧪 Evaluation & Benchmark Suite (eval_scenarios.py)"]
        Scenarios["5 Real-World Scenarios\n(Wealth, Health, Realty, Nonprofit, SaaS)"]
        EvalResults["eval_results.json\n(100% Pass Rate | 96.8 Avg Score)"]
    end

    Frontend -->|HTTP / SSE| API
    API --> AgentCore
    AgentCore --> Hooks
    AgentCore -->|Converse API| Bedrock
    Benchmarks -->|Audit & Validate| AgentCore
```

---

## 3. Data Flow & Transformation Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Business Owner
    participant UI as 💻 React Command Center
    participant Server as 🐍 Flask Backend
    participant Sup as 🤖 Supervisor Agent
    participant Data as 📊 Data Agent
    participant Auto as ⚡ Automation Agent
    participant Val as ✅ Validation Agent
    participant SF as 📦 Salesforce Output

    User->>UI: Types "Quantum Leap Wealth" (5 Qs)
    UI->>Server: POST /chat-stream (message + history)
    Server->>Sup: Delegate Business Profile
    
    activate Sup
    Sup->>Data: Generate Pipelines & Custom Fields
    Data-->>Sup: Return 7 Stages + 6 Custom Fields
    
    Sup->>Auto: Generate Workflows & Emails
    Auto-->>Sup: Return 7 Automations + 3 Templates
    
    Sup->>Val: Audit Configuration & Calculate Score
    Val-->>Sup: Return 98/100 Readiness Verdict
    deactivate Sup

    Sup-->>Server: Complete Multi-Agent Response
    Server-->>UI: Streamed Words + Meta JSON (SSE)
    
    UI->>User: Displays 98/100 Score, SF Field Table & Email Templates
    User->>UI: Clicks "⚡ Execute Agent Workflows & Tasks"
    UI->>SF: Generates Salesforce Setup Package (.json & .md)
```

---

## 4. Evaluation Benchmark Suite Overview

```mermaid
gantt
    title 🧪 Evaluation Benchmark Suite Results (100% Pass Rate)
    dateFormat  X
    axisFormat %s

    section Scenarios Tested
    Quantum Leap Wealth (Financial)  :active, q1, 0, 98
    GreenCare Health (Healthcare)     :active, q2, 0, 96
    RealtyPros Direct (Real Estate)  :active, q3, 0, 97
    Hope Foundation (Nonprofit)      :active, q4, 0, 95
    SaaS Tech Studio (Technology)    :active, q5, 0, 98
```

---

## 💡 How to Use These Diagrams in Your Hackathon Presentation

1. **For Devpost / GitHub README**: Copy the Mermaid code blocks directly into your markdown — Devpost and GitHub render Mermaid natively!
2. **For Slide Deck / Presentation**: Take a screenshot of these diagrams or copy the text structure into Google Slides / PowerPoint.
3. **During Pitch**:
   - Show Diagram #1 when explaining **"Why Multi-Agent?"**
   - Show Diagram #2 when judges ask **"What tech stack did you use?"**
   - Show Diagram #4 when judges ask **"Did you test it on real scenarios?"**
