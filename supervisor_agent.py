from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from tools import (
    generate_crm_plan, send_welcome_email, calculate_crm_cost,
    check_subscription_status, cancel_subscription, search_salesforce_pricing
)

# ─── Model Configuration ───
model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-1",
    max_tokens=4096,
)

# ─── Specialized Sub-Agents ───
onboarding_agent = Agent(
    model=model,
    conversation_manager=SlidingWindowConversationManager(window_size=10),
    tools=[generate_crm_plan, send_welcome_email],
    system_prompt="""You specialize in Salesforce CRM Onboarding and Pipeline Setup.
    Help clients define lead stages, custom fields, and automated workflows."""
)

billing_agent = Agent(
    model=model,
    conversation_manager=SlidingWindowConversationManager(window_size=10),
    tools=[calculate_crm_cost, check_subscription_status, cancel_subscription, search_salesforce_pricing],
    system_prompt="""You specialize in Salesforce Billing, Subscription Management, Pricing, and Cancellations.
    Help clients check pricing, calculate team costs, upgrade plans, or process cancellations."""
)

support_agent = Agent(
    model=model,
    conversation_manager=SlidingWindowConversationManager(window_size=10),
    system_prompt="""You specialize in Technical Salesforce Support and Integration troubleshooting.
    Provide friendly, expert advice on Salesforce CRM setup."""
)


# ─── Multi-Agent Supervisor Router ───
class MultiAgentSupervisor:
    def __init__(self):
        self.onboarding = onboarding_agent
        self.billing = billing_agent
        self.support = support_agent

    def route_and_execute(self, user_input: str) -> str:
        text_lower = user_input.lower()
        
        if any(w in text_lower for w in ["price", "cost", "billing", "subscription", "cancel", "refund", "tier"]):
            print("🔀 [Supervisor] Routing request to: Billing & Subscriptions Specialist Agent")
            return str(self.billing(user_input))
            
        elif any(w in text_lower for w in ["error", "bug", "issue", "connect", "integrate", "tech", "help"]):
            print("🔀 [Supervisor] Routing request to: Technical Support Specialist Agent")
            return str(self.support(user_input))
            
        else:
            print("🔀 [Supervisor] Routing request to: CRM Onboarding Specialist Agent")
            return str(self.onboarding(user_input))


if __name__ == "__main__":
    supervisor = MultiAgentSupervisor()
    print("=" * 60)
    print("🤖 NextWave Multi-Agent Supervisor System Active")
    print("=" * 60)
    print("Specialists: Onboarding Agent | Billing Agent | Technical Support Agent")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Shutting down Multi-Agent Supervisor. Goodbye!")
            break
        response = supervisor.route_and_execute(user_input)
        print(f"\nAgent: {response}\n")
