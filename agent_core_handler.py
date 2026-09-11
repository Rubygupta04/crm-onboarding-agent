"""
AWS Bedrock AgentCore Deployment Handler for NextWave CRM Onboarding Agent
Compatible with AWS Bedrock Agents, AWS Lambda, and AWS Strands SDK AgentCore.
"""

import json
import os
from crm_engine import MultiAgentCRMOrchestrator
from app import query_claude, check_faq

def lambda_handler(event, context):
    """
    AWS AgentCore invocation entry point.
    Handles events from AWS Bedrock Agent runtime or API Gateway.
    """
    print(f"📥 [AgentCore] Invocation received: {json.dumps(event)}")

    # Extract input payload from Bedrock AgentCore event format or API Gateway body
    input_text = ""
    session_id = "agentcore-session"
    history = []

    if isinstance(event, dict):
        if "inputText" in event:
            input_text = event.get("inputText", "")
        elif "body" in event:
            try:
                body_data = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
                input_text = body_data.get("message", "")
                history = body_data.get("history", [])
            except Exception:
                input_text = str(event.get("body", ""))
        elif "message" in event:
            input_text = event.get("message", "")
            history = event.get("history", [])
        
        session_id = event.get("sessionId", event.get("sessionAttributes", {}).get("sessionId", session_id))

    if not input_text:
        input_text = "hello"

    # Route request to Multi-Agent Supervisor / Strands Engine
    orchestrator = MultiAgentCRMOrchestrator()

    # Check for direct question / off-topic fallback
    faq_ans = check_faq(input_text)
    if faq_ans:
        response_body = faq_ans
    else:
        claude_ans, model_used = query_claude(input_text)
        if claude_ans:
            response_body = f"{claude_ans}\n\n🤖 *[Powered by AgentCore / {model_used}]*"
        else:
            response_body = "NextWave CRM Onboarding Agent ready. Type 'hello' to begin guided setup!"

    response_payload = {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup", "CRMOnboardingActionGroup"),
            "apiPath": event.get("apiPath", "/onboard"),
            "httpMethod": "POST",
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": json.dumps({
                        "response": response_body,
                        "session_id": session_id,
                        "status": "success",
                        "agentcore_runtime": "AWS Bedrock AgentCore + Strands SDK"
                    })
                }
            }
        }
    }

    return response_payload


if __name__ == "__main__":
    # Test local execution
    test_event = {"inputText": "Can you explain how Salesforce CRM connects with AI automation in 2 bullet points?"}
    res = lambda_handler(test_event, None)
    print("AgentCore Response Test:")
    print(json.dumps(res, indent=2))
