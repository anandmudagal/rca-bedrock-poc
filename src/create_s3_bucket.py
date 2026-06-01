from __future__ import annotations

import argparse
import sys

from botocore.exceptions import ClientError

from aws_config import client, load_settings, require


def create_bucket(bucket: str, region: str) -> None:
    s3 = client("s3", region)
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"Created bucket: s3://{bucket}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket already exists and is owned by you: s3://{bucket}")

    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )
    s3.put_bucket_encryption(
        Bucket=bucket,
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256",
                    }
                }
            ]
        },
    )
    print("Applied public access block and SSE-S3 encryption.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket")
    parser.add_argument("--region")
    args = parser.parse_args()

    settings = load_settings()
    bucket = args.bucket or require(settings.bucket, "S3_BUCKET")
    region = args.region or settings.region

    try:
        create_bucket(bucket, region)
        return 0
    except (ClientError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
