# Create Bedrock Knowledge Base from S3

## Prerequisites

1. AWS credentials are configured locally.
2. Bedrock model access is enabled in your selected region.
3. `python src/upload_to_s3.py` has uploaded these files:

```text
s3://<S3_BUCKET>/<S3_PREFIX>/data/sample_payment_logs.jsonl
s3://<S3_BUCKET>/<S3_PREFIX>/runbooks/payment_api_runbook.txt
s3://<S3_BUCKET>/<S3_PREFIX>/outputs/incident_bundle_payment_api.txt
```

Run this check first:

```bash
python src/aws_preflight.py
```

## Console Steps

1. Open Amazon Bedrock console.
2. Confirm you are in the same region as `.env` `AWS_REGION`.
3. Go to Knowledge Bases.
4. Choose Create knowledge base.
5. Name it `sre-ai-log-rca-kb`.
6. Select S3 as the data source.
7. Use S3 URI:

```text
s3://<S3_BUCKET>/<S3_PREFIX>/
```

8. Use fixed-size chunking for this POC. The files are short text/JSONL artifacts, so simple chunking is enough.
9. Choose `Amazon Titan Text Embeddings V2` as the embedding model if available.
10. Let Bedrock create/manage the vector store if the console offers that option. S3 Vectors or OpenSearch Serverless are both fine for this small POC.
11. Let Bedrock create the Knowledge Base service role.
12. Create the Knowledge Base.
13. Open the created Knowledge Base and copy:
    - Knowledge Base ID
    - Data source ID
14. Sync the data source once from the console, or run `python src/start_kb_ingestion.py` after updating `.env`.

The chunking strategy is tied to the data source. To change it later, delete and recreate the data source.

## Update .env

```text
BEDROCK_KB_ID=your_kb_id
BEDROCK_DATA_SOURCE_ID=your_data_source_id
BEDROCK_MODEL_ARN=arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0
```

Adjust the region in the ARN if your `AWS_REGION` is not `us-east-1`.

## Run Ingestion

```bash
python src/start_kb_ingestion.py
```

## Query

```bash
python src/query_bedrock_kb.py
```

The RCA answer is printed and saved to `outputs/rca_from_kb.md`.
