import json
import time
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS

# Try to import Strands AI for intelligent fallback
try:
    from strands import Agent
    from strands.models import BedrockModel
    from strands.agent.conversation_manager import SlidingWindowConversationManager
    from strands.hooks import (
        HookProvider, HookRegistry,
        BeforeToolCallEvent, AfterToolCallEvent, BeforeModelCallEvent
    )
    from tools import (
        generate_crm_plan, send_welcome_email, calculate_crm_cost,
        check_subscription_status, cancel_subscription, search_salesforce_pricing
    )

    class CRMAgentHooks(HookProvider):
        """Agent Lifecycle Hooks to monitor tool calls and execution events."""
        def register_hooks(self, registry: HookRegistry) -> None:
            registry.add_callback(BeforeToolCallEvent, self.on_tool_start)
            registry.add_callback(AfterToolCallEvent, self.on_tool_end)
            registry.add_callback(BeforeModelCallEvent, self.on_llm_start)

        def on_tool_start(self, event: BeforeToolCallEvent):
            tool_name = getattr(event, 'tool_name', 'unknown')
            print(f"🔧 [Agent Hook] Tool Started: {tool_name}")

        def on_tool_end(self, event: AfterToolCallEvent):
            tool_name = getattr(event, 'tool_name', 'unknown')
            print(f"✅ [Agent Hook] Tool Completed: {tool_name}")

        def on_llm_start(self, event: BeforeModelCallEvent):
            print("🤖 [Agent Hook] Claude AI thinking...")

    model = BedrockModel(
        model_id="global.anthropic.claude-sonnet-4-6",
        region_name="us-west-1",
        max_tokens=512,
    )
    ai_agent = Agent(
        model=model,
        conversation_manager=SlidingWindowConversationManager(window_size=10),
        tools=[
            generate_crm_plan, send_welcome_email, calculate_crm_cost,
            check_subscription_status, cancel_subscription, search_salesforce_pricing
        ],
        hooks=[CRMAgentHooks()],
        system_prompt="""You are a helpful CRM Onboarding Specialist for NextWave Tech Studio.
        You help small businesses set up Salesforce CRM.
        You have tools to calculate CRM costs, send welcome emails, generate CRM plans, check subscription status, search live pricing, and manage cancellations.
        Keep answers short, friendly, and focused on CRM/Salesforce topics.
        If asked something unrelated to CRM or business, politely redirect to the onboarding topic.
        Always end with encouragement to continue the onboarding process."""
    )
    AI_AVAILABLE = True
    print("[OK] Claude AI + Strands Tools + Agent Lifecycle Hooks active.")
except Exception as e:
    AI_AVAILABLE = False
    print(f"[WARN] Claude AI not available, using FAQ fallback only. ({e})")

app = Flask(__name__)
CORS(app)


# ─── FAQ Keyword Handler ────────────────────────────────────────────────────

FAQ = [
    {
        "keywords": ["what is salesforce", "what's salesforce", "salesforce mean"],
        "answer": """**What is Salesforce?** 🤔

Salesforce is the world's #1 CRM (Customer Relationship Management) platform.
It helps businesses track leads, manage customer relationships, automate follow-ups, and close more deals — all in one place.

It's used by over 150,000 companies worldwide, from small nonprofits to Fortune 500 companies.

Ready to continue setting up YOUR Salesforce? 🚀"""
    },
    {
        "keywords": ["what is crm", "what's a crm", "what does crm mean"],
        "answer": """**What is a CRM?** 📋

CRM stands for **Customer Relationship Management**.
It's a system that helps you:
- Track all your leads and clients in one place
- Never forget to follow up
- See your entire sales pipeline at a glance
- Automate repetitive tasks like emails and reminders

Think of it as a supercharged contact book for your business! 💼

Let's get yours set up — continue with the onboarding questions! 🚀"""
    },
    {
        "keywords": ["how much", "cost", "price", "pricing", "expensive", "free"],
        "answer": """**Salesforce Pricing** 💰

Here are the main plans:
- **Essentials** — $25/user/month (up to 5 users, perfect for small teams)
- **Professional** — $75/user/month (full sales features)
- **Enterprise** — $150/user/month (advanced customization)
- **Unlimited** — $300/user/month (everything + 24/7 support)

✅ All plans come with a **30-day free trial**!

Your onboarding plan will recommend the best tier for your team. Let's keep going! 🚀"""
    },
    {
        "keywords": ["upgrade", "upgrading", "change plan", "switch plan", "higher tier", "upgrade plan"],
        "answer": """**Upgrading Your Salesforce Plan** 🚀

Yes! You can upgrade your Salesforce CRM plan anytime:
- **Starter/Essentials → Professional** ($80/user/month): Unlocks advanced pipeline forecasting & lead scoring.
- **Professional → Enterprise** ($165/user/month): Unlocks custom workflow automation rules & API integrations.

To upgrade immediately, go to **Salesforce Setup ➔ Billing & Subscriptions** or contact **support@dnextwave.com**!"""
    },
    {
        "keywords": ["subscription", "billing", "my plan", "status", "subscription status", "plan status", "plan"],
        "answer": """**Salesforce Subscription & Billing** 💳

- **Current Trial Status**: 30-Day Free Trial Active
- **Starter/Essentials Tier**: $25/user/month
- **Refund Policy**: Full refund eligible within 30 days of billing charge
- **Cancellation**: Can be requested anytime from Account Settings or via support@dnextwave.com"""
    },
    {
        "keywords": ["cancel", "cancellation", "refund", "stop subscription"],
        "answer": """**Subscription Cancellation & Refund Policy** 🚫

If you need to cancel your Salesforce subscription:
1. **Cancellation**: Processed immediately; access continues until the end of your billing cycle.
2. **Data Export**: Your data remains available for download for 30 days post-cancellation.
3. **Refunds**: Eligible for a full refund within 30 days of your last billing charge.

Contact **support@dnextwave.com** or **support@salesforce.com** to process!"""
    },
    {
        "keywords": ["how long", "how much time", "setup time", "how many days"],
        "answer": """**How long does Salesforce setup take?** ⏱️

- **Basic setup** (pipeline + fields): 1–2 days
- **With automation rules**: 3–5 days
- **Full onboarding with training**: 1–2 weeks

With NextWave's CRM plan we're building for you, your team can be up and running in **under a week**! 🚀

Let's finish your onboarding questions so we can give you an exact plan!"""
    },
    {
        "keywords": ["help", "what can you do", "what do you do"],
        "answer": """**I'm your NextWave CRM Onboarding Agent!** 🤖

Here's what I can help you with:
- 🎯 Build a custom Salesforce pipeline for your business
- 📋 Recommend the right Salesforce plan for your team size
- ⚡ Suggest automations to save you time
- 📊 Identify the best custom fields for your industry
- 💳 Manage subscription status, billing, and cancellations

Just answer my 5 questions and I'll generate your full personalized CRM setup plan!

Type **'hello'** to start (or continue) the onboarding! 🚀"""
    },
    {
        "keywords": ["restart", "start over", "reset", "begin again", "hello", "hi", "hey", "start"],
        "answer": None  # Let the normal flow handle it (step logic)
    }
]


def check_faq(message):
    """Returns FAQ answer if message matches known keywords, else None."""
    msg_lower = message.lower().strip()
    for faq in FAQ:
        if faq["answer"] is None:
            continue
        if any(kw in msg_lower for kw in faq["keywords"]):
            return faq["answer"]
    return None


def ai_fallback(message):
    """Use Claude AI to answer if available, else return a generic response."""
    if AI_AVAILABLE:
        try:
            response = ai_agent(message)
            return str(response)
        except Exception as e:
            print(f"AI error: {e}")

    return """I'm not sure about that, but I'm here to help you set up your Salesforce CRM! 😊

If you have questions about **Salesforce**, **CRM setup**, or **pricing**, just ask!

Otherwise, type **'hello'** to continue your personalized CRM onboarding. 🚀"""


# ─── Industry / Team / Plan Helpers ────────────────────────────────────────

def detect_industry(text):
    text = text.lower()
    if any(w in text for w in ["financial", "finance", "bank", "insurance", "investment", "accounting"]):
        return "Financial Services"
    elif any(w in text for w in ["health", "medical", "clinic", "hospital", "dental", "pharma"]):
        return "Healthcare"
    elif any(w in text for w in ["nonprofit", "non-profit", "charity", "ngo", "foundation"]):
        return "Nonprofit"
    elif any(w in text for w in ["retail", "shop", "store", "ecommerce", "e-commerce"]):
        return "Retail"
    elif any(w in text for w in ["tech", "software", "saas", "it ", "technology"]):
        return "Technology"
    elif any(w in text for w in ["real estate", "realty", "property", "realtor"]):
        return "Real Estate"
    elif any(w in text for w in ["consult", "consulting", "advisory"]):
        return "Consulting"
    elif any(w in text for w in ["education", "school", "university", "training", "coaching"]):
        return "Education"
    else:
        return "General Business"


def get_pipeline_stages(industry):
    stages = {
        "Financial Services": [
            "New Prospect", "Initial Consultation", "Financial Review",
            "Proposal Sent", "Compliance Check", "Agreement Signed ✅", "Closed Lost ❌"
        ],
        "Healthcare": [
            "New Patient Inquiry", "Appointment Booked", "Consultation Done",
            "Treatment Plan Sent", "Follow-Up Scheduled", "Patient Onboarded ✅", "Closed Lost ❌"
        ],
        "Nonprofit": [
            "New Donor/Volunteer", "First Contact", "Needs Assessment",
            "Proposal/Ask", "Follow-Up", "Committed ✅", "Not Interested ❌"
        ],
        "Real Estate": [
            "New Lead", "Property Showing", "Offer Made",
            "Negotiation", "Under Contract", "Closed Won ✅", "Closed Lost ❌"
        ],
        "Technology": [
            "New Lead", "Demo Scheduled", "Demo Completed",
            "Proposal Sent", "Trial/POC", "Contract Signed ✅", "Closed Lost ❌"
        ],
    }
    default = [
        "New Lead", "First Contact Made", "Needs Assessment",
        "Proposal Sent", "Follow-Up", "Closed Won ✅", "Closed Lost ❌"
    ]
    return stages.get(industry, default)


def get_salesforce_tier(team_size_text):
    text = team_size_text.lower()
    if any(w in text for w in ["just me", "only me", "1", "solo", "myself"]):
        return "Salesforce Essentials (1 user) — $25/month"
    elif any(w in text for w in ["2", "3", "4", "5", "2-5", "small"]):
        return "Salesforce Essentials (up to 5 users) — $25/user/month"
    elif any(w in text for w in ["6", "7", "8", "9", "10", "6-10"]):
        return "Salesforce Professional — $75/user/month"
    else:
        return "Salesforce Enterprise — $150/user/month"


def get_lead_source_fields(lead_source_text):
    text = lead_source_text.lower()
    fields = ["Lead Source (dropdown)"]
    if "referral" in text:
        fields.append("Referred By (contact lookup)")
    if "website" in text or "online" in text:
        fields.append("Website Form Source")
    if "social" in text or "linkedin" in text or "instagram" in text:
        fields.append("Social Media Channel")
    if "event" in text or "network" in text:
        fields.append("Event Name / Location")
    fields += ["First Contact Date", "Follow-Up Date", "Proposal Sent Date"]
    return fields


# ─── Question Helper Prompts & State Machine ───────────────────────────────

QUESTION_PROMPTS = {
    1: """**Question 1 of 5:** What is your business name and what industry are you in?
(Example: Acme Consulting, financial services, healthcare, retail)""",
    2: """**Question 2 of 5:** How many team members will be using the CRM?
(Example: just me, 2-5 people, 6-10 people, more than 10)""",
    3: """**Question 3 of 5:** Where do your leads or clients come from?
(Example: networking events, website, referrals, social media)""",
    4: """**Question 4 of 5:** What does your typical client journey look like?
(Example: first call then proposal then follow up then close)""",
    5: """**Question 5 of 5:** What kind of follow-up reminders do you need?
(Example: call after 3 days, send email weekly, check in monthly)"""
}

QUESTION_REMINDERS = {
    1: "\n\n📍 *Now, let's start with Question 1 of 5: What is your business name and industry?*",
    2: "\n\n📍 *Now, back to Question 2 of 5: How many team members will use the CRM?*",
    3: "\n\n📍 *Now, back to Question 3 of 5: Where do your leads or clients come from?*",
    4: "\n\n📍 *Now, back to Question 4 of 5: What does your typical client journey look like?*",
    5: "\n\n📍 *Now, back to Question 5 of 5: What kind of follow-up reminders do you need?*"
}

GENERIC_WORDS = {
    "yes", "no", "ok", "okay", "sure", "yep", "yeah", "yup", "fine", "cool",
    "thanks", "thank you", "k", "kk", "good", "great", "hi", "hello", "hey",
    "start", "begin", "please", "test", "nah", "nope", "whatever", "idk"
}

INVALID_ANSWER_PROMPTS = {
    1: """Please share your actual business name and industry (e.g. 'Acme Consulting, Financial Services' or 'Summit Realty, Real Estate') so I can tailor your Salesforce setup!

""" + QUESTION_PROMPTS[1],
    2: """Please specify how many team members will use the CRM (e.g. 'just me', '3 people', '5 users') so I can recommend the best Salesforce plan!

""" + QUESTION_PROMPTS[2],
    3: """Please specify where your leads or clients come from (e.g. 'website, referrals, social media, events')!

""" + QUESTION_PROMPTS[3],
    4: """Please describe your typical sales journey steps (e.g. 'first call -> proposal -> follow up -> close')!

""" + QUESTION_PROMPTS[4],
    5: """Please specify what follow-up reminders you need (e.g. 'call after 3 days, send email weekly')!

""" + QUESTION_PROMPTS[5]
}


def is_question_or_offtopic(message):
    msg = message.strip().lower()
    
    # 1. Ends with question mark
    if msg.endswith("?"):
        return True
        
    # 2. Known FAQ keywords match
    if check_faq(message) is not None:
        return True

    # 3. Common off-topic triggers (Zoom, weather, code, general setup non-CRM)
    offtopic_words = [
        "zoom", "video meeting", "google meet", "teams meeting", "skype",
        "weather", "recipe", "password", "wifi", "printer", "camera",
        "python", "javascript", "react", "html", "code", "game"
    ]
    if any(w in msg for w in offtopic_words):
        return True

    # 4. Question phrase starters
    question_starters = (
        "how to", "how do", "how can", "what is", "what are", "what does",
        "where is", "where do", "why is", "why do", "can you", "can i",
        "tell me", "explain", "help me"
    )
    if any(msg.startswith(s) for s in question_starters):
        return True

    return False


def is_generic_or_invalid_answer(message, pending_q):
    msg = message.strip().lower()
    words = [w.strip(".,!?") for w in msg.split()]
    
    # 1. Single word or short generic phrase made up of words like "yes", "ok", "sure", "hello"
    if len(words) <= 2 and all(w in GENERIC_WORDS for w in words):
        return True
        
    # 2. Extremely short input (less than 2 characters)
    if len(msg) < 2:
        return True
        
    return False


def parse_onboarding_answers(history):
    """
    Parses history to retrieve answered questions and determine current pending question (1-5, or 6 if complete).
    """
    answers = {}
    pending_q = 0  # 0 means welcome / start state
    
    for i, item in enumerate(history):
        if item.get('role') == 'agent':
            text = item.get('text', '')
            if 'Personalized Salesforce CRM Setup Plan' in text:
                pending_q = 6
            elif 'Question 5 of 5:' in text:
                pending_q = 5
            elif 'Question 4 of 5:' in text:
                pending_q = 4
            elif 'Question 3 of 5:' in text:
                pending_q = 3
            elif 'Question 2 of 5:' in text:
                pending_q = 2
            elif 'Question 1 of 5:' in text or 'What is your business name' in text:
                pending_q = 1
                
        elif item.get('role') == 'user':
            text = item.get('text', '')
            # Check if this user message was accepted as an answer by looking at the subsequent agent message
            if 1 <= pending_q <= 5 and i + 1 < len(history):
                next_agent = history[i+1].get('text', '')
                if "Question " in next_agent or "Personalized Salesforce CRM Setup Plan" in next_agent:
                    if pending_q == 1 and ('Question 2 of 5:' in next_agent or 'Personalized' in next_agent):
                        answers[1] = text
                    elif pending_q == 2 and ('Question 3 of 5:' in next_agent or 'Personalized' in next_agent):
                        answers[2] = text
                    elif pending_q == 3 and ('Question 4 of 5:' in next_agent or 'Personalized' in next_agent):
                        answers[3] = text
                    elif pending_q == 4 and ('Question 5 of 5:' in next_agent or 'Personalized' in next_agent):
                        answers[4] = text
                    elif pending_q == 5 and 'Personalized' in next_agent:
                        answers[5] = text

    return pending_q, answers


# ─── Schema & Email Template Helpers ─────────────────────────────────────────

def generate_salesforce_schema(business_info, industry, custom_fields, pipeline_stages):
    return {
        "org_name": business_info,
        "industry": industry,
        "target_object": "Opportunity_and_Lead",
        "custom_fields": [
            {
                "api_name": f.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "").strip("_") + "__c",
                "label": f,
                "type": "Text" if "date" not in f.lower() else "Date"
            }
            for f in custom_fields
        ],
        "pipeline_stages": pipeline_stages,
        "generated_by": "NextWave CRM Onboarding Agent (AWS Strands SDK)"
    }


def generate_email_templates(business_info, industry, lead_source, follow_up):
    return [
        {
            "title": "📧 Initial Lead Outreach",
            "subject": f"Thank you for connecting with {business_info}",
            "body": f"Hi [Client Name],\n\nThank you for reaching out via {lead_source}! We'd love to learn more about how we can support your goals in {industry}.\n\nWhen would be a good time for a brief 10-minute intro call?\n\nBest regards,\n[Your Name]\n{business_info}"
        },
        {
            "title": "🔔 Follow-up Reminder",
            "subject": f"Following up on our conversation — {business_info}",
            "body": f"Hi [Client Name],\n\nJust following up on our previous note ({follow_up}). I wanted to make sure you had everything you need to take the next step.\n\nLet me know if you have any questions!\n\nBest,\n[Your Name]"
        },
        {
            "title": "🚀 Proposal & Next Steps",
            "subject": f"Your Custom Proposal from {business_info}",
            "body": f"Hi [Client Name],\n\nIt was great speaking with you! Attached is your custom proposal tailored to your needs.\n\nPlease review and let me know if you'd like to schedule a quick walk-through.\n\nWarm regards,\n[Your Name]"
        }
    ]


# ─── Main Response Logic ────────────────────────────────────────────────────

def get_crm_response(message, history):
    # Exclude current unhandled user message from history slice if present
    hist_to_parse = history[:-1] if (history and history[-1].get('role') == 'user') else history
    pending_q, answers = parse_onboarding_answers(hist_to_parse)
    
    msg_clean = message.strip()
    msg_lower = msg_clean.lower()
    
    print(f"Pending Question: {pending_q} | Answers so far: {answers} | Input: {message}")

    # 1. Check if user is asking an FAQ or off-topic question
    if is_question_or_offtopic(message):
        faq_ans = check_faq(message)
        if faq_ans:
            response_body = faq_ans
        else:
            response_body = ai_fallback(message)
            
        # If in active onboarding flow (Q1..Q5), attach reminder of current question
        if 1 <= pending_q <= 5:
            return {
                "response": response_body + QUESTION_REMINDERS.get(pending_q, ""),
                "step": pending_q
            }
        elif pending_q == 0:
            return {
                "response": response_body + "\n\nReady to get started? Type **'hello'** or enter your business name!",
                "step": 1
            }
        else:
            return {
                "response": response_body,
                "step": 6
            }

    # 2. Greeting / Start command (if at welcome state Q0, or if user explicitly sends hello/hi/start/restart)
    if pending_q == 0 or msg_lower in ["hello", "hi", "hey", "start", "begin", "restart"]:
        return {
            "response": """Great! Welcome to NextWave CRM Onboarding! 🎉

I will help you set up the perfect Salesforce CRM for your business.

""" + QUESTION_PROMPTS[1],
            "step": 1
        }

    # 3. Check if user provided a generic non-answer like "yes", "ok", "sure", etc.
    if 1 <= pending_q <= 5 and is_generic_or_invalid_answer(message, pending_q):
        return {
            "response": INVALID_ANSWER_PROMPTS[pending_q],
            "step": pending_q
        }

    # 4. User is answering pending_q (1 to 5) with a valid answer
    if pending_q == 1:
        answers[1] = msg_clean
        return {
            "response": """Perfect! Thank you for sharing that.

""" + QUESTION_PROMPTS[2],
            "step": 2
        }

    elif pending_q == 2:
        answers[2] = msg_clean
        return {
            "response": """Great! That helps me understand your setup.

""" + QUESTION_PROMPTS[3],
            "step": 3
        }

    elif pending_q == 3:
        answers[3] = msg_clean
        return {
            "response": """Excellent! Understanding your lead sources is key.

""" + QUESTION_PROMPTS[4],
            "step": 4
        }

    elif pending_q == 4:
        answers[4] = msg_clean
        return {
            "response": """Almost done! Just one more question.

""" + QUESTION_PROMPTS[5],
            "step": 5
        }

    elif pending_q == 5:
        answers[5] = msg_clean
        
        business_info  = answers.get(1, 'Your Business')
        team_size      = answers.get(2, 'your team')
        lead_source    = answers.get(3, 'various sources')
        client_journey = answers.get(4, 'your process')
        follow_up      = answers.get(5, 'regular reminders')

        industry = detect_industry(business_info)
        pipeline_stages = get_pipeline_stages(industry)
        sf_tier = get_salesforce_tier(team_size)
        custom_fields = get_lead_source_fields(lead_source)

        stages_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(pipeline_stages)])
        fields_text = "\n".join([f"- {f}" for f in custom_fields])

        text_plan = f"""✅ Thank you! Here is your Personalized Salesforce CRM Setup Plan:

---

👤 **Business:** {business_info}
🏭 **Industry Detected:** {industry}
👥 **Team Size:** {team_size}
📣 **Lead Sources:** {lead_source}
🔄 **Client Journey:** {client_journey}
🔔 **Follow-Up Style:** {follow_up}

---

🎯 **Recommended Pipeline Stages for {industry}:**
{stages_text}

---

⚡ **Automation Recommendations:**
- Auto-capture leads from {lead_source} into Salesforce
- Set follow-up reminders based on: "{follow_up}"
- Auto-send proposal follow-up emails after 5 days of no response
- Weekly stale lead alerts for deals inactive over 7 days
- Auto-assign new leads to the right team member

---

📊 **Custom Fields to Add in Salesforce:**
{fields_text}

---

💡 **Recommended Salesforce Plan:**
{sf_tier}

---

Your personalized CRM is ready to launch! 🚀
NextWave Tech Studio • dnextwave.com

*Have questions about your plan? Just ask me anything!*"""

        schema = generate_salesforce_schema(business_info, industry, custom_fields, pipeline_stages)
        email_templates = generate_email_templates(business_info, industry, lead_source, follow_up)

        return {
            "response": text_plan,
            "step": 6,
            "pipeline": pipeline_stages,
            "salesforce_schema": schema,
            "email_templates": email_templates,
            "business_info": business_info,
            "industry": industry
        }

    else:
        # Post-plan: answered already, standard Q&A
        faq_ans = check_faq(message)
        if faq_ans:
            return {"response": faq_ans, "step": 6}
        return {"response": ai_fallback(message), "step": 6}


# ─── Flask Route ────────────────────────────────────────────────────────────

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    history = data.get("history", [])
    res_data = get_crm_response(message, history)
    return jsonify(res_data)


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    data = request.get_json() or {}
    message = data.get("message", "")
    history = data.get("history", [])

    def generate():
        res_data = get_crm_response(message, history)
        full_response = res_data.get("response", "") if isinstance(res_data, dict) else str(res_data)

        # 1. Send metadata header chunk first
        meta_chunk = {
            "step": res_data.get("step", 1) if isinstance(res_data, dict) else 1,
            "pipeline": res_data.get("pipeline") if isinstance(res_data, dict) else None,
            "salesforce_schema": res_data.get("salesforce_schema") if isinstance(res_data, dict) else None,
            "email_templates": res_data.get("email_templates") if isinstance(res_data, dict) else None,
            "business_info": res_data.get("business_info") if isinstance(res_data, dict) else None,
            "industry": res_data.get("industry") if isinstance(res_data, dict) else None,
        }
        yield f"data: {json.dumps({'meta': meta_chunk})}\n\n"

        # 2. Stream text words in real time with micro-delay
        words = full_response.split(" ")
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            yield f"data: {json.dumps({'text': chunk})}\n\n"
            time.sleep(0.015)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route('/run-agent-tasks', methods=['POST'])
def run_agent_tasks():
    data = request.json or {}
    business = data.get('business_name') or 'Client Business'
    
    # Autonomous Agent task execution simulation
    tasks_completed = [
        f"✅ Created Salesforce pipeline for {business}",
        f"✅ Generated 3 AI sales email templates",
        f"✅ Built custom field schema for {business}",
        f"✅ Set up follow-up automation rules",
        f"✅ Created onboarding checklist PDF",
        f"✅ Sent welcome email to {business} team",
    ]
    
    return jsonify({
        'tasks': tasks_completed,
        'status': 'Agent completed all tasks!'
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)