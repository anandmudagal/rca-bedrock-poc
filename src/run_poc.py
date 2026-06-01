from __future__ import annotations

import argparse
import subprocess
import sys


def run_step(command: list[str]) -> int:
    print(f"\n$ {' '.join(command)}")
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SRE AI RCA POC workflow.")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--bucket")
    parser.add_argument("--prefix")
    parser.add_argument("--region")
    parser.add_argument("--skip-upload", action="store_true")
    parser.add_argument("--skip-ingestion", action="store_true")
    parser.add_argument("--local-only", action="store_true", help="Only generate logs and build the incident bundle.")
    parser.add_argument("--direct", action="store_true", help="Use direct Bedrock Converse instead of a Knowledge Base.")
    args = parser.parse_args()

    steps = [
        [args.python, "src/generate_payment_logs.py"],
        [args.python, "src/build_incident_bundle.py"],
    ]

    if args.local_only:
        for step in steps:
            return_code = run_step(step)
            if return_code != 0:
                return return_code
        return 0

    if not args.skip_upload:
        upload = [args.python, "src/upload_to_s3.py"]
        if args.bucket:
            upload.extend(["--bucket", args.bucket])
        if args.prefix:
            upload.extend(["--prefix", args.prefix])
        if args.region:
            upload.extend(["--region", args.region])
        steps.append(upload)

    if args.direct:
        direct = [args.python, "src/query_bedrock_direct_no_kb.py"]
        if args.region:
            direct.extend(["--region", args.region])
        steps.append(direct)
    else:
        if not args.skip_ingestion:
            ingestion = [args.python, "src/start_kb_ingestion.py"]
            if args.region:
                ingestion.extend(["--region", args.region])
            steps.append(ingestion)
        kb_query = [args.python, "src/query_bedrock_kb.py"]
        if args.region:
            kb_query.extend(["--region", args.region])
        steps.append(kb_query)

    for step in steps:
        return_code = run_step(step)
        if return_code != 0:
            return return_code

    return 0


if __name__ == "__main__":
    sys.exit(main())
