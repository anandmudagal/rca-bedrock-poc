# Step-by-Step Implementation

## 1. Configure AWS and Environment

Copy `.env.example` to `.env`, then set:

```text
AWS_REGION=us-east-1
S3_BUCKET=your-globally-unique-sre-ai-poc-bucket
S3_PREFIX=sre-ai-poc
```

Configure your AWS account credentials:

```bash
aws configure
# If your AWS CLI uses IAM Identity Center, run: aws login
python src/aws_preflight.py
```

## 2. Create S3 Bucket

```bash
python src/create_s3_bucket.py
```

## 3. Install Dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Generate Logs

```bash
python src/generate_payment_logs.py
```

## 5. Build Incident Bundle

```bash
python src/build_incident_bundle.py
```

## 6. Upload to S3

```bash
python src/upload_to_s3.py
```

## 7. Create Bedrock Knowledge Base

Follow `docs/03_create_bedrock_knowledge_base.md`.

## 8. Start Ingestion Job

Update `.env` with `BEDROCK_KB_ID` and `BEDROCK_DATA_SOURCE_ID`, then run:

```bash
python src/start_kb_ingestion.py
```

## 9. Ask RCA Question

```bash
python src/query_bedrock_kb.py
```

## 10. Optional Direct Bedrock Test Before KB

```bash
python src/query_bedrock_direct_no_kb.py
```

## One-command Runner

After the Knowledge Base values are in `.env`, run:

```bash
python src/run_poc.py
```

Before the Knowledge Base exists, you can still run local generation, upload,
and direct Bedrock analysis:

```bash
python src/run_poc.py --direct
```
