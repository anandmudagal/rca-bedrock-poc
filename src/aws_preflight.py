from __future__ import annotations

import argparse
import sys

from botocore.exceptions import ClientError, NoCredentialsError

from aws_config import client, load_settings


def run_preflight(region: str) -> int:
    failures = 0

    try:
        sts = client("sts", region)
        identity = sts.get_caller_identity()
        print(f"AWS identity: {identity['Arn']}")
    except (ClientError, NoCredentialsError) as exc:
        print(f"AWS credentials: not ready ({exc})")
        failures += 1

    try:
        bedrock = client("bedrock", region)
        models = bedrock.list_foundation_models()["modelSummaries"]
        matching = [
            model["modelId"]
            for model in models
            if "embed" in model["modelId"].lower() or "claude" in model["modelId"].lower()
        ]
        print(f"Bedrock models visible in {region}: {len(models)}")
        for model_id in matching[:10]:
            print(f"  {model_id}")
    except (ClientError, NoCredentialsError) as exc:
        print(f"Bedrock model access check: not ready ({exc})")
        failures += 1

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region")
    args = parser.parse_args()

    settings = load_settings()
    failures = run_preflight(args.region or settings.region)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
