from __future__ import annotations

import argparse
import sys
from pathlib import Path

from botocore.exceptions import ClientError

from aws_config import client, load_settings


def analyze_direct(model_id: str, region: str, bundle_path: Path) -> str:
    bundle = bundle_path.read_text(encoding="utf-8")
    prompt = f"""
You are an experienced SRE assistant.

Analyze this incident bundle and return:
1. Incident summary
2. Probable root cause
3. Evidence from logs
4. Recommended remediation steps
5. ServiceNow incident summary

{bundle}
"""

    bedrock_runtime = client("bedrock-runtime", region)
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 1200, "temperature": 0.2},
    )
    return response["output"]["message"]["content"][0]["text"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id")
    parser.add_argument("--region")
    parser.add_argument("--bundle", default="outputs/incident_bundle_payment_api.txt")
    parser.add_argument("--output", default="outputs/rca_direct.md")
    args = parser.parse_args()

    settings = load_settings()
    model_id = args.model_id or settings.model_id
    region = args.region or settings.region

    try:
        answer = analyze_direct(model_id, region, Path(args.bundle))
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(answer, encoding="utf-8")
        print(answer)
        print(f"\nSaved RCA output: {output_path}")
        return 0
    except (ClientError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
