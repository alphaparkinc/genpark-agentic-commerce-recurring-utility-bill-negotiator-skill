#!/usr/bin/env python3
import json
import sys
from client import AgenticUtilityBillNegotiator

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        negotiator = AgenticUtilityBillNegotiator()
        res = negotiator.audit_and_negotiate_bill("Comcast Xfinity", "1000Mbps Gigabit", 115.0, contract_end_months_ago=8)
        assert res["annual_savings_potential_usd"] == 600.0 # (115 - 65) * 12
        assert "Google Fiber" in res["retention_negotiation_script"]
        print(f"[TEST PASS] Bill Negotiator Savings: ${res['annual_savings_potential_usd']}/yr")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-bill-negotiator", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "audit_and_negotiate_bill", "description": "Audit telecom bill and synthesize retention script"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                negotiator = AgenticUtilityBillNegotiator()
                out = negotiator.audit_and_negotiate_bill(
                    args.get("provider", "Telecom"),
                    args.get("service_tier", "Standard"),
                    float(args.get("current_monthly_charge", 80.0)),
                    int(args.get("contract_end_months_ago", 0))
                )
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
