# 🎤 Hackathon Presentation Deck & Pitch Script
## NextWave Autonomous CRM Onboarding Platform
**Agents for Humans Hackathon 2026 Pitch Deck**
*Total Timing: 2 Minutes 30 Seconds Pitch + Q&A*

---

## 📋 Presentation Overview at a Glance

| Slide # | Slide Title | Timing | Core Message |
|---|---|---|---|
| **Slide 1** | Title & Hook | 0:00 - 0:20 | Introducing NextWave: Autonomous CRM setup powered by AWS Strands Agents. |
| **Slide 2** | The Problem | 0:20 - 0:45 | Small businesses fail at CRM onboarding — 68% give up due to setup complexity. |
| **Slide 3** | The Solution | 0:45 - 1:10 | Not just a chatbot — an autonomous multi-agent operational platform. |
| **Slide 4** | Multi-Agent Architecture | 1:10 - 1:35 | Supervisor routing work to specialized Data, Automation, Validation & Scoring agents. |
| **Slide 5** | Live Demo Walkthrough | 1:35 - 2:00 | Guided 5-question interview to 98/100 Readiness Score & Salesforce Custom Fields Table. |
| **Slide 6** | Evaluation Benchmarks | 2:00 - 2:15 | 100% Pass Rate across 5 industry scenarios with 96.8/100 average quality score. |
| **Slide 7** | Tech Stack & AWS Strands | 2:15 - 2:30 | AWS Strands SDK, Bedrock Claude AI, React 19, Flask Server, Agent Hooks. |
| **Slide 8** | Q&A & Key Takeaway | — | "Why build custom when ChatGPT exists?" — Deterministic Salesforce JSON schema execution. |

---

## 🎨 Slide Content & Speaker Scripts

### 📍 Slide 1: Title & Hook
**Visual Layout**: Dark futuristic theme with glowing blue/green accents, NextWave logo, and taglines.

- **Title**: NextWave CRM Onboarding Agent
- **Subtitle**: Transforming CRM Setup from Weeks of Manual Work to 3 Minutes of Autonomous AI Operations
- **Event**: Agents for Humans Hackathon 2026
- **Tagline**: *Powered by AWS Strands SDK + Amazon Bedrock Claude AI*

> 🎙️ **Speaker Script (20s)**:
> *"Hello judges! Every year, millions of small business owners purchase CRM software like Salesforce to grow their sales. But over 68% of them struggle with setup — custom fields, pipelines, lead assignment, and email templates take weeks of technical consulting. Today, we’re showing you **NextWave CRM Onboarding Agent**: an autonomous multi-agent platform that turns a 5-minute conversation into a production-ready Salesforce configuration!"*

---

### 📍 Slide 2: The Problem
**Visual Layout**: Split layout comparing "Traditional CRM Setup" vs "The Friction Point".

- **The CRM Onboarding Crisis**:
  - 🛑 **High Complexity**: Setting up custom objects, picklists, and workflows requires expensive consultants ($150–$300/hr).
  - 🛑 **Generic Chatbots Fall Short**: Standard AI chatbots just give text advice — they don't generate actual database schemas or audit configurations for errors.
  - 🛑 **Time-to-Value Delay**: Teams spend 2 to 4 weeks onboarding before sending their first email.

> 🎙️ **Speaker Script (25s)**:
> *"Why do small businesses give up on CRMs? Because standard AI chatbots like ChatGPT give advice, but they don't DO the work. Creating custom fields, configuring lead assignment, and verifying data accuracy requires specialized domain expertise across database architecture, workflow triggers, and quality validation. Businesses don't need another generic chat widget — they need an operational multi-agent team."*

---

### 📍 Slide 3: The Solution
**Visual Layout**: Hero screenshot of the React Command Center with live terminal ticker and 98/100 Readiness Card.

- **NextWave Solution**:
  - 🎯 **Guided 5-Question Interview**: Simple conversation tailored to business name, industry, team size, lead sources, and follow-up style.
  - 📊 **CRM Readiness Score (98/100)**: Instant automated quality audit and readiness rating.
  - 🏢 **Salesforce Custom Fields Table Inspector**: Enterprise data table rendering API names (`lead_source__c`), field types, and object targets.
  - ⚡ **Autonomous Execution**: One-click execution generating Salesforce-ready JSON schemas and AI email templates.

> 🎙️ **Speaker Script (25s)**:
> *"Enter NextWave! Our platform conducts a brief guided 5-question interview with the business owner. In under 3 minutes, our autonomous agent team designs an industry-specific Salesforce pipeline, configures custom fields, sets up automated lead assignment rules, and audits the entire setup for errors — issuing an immediate 98/100 CRM Readiness Score."*

---

### 📍 Slide 4: Multi-Agent Architecture
**Visual Layout**: Embedded Mermaid flowchart of Supervisor ➔ Sub-Agents.

- **Orchestration Architecture**:
  ```
          🤖 SUPERVISOR AGENT
                   │
    ┌──────────────┼──────────────┬──────────────┐
    ↓              ↓              ↓              ↓
  📊 Data     ⚡ Automation   ✅ Validation  📈 Scoring
   Agent          Agent          Agent          Agent
  (Fields)      (Rules)        (Audit)        (Score)
  ```
- **Specialized Roles**:
  1. `Supervisor Agent`: Receives user input and coordinates specialized agent delegation.
  2. `Data Agent`: Builds industry pipelines (Healthcare, Finance, Real Estate) and field schemas.
  3. `Automation Agent`: Configures stale deal alerts, lead assignment, and AI email templates.
  4. `Validation Agent`: Audits for naming conflicts, duplicate stages, and compliance errors.
  5. `Scoring Agent`: Calculates quantitative CRM readiness score out of 100.

> 🎙️ **Speaker Script (25s)**:
> *"Here is how our engine works under the hood. We built a true multi-agent system using the AWS Strands SDK. A **Supervisor Agent** coordinates four specialized sub-agents: the **Data Agent** generates custom fields and stages; the **Automation Agent** writes workflow rules; the **Validation Agent** checks for data conflicts; and the **Scoring Agent** calculates the readiness score. Every agent action is monitored via real-time lifecycle hooks!"*

---

### 📍 Slide 5: Live Demo Walkthrough
**Visual Layout**: 4 key UI feature callouts (Auto-Demo Mode, Terminal Ticker, Workspace Tabs, Multi-Agent Console).

- **Key Highlights to Show Judges**:
  - ▶️ **Watch Agent Work Automatically**: One-click animated auto-demo.
  - ⚡ **Live AWS Strands Activity Ticker**: Real-time terminal streaming of agent thought execution.
  - 🏢 **Salesforce Custom Fields Table**: Direct inspector tab for API names and data types.
  - 🤖 **Top Multi-Agent Activity Console**: Visual progression from Supervisor to Completion.

> 🎙️ **Speaker Script (25s)**:
> *"Let's see it in action! [Click 'Watch Agent Work Automatically']. Notice how our Live AWS Strands Terminal Ticker streams agent activity in real time. Once complete, our workspace unlocks visual pipeline kanban stages, AI email templates, and our dedicated Salesforce Custom Fields Table inspector. With one click on '⚡ Execute Agent Workflows', the business owner exports a validated `salesforce_schema.json` ready for direct API import!"*

---

### 6: Evaluation Benchmarks
**Visual Layout**: Summary table of evaluation scenario results.

- **Benchmark Suite Results (`eval_scenarios.py`)**:
  - 🧪 **5 Diverse Scenarios Tested**: Financial Services, Healthcare, Real Estate, Nonprofit, Tech SaaS.
  - 🎯 **100% Pass Rate**: All 5 test scenarios achieved `READY FOR DEPLOYMENT` status.
  - 📈 **96.8 / 100 Average Score**: Consistently high quality configuration across industries.

| Business Scenario | Industry | Status | Score |
|---|---|---|---|
| Quantum Leap Wealth | Financial Services | ✅ PASS | 98/100 |
| GreenCare Health | Healthcare | ✅ PASS | 96/100 |
| RealtyPros Direct | Real Estate | ✅ PASS | 97/100 |
| Hope Foundation | Nonprofit | ✅ PASS | 95/100 |
| SaaS Tech Studio | Technology | ✅ PASS | 98/100 |

> 🎙️ **Speaker Script (15s)**:
> *"To prove reliability, we built an automated evaluation suite testing 5 real-world business scenarios spanning Healthcare to Real Estate. NextWave achieved a 100% pass rate with a 96.8/100 average quality score across all benchmarks!"*

---

### 📍 Slide 7: Tech Stack & Technical Excellence
**Visual Layout**: Icons / boxes for AWS Strands SDK, Bedrock, React 19, Flask.

- **Tech Stack**:
  - ⚡ **AWS Strands SDK**: Agent, Tool decorators, lifecycle hooks (`BeforeToolCallEvent`, `AfterToolCallEvent`).
  - 🧠 **Amazon Bedrock**: Anthropic Claude Sonnet for deep contextual understanding.
  - 💻 **Frontend**: React 19, Server-Sent Events (SSE) word streaming, custom dark aesthetics.
  - 🐍 **Backend**: Python Flask, streaming endpoints (`/chat-stream`, `/run-supervisor`).

> 🎙️ **Speaker Script (15s)**:
> *"Our tech stack leverages the AWS Strands SDK combined with Amazon Bedrock Claude AI on the backend, paired with a high-performance React 19 frontend streaming real-time event chunks."*

---

### 📍 Slide 8: Q&A & Judge FAQ Prep
**Visual Layout**: Thank you text, GitHub link, contact email (`support@dnextwave.com`).

- **Thank You!**
- **Live Demo**: `http://localhost:3000`
- **Backend API**: `http://localhost:5000`

---

## 🎯 Anticipated Judge Q&A & Key Winning Answers

### Q1: "Why build a multi-agent system when ChatGPT or Claude can answer CRM questions in a single prompt?"
> **Answer**:
> *"Single-prompt LLMs provide conversational answers, but they suffer from hallucinations and lack structural guarantees required for enterprise databases. In CRM onboarding, a single error — like a missing picklist API name or invalid stage progression — breaks Salesforce imports. Our Supervisor delegates to specialized Data, Automation, and Validation agents. The Validation Agent independently audits the configuration for conflicts and outputs a verified JSON schema that can be deterministically pushed to Salesforce APIs."*

### Q2: "How does AWS Strands SDK power your application?"
> **Answer**:
> *"We use AWS Strands SDK for agent creation, tool decoration (`@tool`), and lifecycle hooks (`HookProvider`). With lifecycle hooks like `BeforeToolCallEvent` and `AfterToolCallEvent`, we capture agent execution events in real time and stream them directly to our UI's Live Terminal Ticker, giving users complete visibility into agent operations."*

### Q3: "How do you handle non-standard or unexpected business inputs?"
> **Answer**:
> *"Our state machine evaluates inputs using keyword fuzzy matching and intent detection. If a user provides an off-topic or generic input (like 'ok' or 'zoom meeting'), our agent gently redirects them back to the active question while preserving their onboarding step progress."*
