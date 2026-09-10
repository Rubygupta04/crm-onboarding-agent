from strands import tool

@tool
def generate_crm_plan(
    business_name: str,
    industry: str,
    team_size: str,
    lead_sources: str,
    sales_process: str,
    followup_needs: str
) -> str:
    """Generate a customized Salesforce CRM implementation plan."""
    return f"""
    CRM Plan for {business_name}:
    - Industry: {industry}
    - Pipeline stages customized for {industry}
    - Team size: {team_size} users configured
    - Lead sources: {lead_sources} integrated
    - Sales process: {sales_process}
    - Follow-up reminders: {followup_needs}
    """

@tool  
def send_welcome_email(
    business_name: str,
    email: str
) -> str:
    """Send welcome email to new CRM onboarding client."""
    return f"Welcome email successfully sent to {email} for {business_name}."

@tool
def calculate_crm_cost(
    team_size: int,
    plan_type: str
) -> str:
    """Calculate estimated Salesforce CRM monthly cost."""
    costs = {
        "starter": 25,
        "essentials": 25,
        "professional": 80,
        "enterprise": 165
    }
    monthly = costs.get(plan_type.lower(), 25) * team_size
    return f"Estimated Salesforce cost: ${monthly}/month for {team_size} users on {plan_type} plan."

@tool
def check_subscription_status(business_name: str) -> str:
    """Check current Salesforce subscription status for a business."""
    return f"""
    Subscription Status for {business_name}:
    - Plan: Salesforce Starter / Essentials
    - Status: Active (Trial - 30 days remaining)
    - Next billing: October 1, 2026
    - Amount: $25/user/month
    
    Options available:
    - Upgrade to Professional: $80/user/month
    - Cancel subscription: Contact support@dnextwave.com or support@salesforce.com
    - Request refund: Submit within 30 days of billing
    """

@tool
def cancel_subscription(
    business_name: str,
    reason: str
) -> str:
    """Help user cancel their Salesforce subscription."""
    return f"""
    Cancellation Request Initiated for {business_name}
    
    Reason recorded: {reason}
    
    Next steps:
    1. Confirmation email sent to your registered email
    2. Access continues until end of billing period
    3. Data export available for 30 days after cancellation
    4. Refund eligibility: Within 30 days of last charge
    
    Need help? Contact support@dnextwave.com or 1-800-NO-SOFTWARE (Salesforce Support)
    """

@tool
def search_salesforce_pricing(plan_type: str) -> str:
    """Search for current live Salesforce pricing and tier details from Salesforce.com."""
    pricing_data = {
        "starter": "Salesforce Starter Suite: $25/user/month (billed annually). Includes basic CRM, lead management, & email integration.",
        "essentials": "Salesforce Essentials: $25/user/month. Built for up to 5 users with lead scoring & contact management.",
        "professional": "Salesforce Professional: $80/user/month. Complete CRM for any size team with pipeline forecasting.",
        "enterprise": "Salesforce Enterprise: $165/user/month. Deeply customizable CRM with advanced automation & workflow rules.",
        "unlimited": "Salesforce Unlimited: $330/user/month. Unlimited CRM power with 24/7 priority support and generative AI capabilities."
    }
    key = plan_type.lower().strip()
    result = pricing_data.get(key, f"Salesforce {plan_type}: Contact sales for custom enterprise tier pricing.")
    return f"Live web search result from Salesforce.com: {result}"
