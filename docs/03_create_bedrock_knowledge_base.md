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

## Console IAM Permissions

Do not create the Knowledge Base while signed in as the AWS root user. Sign in as
an IAM user or IAM Identity Center role.

For this learning POC, the fastest setup is to attach these AWS managed policies
to the IAM identity that will create the Knowledge Base in the console:

```text
AmazonBedrockFullAccess
AmazonS3FullAccess
IAMFullAccess
AWSLambda_ReadOnlyAccess
AmazonOpenSearchServiceFullAccess
```

The Bedrock console may call Lambda APIs while loading console options. If you
see `lambda:ListFunctions` access denied, add `AWSLambda_ReadOnlyAccess`.

If Bedrock creates an Amazon OpenSearch Serverless vector store for the
Knowledge Base, the console identity also needs OpenSearch Serverless `aoss`
permissions. If `AmazonOpenSearchServerlessFullAccess` is available in IAM,
attach it. If it is not available, add this inline policy to the IAM user or
role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "OpenSearchServerlessForBedrockKnowledgeBase",
      "Effect": "Allow",
      "Action": [
        "aoss:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CreateOpenSearchServerlessServiceLinkedRole",
      "Effect": "Allow",
      "Action": [
        "iam:CreateServiceLinkedRole"
      ],
      "Resource": "*"
    }
  ]
}
```

This resolves errors like:

```text
AccessDeniedException: not authorized to perform: aoss:CreateSecurityPolicy
```

For production, replace the broad managed policies and `aoss:*` statement with
least-privilege policies scoped to the specific bucket, Knowledge Base, service
role, and OpenSearch Serverless collection.

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
