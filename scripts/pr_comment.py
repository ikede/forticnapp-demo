import json
import sys

with open("reports/lacework.json") as f:
    report = json.load(f)

critical = 0
high = 0
medium = 0
low = 0

markdown = []

markdown.append("# 🛡️ FortiCNAPP Code Security Report")
markdown.append("")
markdown.append("| Severity | Count |")
markdown.append("|----------|------:|")

vulnerabilities = report.get("Vulnerabilities", [])

for vuln in vulnerabilities:
    severity = vuln.get("Info", {}).get("Severity", "").lower()

    if severity == "critical":
        critical += 1
    elif severity == "high":
        high += 1
    elif severity == "medium":
        medium += 1
    elif severity == "low":
        low += 1

markdown.append(f"| Critical | {critical} |")
markdown.append(f"| High | {high} |")
markdown.append(f"| Medium | {medium} |")
markdown.append(f"| Low | {low} |")
markdown.append("")

if critical > 0 or high > 0:
    markdown.append("## ❌ Pull Request Failed")
    markdown.append("")
    markdown.append("High or Critical vulnerabilities were detected.")
else:
    markdown.append("## ✅ Pull Request Passed")
    markdown.append("")
    markdown.append("No High or Critical vulnerabilities were detected.")

markdown.append("")
markdown.append("## Vulnerabilities")
markdown.append("")

if not vulnerabilities:
    markdown.append("No third-party vulnerabilities found.")
else:
    for vuln in vulnerabilities:
        info = vuln.get("Info", {})
        severity = info.get("Severity", "Unknown")
        name = info.get("Name", "Unknown")
        markdown.append(f"- **{severity}** — {name}")

with open("reports/pr_comment.md", "w") as f:
    f.write("\n".join(markdown))

if critical > 0 or high > 0:
    sys.exit(1)
