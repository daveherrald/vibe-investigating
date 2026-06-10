#!/usr/bin/env python3
"""Deploy the Lakewatch Research Agent Genie Space config, in place.

Reads lakewatch-research-agent.serialized.json and pushes it to the existing
space via the Databricks REST API. Requires the Databricks CLI authenticated
to the target workspace.

Usage:
    GENIE_SPACE_ID=<id> DATABRICKS_PROFILE=<profile> python3 deploy.py

Defaults target the DH Demo deployment.
"""
import json, os, subprocess, sys, tempfile

SPACE_ID = os.environ.get("GENIE_SPACE_ID", "01f136c1f0ae142fbb37c56981ae2354")
PROFILE  = os.environ.get("DATABRICKS_PROFILE", "DEFAULT")
HERE     = os.path.dirname(os.path.abspath(__file__))

def api(method, path, body=None):
    cmd = ["databricks", "api", method, path, "--profile", PROFILE]
    if body is not None:
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(body, f); f.close()
        cmd += ["--json", "@" + f.name]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or r.stderr.strip().startswith("Error"):
        sys.exit("API error: " + (r.stdout + r.stderr))
    return r.stdout

def main():
    ss = json.load(open(os.path.join(HERE, "lakewatch-research-agent.serialized.json")))
    # Proto requires data_sources.tables sorted by identifier.
    ss["data_sources"]["tables"].sort(key=lambda t: t["identifier"])
    cur = json.loads(api("get", f"/api/2.0/genie/spaces/{SPACE_ID}?include_serialized_space=true"))
    body = {
        "space_id": SPACE_ID,
        "title": cur["title"],
        "description": cur["description"],
        "warehouse_id": cur["warehouse_id"],
        "serialized_space": json.dumps(ss),
        # etag intentionally omitted: the API rejects even a matching etag,
        # so conflict detection is skipped (single-editor workspace).
    }
    api("patch", f"/api/2.0/genie/spaces/{SPACE_ID}", body)
    print(f"Deployed {len(ss['data_sources']['tables'])} tables to space {SPACE_ID}")

if __name__ == "__main__":
    main()
