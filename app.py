from flask import Flask, request, jsonify
from flask_cors import CORS

# Try to import Strands AI for intelligent fallback
try:
    from strands import Agent
    from strands.models import BedrockModel
    model = BedrockModel(
        model_id="global.anthropic.claude-sonnet-4-6",
        region_name="us-west-1",
        max_tokens=512,
    )
    ai_agent = Agent(
        model=model,
        system_prompt="""You are a helpful CRM Onboarding Specialist for NextWave Tech Studio.
        You help small businesses set up Salesforce CRM.
        Keep answers short, friendly, and focused on CRM/Salesforce topics.
        If asked something unrelated to CRM or business, politely redirect to the onboarding topic.
        Always end with encouragement to continue the onboarding process."""
    )
    AI_AVAILABLE = True
    print("[OK] Claude AI fallback is active.")
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


# ─── Main Response Logic ────────────────────────────────────────────────────

def get_crm_response(message, history):
    user_messages = [m for m in history if m.get('role') == 'user']
    step = len(user_messages)

    print(f"Step: {step} | Message: {message}")

    # ── Check FAQ first (except during active onboarding steps 2-5) ──
    if step < 2 or step >= 6:
        faq_answer = check_faq(message)
        if faq_answer:
            return faq_answer

    # ── Mid-flow: check if user is asking a question instead of answering ──
    if 2 <= step <= 5 and message.strip().endswith("?"):
        faq_answer = check_faq(message)
        if faq_answer:
            # Remind them where they are after answering
            question_reminders = {
                2: "\n\n📍 *Now, back to Question 1: What is your business name and industry?*",
                3: "\n\n📍 *Now, back to Question 2: How many team members will use the CRM?*",
                4: "\n\n📍 *Now, back to Question 3: Where do your leads come from?*",
                5: "\n\n📍 *Now, back to Question 4: What does your client journey look like?*",
            }
            return faq_answer + question_reminders.get(step, "")
        else:
            # Unknown question mid-flow → AI fallback + remind where they are
            ai_response = ai_fallback(message)
            question_reminders = {
                2: "\n\n📍 *Back to Question 1: What is your business name and industry?*",
                3: "\n\n📍 *Back to Question 2: How many team members will use the CRM?*",
                4: "\n\n📍 *Back to Question 3: Where do your leads come from?*",
                5: "\n\n📍 *Back to Question 4: What does your client journey look like?*",
            }
            return ai_response + question_reminders.get(step, "")

    # ── Normal onboarding flow ──
    if step == 1:
        return """Great! Welcome to NextWave CRM Onboarding! 🎉

I will help you set up the perfect Salesforce CRM for your business.

**Question 1 of 5:** What is your business name and what industry are you in?
(Example: financial services, nonprofit, healthcare, retail)"""

    elif step == 2:
        return """Perfect! Thank you for sharing that.

**Question 2 of 5:** How many team members will be using the CRM?
(Example: just me, 2-5 people, 6-10 people, more than 10)"""

    elif step == 3:
        return """Great! That helps me understand your setup.

**Question 3 of 5:** Where do your leads or clients come from?
(Example: networking events, website, referrals, social media)"""

    elif step == 4:
        return """Excellent! Understanding your lead sources is key.

**Question 4 of 5:** What does your typical client journey look like?
(Example: first call then proposal then follow up then close)"""

    elif step == 5:
        return """Almost done! Just one more question.

**Question 5 of 5:** What kind of follow-up reminders do you need?
(Example: call after 3 days, send email weekly, check in monthly)"""

    elif step == 6:
        business_info  = user_messages[1].get('text', 'Your Business')  if len(user_messages) > 1 else 'Your Business'
        team_size      = user_messages[2].get('text', 'your team')       if len(user_messages) > 2 else 'your team'
        lead_source    = user_messages[3].get('text', 'various sources') if len(user_messages) > 3 else 'various sources'
        client_journey = user_messages[4].get('text', 'your process')   if len(user_messages) > 4 else 'your process'
        follow_up      = user_messages[5].get('text', 'regular reminders') if len(user_messages) > 5 else 'regular reminders'

        industry = detect_industry(business_info)
        pipeline_stages = get_pipeline_stages(industry)
        sf_tier = get_salesforce_tier(team_size)
        custom_fields = get_lead_source_fields(lead_source)

        stages_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(pipeline_stages)])
        fields_text = "\n".join([f"- {f}" for f in custom_fields])

        return f"""✅ Thank you! Here is your Personalized Salesforce CRM Setup Plan:

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

    else:
        # Post-plan: check FAQ first, then AI fallback
        faq_answer = check_faq(message)
        if faq_answer:
            return faq_answer
        return ai_fallback(message)


# ─── Flask Route ────────────────────────────────────────────────────────────

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    history = data.get("history", [])
    response = get_crm_response(message, history)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=5000)