"""
eval_scenarios.py - Evaluation Benchmark Suite for CRM Agent Suite
Tests 5-10 business scenarios, measuring validation pass rate & readiness scores.
"""

import json
import time
from crm_engine import MultiAgentCRMOrchestrator

TEST_SCENARIOS = [
    {
        "name": "Quantum Leap Wealth",
        "industry": "Financial Services",
        "team_size": "8 users",
        "lead_source": "Networking events & wealth referrals",
        "client_journey": "Discovery call -> Portfolio review -> Proposal -> Signed agreement",
        "follow_up": "Follow up call every 3 days"
    },
    {
        "name": "GreenCare Health Clinic",
        "industry": "Healthcare",
        "team_size": "15 users",
        "lead_source": "Patient online portal & doctor referrals",
        "client_journey": "Patient inquiry -> Insurance check -> Consultation -> Treatment plan",
        "follow_up": "Send email reminder after 2 days"
    },
    {
        "name": "RealtyPros Direct",
        "industry": "Real Estate",
        "team_size": "4 users",
        "lead_source": "Zillow inquiries & open house signups",
        "client_journey": "Inquiry -> Showing -> Offer -> Escrow -> Closed deal",
        "follow_up": "SMS check in every 5 days"
    },
    {
        "name": "Hope Environmental Nonprofit",
        "industry": "Nonprofit",
        "team_size": "5 users",
        "lead_source": "Annual gala & website grant forms",
        "client_journey": "Donor outreach -> Meeting -> Pledge -> Grant award",
        "follow_up": "Email follow up weekly"
    },
    {
        "name": "Apex SaaS Tech Studio",
        "industry": "Technology",
        "team_size": "12 users",
        "lead_source": "Product trials & LinkedIn ads",
        "client_journey": "Sign up -> Product demo -> POC trial -> Executive proposal -> Signed contract",
        "follow_up": "Automated email sequence"
    }
]

def run_evaluation_suite():
    orchestrator = MultiAgentCRMOrchestrator()
    results = []
    total_score = 0
    start_time = time.time()

    print("=" * 70)
    print("[EVAL] Running Agent Evaluation Suite (5 Business Scenarios)...")
    print("=" * 70)

    for idx, scenario in enumerate(TEST_SCENARIOS, 1):
        t0 = time.time()
        output = orchestrator.generate_and_validate(
            business_info=scenario["name"],
            industry=scenario["industry"],
            team_size=scenario["team_size"],
            lead_source=scenario["lead_source"],
            client_journey=scenario["client_journey"],
            follow_up=scenario["follow_up"]
        )
        elapsed = round(time.time() - t0, 3)
        score = output["readiness_score"]
        total_score += score

        res_entry = {
            "id": idx,
            "scenario_name": scenario["name"],
            "industry": scenario["industry"],
            "readiness_score": score,
            "validation_status": output["validation_report"]["status"],
            "pipeline_stages_count": len(output["pipeline"]),
            "user_roles_count": len(output["user_roles"]),
            "automations_count": len(output["automations"]),
            "latency_seconds": elapsed,
            "passed": score >= 85
        }
        results.append(res_entry)

        status_flag = "[PASS]" if res_entry["passed"] else "[FAIL]"
        print(f"{status_flag} Scenario {idx}: {scenario['name']} | Score: {score}/100 | Latency: {elapsed}s")

    total_elapsed = round(time.time() - start_time, 3)
    avg_score = round(total_score / len(TEST_SCENARIOS), 1)
    pass_rate = round((sum(1 for r in results if r["passed"]) / len(TEST_SCENARIOS)) * 100, 1)

    summary = {
        "total_scenarios": len(TEST_SCENARIOS),
        "pass_rate_percent": pass_rate,
        "average_readiness_score": avg_score,
        "total_benchmark_time_seconds": total_elapsed,
        "results": results
    }

    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 70)
    print(f"[SUMMARY] Evaluation Suite Summary: Pass Rate: {pass_rate}% | Avg Score: {avg_score}/100 | Time: {total_elapsed}s")
    print("[SAVED] Saved detailed evaluation benchmark matrix to eval_results.json")
    print("=" * 70)
    return summary


if __name__ == "__main__":
    run_evaluation_suite()
