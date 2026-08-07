import json
import os
import sys

REPORT = "reports/lacework.json"

if not os.path.exists(REPORT):
    print("ERROR: Scan report not found.")
    sys.exit(1)

with open(REPORT, "r") as f:
    report = json.load(f)

# ------------------------------------
# Find vulnerability list automatically
# ------------------------------------

vulnerabilities = []

if isinstance(report, dict):

    if "Vulnerabilities" in report:
        vulnerabilities = report["Vulnerabilities"]

    elif "vulnerabilities" in report:
        vulnerabilities = report["vulnerabilities"]

    elif "packages" in report:

        for package in report["packages"]:

            vulnerabilities.extend(
                package.get("vulnerabilities", [])
            )

# ------------------------------------

critical = 0
high = 0
medium = 0
low = 0

markdown = []

markdown.append("# 🛡️ FortiCNAPP Security Review")
markdown.append("")
markdown.append("## Dependency Scan")
markdown.append("")

markdown.append("| Severity | Count |")
markdown.append("|----------|------:|")

for vuln in vulnerabilities:

    severity = (
        vuln.get("Info", {})
            .get("Severity", "")
            .lower()
    )

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

if critical or high:

    markdown.append("## ❌ Policy Failed")
    markdown.append("")
    markdown.append(
        "High or Critical vulnerabilities were detected."
    )

else:

    markdown.append("## ✅ Policy Passed")
    markdown.append("")
    markdown.append(
        "No High or Critical vulnerabilities detected."
    )

markdown.append("")
markdown.append("---")
markdown.append("")
markdown.append("## Findings")
markdown.append("")

if len(vulnerabilities) == 0:

    markdown.append(
        "No third-party vulnerabilities found."
    )

else:

    for vuln in vulnerabilities:

        info = vuln.get("Info", {})

        severity = info.get("Severity", "Unknown")
        package = info.get("Package", "")
        name = info.get("Name", "Unknown")
        fix = info.get("FixedVersion", "-")

        markdown.append(
            f"- **{severity}** | `{package}` | {name} | Fix: **{fix}**"
        )

os.makedirs("reports", exist_ok=True)

with open("reports/pr_comment.md", "w") as f:
    f.write("\n".join(markdown))

print("Markdown report created.")

if critical or high:
    sys.exit(1)
