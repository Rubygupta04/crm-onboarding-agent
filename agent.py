from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from tools import (
    generate_crm_plan, send_welcome_email, calculate_crm_cost,
    check_subscription_status, cancel_subscription, search_salesforce_pricing
)
from strands.hooks import (
    HookProvider, HookRegistry,
    BeforeToolCallEvent, AfterToolCallEvent, BeforeModelCallEvent
)

try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp
    AGENTCORE_AVAILABLE = True
except ImportError:
    AGENTCORE_AVAILABLE = False

from app import get_crm_response

# ─── Agent Lifecycle Hooks ───
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

# Model configuration for AWS Bedrock
model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-1",
    max_tokens=4096,
)

hooks = CRMAgentHooks()

# Create your CRM Onboarding Agent equipped with Strands Tools & Conversation Memory
agent = Agent(
    model=model,
    conversation_manager=SlidingWindowConversationManager(window_size=10),
    tools=[
        generate_crm_plan, send_welcome_email, calculate_crm_cost,
        check_subscription_status, cancel_subscription, search_salesforce_pricing
    ],
    hooks=[hooks],
    system_prompt="""You are a helpful CRM Onboarding Specialist for NextWave Tech Studio. 
    Your job is to help small businesses and nonprofits set up Salesforce CRM.
    
    You have tools to generate CRM plans, send welcome emails, calculate CRM costs, check subscription status, search live pricing, and manage cancellations.
    Use these tools when appropriate to assist the user!
    
    Ask the user these questions one by one:
    1. What is your business name and industry?
    2. How many team members will use the CRM?
    3. What are your main lead sources? (networking, website, referrals, events)
    4. What does your typical sales process look like?
    5. What follow-up reminders do you need?
    
    After gathering all answers provide:
    - A custom Salesforce pipeline recommendation
    - Lead stages specific to their business
    - Automation suggestions
    - A simple setup checklist
    
    Be friendly, professional, and specific to their business needs."""
)


def supervisor(message, history=None):
    """Supervisor Agent router delegating execution to NextWave Multi-Agent Engine."""
    res = get_crm_response(message, history or [])
    if isinstance(res, dict):
        return res.get("response", str(res))
    return str(res)


# ─── AWS Bedrock AgentCore Deployment Runtime ───
if AGENTCORE_AVAILABLE:
    app = BedrockAgentCoreApp()

    @app.entrypoint
    def run(payload):
        message = payload.get("message", "")
        history = payload.get("history", [])
        response = supervisor(message, history)
        return {"response": str(response)}

if __name__ == "__main__":
    if AGENTCORE_AVAILABLE and hasattr(app, "run"):
        print("🚀 Starting AWS Bedrock AgentCore Application Runtime...")
        app.run()
    else:
        print("=" * 50)
        print("Welcome to NextWave CRM Onboarding Agent!")
        print("=" * 50)
        print("I will help you set up Salesforce CRM.")
        print("Type 'quit' to exit\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Thank you for using NextWave CRM Agent!")
                break
            response = agent(user_input)
            print(f"\nAgent: {response}\n")