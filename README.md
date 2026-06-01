# SRE AI POC: Intelligent Log Analysis and RCA Assistance using Amazon Bedrock

## Goal

Build an end-to-end POC that:

1. Generates `payment-api` production-style latency/error logs locally.
2. Uploads logs and runbook to Amazon S3.
3. Creates an Amazon Bedrock Knowledge Base from S3.
4. Asks Bedrock: **Analyze payment-api high-latency issue and suggest RCA.**
5. Outputs incident summary, probable root cause, evidence, and remediation steps.

## Architecture

```text
Local VS Code / Python
        |
Generate payment-api logs
        |
Build incident bundle
        |
Upload logs + runbook + bundle to S3
        |
Amazon Bedrock Knowledge Base
        |
Ask RCA question
        |
RCA summary + probable cause + remediation
```

## Project Structure

```text
src/        Python scripts
data/       sample generated logs
runbooks/   payment-api runbook
docs/       step-by-step implementation notes
iam/        sample IAM policy
outputs/    generated incident bundle and RCA answers
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Configure AWS credentials for your account.
aws configure
# If your AWS CLI uses IAM Identity Center, run: aws login

# Copy .env.example to .env and set AWS_REGION, S3_BUCKET, and S3_PREFIX.
python src/aws_preflight.py
python src/create_s3_bucket.py
python src/generate_payment_logs.py
python src/build_incident_bundle.py
python src/upload_to_s3.py
```

Then create the Bedrock Knowledge Base from the uploaded S3 prefix using
`docs/03_create_bedrock_knowledge_base.md`, update `.env` with the Knowledge
Base ID, data source ID, and generation model ARN, and run:

```bash
python src/start_kb_ingestion.py
python src/query_bedrock_kb.py
```

For a faster smoke test before the Knowledge Base exists, use direct Bedrock
Converse with the generated incident bundle:

```bash
python src/query_bedrock_direct_no_kb.py
```

To run the whole workflow after `.env` is ready:

```bash
python src/run_poc.py
```

## Resume Line

Built an end-to-end AI-assisted SRE RCA POC using Python, Amazon S3, Amazon Bedrock Knowledge Bases, and production-style payment API logs to summarize incidents, identify probable root cause, and recommend remediation steps for faster incident triage.
