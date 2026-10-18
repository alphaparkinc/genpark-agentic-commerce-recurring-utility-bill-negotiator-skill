from client import AgenticUtilityBillNegotiator

def main():
    negotiator = AgenticUtilityBillNegotiator()
    res = negotiator.audit_and_negotiate_bill("Spectrum Internet", "Ultra 500M", 89.99, contract_end_months_ago=12)
    print("--- Recurring Utility Bill Audit ---")
    print(f"Provider: {res['provider']} | Current: ${res['current_monthly_charge_usd']}/mo")
    print(f"Target: ${res['target_benchmark_rate_usd']}/mo | Potential Savings: ${res['annual_savings_potential_usd']}/yr")
    print(f"Negotiation Script:\n{res['retention_negotiation_script']}")

if __name__ == "__main__":
    main()
