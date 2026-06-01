import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_FILE = Path("data/sample_payment_logs.jsonl")

def main():
    random.seed(42)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2026, 5, 31, 10, 0, 0, tzinfo=timezone.utc)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for i in range(100):
            ts = start + timedelta(minutes=i)
            anomaly = 62 <= i <= 78

            row = {
                "timestamp": ts.isoformat().replace("+00:00", "Z"),
                "service": "payment-api",
                "endpoint": "/payment/submit",
                "latency_ms": random.randint(950, 1850) if anomaly else random.randint(180, 310),
                "status_code": 500 if anomaly and random.random() < 0.65 else 200,
                "error_message": random.choice(["DB connection timeout", "Payment gateway response delay", "Connection pool exhausted"]) if anomaly else "",
                "cpu_usage": random.randint(78, 94) if anomaly else random.randint(28, 57),
                "memory_usage": random.randint(72, 89) if anomaly else random.randint(38, 62),
                "request_count": random.randint(1200, 2200) if anomaly else random.randint(700, 1500),
                "host": f"ip-10-0-2-{random.randint(10,50)}",
                "environment": "poc"
            }
            f.write(json.dumps(row) + "\n")

    print(f"Generated logs: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
