import json
from pathlib import Path
from statistics import mean

LOG_FILE = Path("data/sample_payment_logs.jsonl")
RUNBOOK_FILE = Path("runbooks/payment_api_runbook.txt")
OUTPUT_FILE = Path("outputs/incident_bundle_payment_api.txt")

def main():
    logs = [json.loads(line) for line in LOG_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    normal = [x for x in logs if x["latency_ms"] < 500 and x["status_code"] == 200]
    incident = [x for x in logs if x["latency_ms"] >= 800 or x["status_code"] >= 500 or x["error_message"]]

    avg_normal = round(mean([x["latency_ms"] for x in normal]), 2)
    avg_incident = round(mean([x["latency_ms"] for x in incident]), 2)
    max_latency = max(x["latency_ms"] for x in logs)
    error_count = sum(1 for x in logs if x["status_code"] >= 500)
    timeout_count = sum(1 for x in logs if "timeout" in x["error_message"].lower())

    sample_logs = "\n".join(json.dumps(x) for x in incident[:15])
    runbook = RUNBOOK_FILE.read_text(encoding="utf-8")

    bundle = f"""# Incident Bundle: payment-api high latency

## Summary Metrics
Service: payment-api
Endpoint: /payment/submit
Total log rows: {len(logs)}
Incident log rows: {len(incident)}
Average normal latency: {avg_normal} ms
Average incident latency: {avg_incident} ms
Max latency: {max_latency} ms
HTTP 500 error count: {error_count}
DB timeout count: {timeout_count}

## Sample Incident Logs
{sample_logs}

## Runbook Context
{runbook}

## RCA Question
Analyze payment-api high-latency issue and suggest RCA.
Return incident summary, probable root cause, evidence, and remediation steps.
"""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(bundle, encoding="utf-8")
    print(f"Created incident bundle: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
