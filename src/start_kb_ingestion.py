from __future__ import annotations

import argparse
import sys
import time

from botocore.exceptions import ClientError

from aws_config import client, load_settings, require


TERMINAL_STATUSES = {"COMPLETE", "FAILED", "STOPPED"}


def start_ingestion(kb_id: str, data_source_id: str, region: str, wait: bool) -> dict:
    bedrock_agent = client("bedrock-agent", region)
    response = bedrock_agent.start_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=data_source_id,
        description="Sync SRE AI POC data from S3",
    )

    job = response["ingestionJob"]
    job_id = job["ingestionJobId"]
    print(f"Started ingestion job: {job_id}")
    print(f"Status: {job['status']}")

    if not wait:
        return job

    while job["status"] not in TERMINAL_STATUSES:
        time.sleep(10)
        response = bedrock_agent.get_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=data_source_id,
            ingestionJobId=job_id,
        )
        job = response["ingestionJob"]
        stats = job.get("statistics", {})
        print(f"Status: {job['status']} {stats}")

    return job


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb-id")
    parser.add_argument("--data-source-id")
    parser.add_argument("--region")
    parser.add_argument("--no-wait", action="store_true")
    args = parser.parse_args()

    settings = load_settings()
    kb_id = args.kb_id or require(settings.kb_id, "BEDROCK_KB_ID")
    data_source_id = args.data_source_id or require(settings.data_source_id, "BEDROCK_DATA_SOURCE_ID")
    region = args.region or settings.region

    try:
        job = start_ingestion(kb_id, data_source_id, region, wait=not args.no_wait)
        status = job["status"]
        print(f"Ingestion finished with status: {status}")
        if "statistics" in job:
            print(f"Statistics: {job['statistics']}")
        return 0 if status == "COMPLETE" or args.no_wait else 1
    except (ClientError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
