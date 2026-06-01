from __future__ import annotations

import argparse
import sys
from pathlib import Path

from botocore.exceptions import ClientError

from aws_config import client, load_settings, require

DEFAULT_QUESTION = """
Analyze payment-api high-latency issue and suggest RCA.
Return:
1. Incident summary
2. Probable root cause
3. Evidence from logs/runbook
4. Remediation steps
5. ServiceNow incident summary
"""


def query_kb(kb_id: str, model_arn: str, region: str, question: str, results: int) -> str:
    bedrock_agent_runtime = client("bedrock-agent-runtime", region)
    response = bedrock_agent_runtime.retrieve_and_generate(
        input={"text": question[:1000]},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": model_arn,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {"numberOfResults": results}
                },
            },
        },
    )
    return response["output"]["text"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb-id")
    parser.add_argument("--model-arn")
    parser.add_argument("--region")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--results", type=int, default=8)
    parser.add_argument("--output", default="outputs/rca_from_kb.md")
    args = parser.parse_args()

    settings = load_settings()
    kb_id = args.kb_id or require(settings.kb_id, "BEDROCK_KB_ID")
    model_arn = args.model_arn or require(settings.model_arn, "BEDROCK_MODEL_ARN")
    region = args.region or settings.region

    try:
        answer = query_kb(kb_id, model_arn, region, args.question, args.results)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(answer, encoding="utf-8")
        print(answer)
        print(f"\nSaved RCA output: {output_path}")
        return 0
    except (ClientError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
