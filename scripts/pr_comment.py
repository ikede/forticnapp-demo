import json
import traceback
import sys
from pathlib import Path

try:
    report_file = Path("reports/lacework.json")

    if not report_file.exists():
        raise FileNotFoundError("reports/lacework.json was not generated.")

    with report_file.open() as f:
        report = json.load(f)

    print("Successfully loaded FortiCNAPP report")

    markdown = []

    markdown.append("# 🛡️ FortiCNAPP Code Security Report")
    markdown.append("")
    markdown.append("```json")
    markdown.append(json.dumps(report, indent=2)[:5000])
    markdown.append("```")

    Path("reports").mkdir(exist_ok=True)

    with open("reports/pr_comment.md", "w") as f:
        f.write("\n".join(markdown))

    print("Generated reports/pr_comment.md")

except Exception:
    traceback.print_exc()
    sys.exit(1)
