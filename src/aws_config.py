from __future__ import annotations

import os
from dataclasses import dataclass

import boto3
from botocore.config import Config
from dotenv import load_dotenv


DEFAULT_REGION = "us-east-1"
DEFAULT_PREFIX = "sre-ai-poc"
DEFAULT_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


@dataclass(frozen=True)
class AwsSettings:
    region: str
    bucket: str | None
    prefix: str
    kb_id: str | None
    data_source_id: str | None
    model_arn: str | None
    model_id: str


def load_settings() -> AwsSettings:
    load_dotenv()
    return AwsSettings(
        region=os.getenv("AWS_REGION", DEFAULT_REGION),
        bucket=os.getenv("S3_BUCKET"),
        prefix=os.getenv("S3_PREFIX", DEFAULT_PREFIX).strip("/"),
        kb_id=os.getenv("BEDROCK_KB_ID"),
        data_source_id=os.getenv("BEDROCK_DATA_SOURCE_ID"),
        model_arn=os.getenv("BEDROCK_MODEL_ARN"),
        model_id=os.getenv("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID),
    )


def client(service_name: str, region_name: str):
    return boto3.client(
        service_name,
        region_name=region_name,
        config=Config(retries={"max_attempts": 5, "mode": "adaptive"}),
    )


def require(value: str | None, name: str) -> str:
    if not value:
        raise ValueError(f"Set {name} in .env or pass it as a CLI argument.")
    return value
