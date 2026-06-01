# Resume and Interview Notes

## Resume Bullet

Built an end-to-end AI-assisted SRE RCA proof-of-concept using Python, Amazon S3, Amazon Bedrock Knowledge Bases, and production-style payment API logs to summarize incidents, identify probable root cause, and recommend remediation steps for faster incident triage.

## Interview Explanation

I generated payment-api logs locally, simulated high-latency and DB timeout errors, created a runbook, uploaded the data to S3, and connected it to Amazon Bedrock Knowledge Base. Then I used Bedrock to analyze the incident, summarize symptoms, identify probable root cause, and recommend remediation steps.

## Production Value

- Reduces manual log analysis
- Accelerates RCA
- Creates consistent incident summaries
- Connects logs with runbook knowledge
- Can integrate with Splunk, CloudWatch Logs, ServiceNow, and Slack
