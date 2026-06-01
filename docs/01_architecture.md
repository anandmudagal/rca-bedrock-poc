# Architecture

```text
Local Python App
  -> sample payment-api logs
  -> incident bundle
  -> S3
  -> Bedrock Knowledge Base
  -> RCA response
```

## Enterprise Extension

```text
Splunk / CloudWatch Logs
  -> Lambda / scheduled ETL
  -> curated incident bundle
  -> S3
  -> Bedrock Knowledge Base
  -> SRE RCA Assistant
  -> ServiceNow / Slack / PagerDuty
```

## Important Design Rule

Do not ingest all raw production logs into Bedrock Knowledge Base.
Ingest curated incident bundles, runbooks, known errors, and RCA documents.
