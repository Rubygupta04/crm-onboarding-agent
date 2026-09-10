from strands import Agent
from strands.models import BedrockModel

# Correct model ID for us-west-1
model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-1",
    max_tokens=4096,
)

# Create your CRM Onboarding Agent
agent = Agent(
    model=model,
    system_prompt="""You are a helpful CRM Onboarding Specialist for NextWave Tech Studio. 
    Your job is to help small businesses and nonprofits set up Salesforce CRM.
    
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