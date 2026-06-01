from __future__ import annotations

import argparse
import sys
from pathlib import Path

from botocore.exceptions import ClientError

from aws_config import client, load_settings, require

FILES = [
    "data/sample_payment_logs.jsonl",
    "runbooks/payment_api_runbook.txt",
    "outputs/incident_bundle_payment_api.txt"
]


def upload_files(bucket: str, prefix: str, region: str) -> list[str]:
    s3 = client("s3", region)
    uploaded = []

    for file_name in FILES:
        path = Path(file_name)
        if not path.exists():
            raise FileNotFoundError(f"Missing {file_name}. Run generate/build scripts first.")
        key = f"{prefix.strip('/')}/{file_name}".replace("\\", "/")
        s3.upload_file(str(path), bucket, key)
        uploaded.append(f"s3://{bucket}/{key}")

    return uploaded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket")
    parser.add_argument("--prefix")
    parser.add_argument("--region")
    args = parser.parse_args()

    settings = load_settings()
    bucket = args.bucket or require(settings.bucket, "S3_BUCKET")
    prefix = args.prefix or settings.prefix
    region = args.region or settings.region

    try:
        for uri in upload_files(bucket, prefix, region):
            print(f"Uploaded: {uri}")
        return 0
    except (ClientError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
