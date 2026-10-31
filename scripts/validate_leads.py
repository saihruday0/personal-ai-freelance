
import json
import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

RESEARCH_FILE = ROOT / "data" / "research_results.json"
AUDIT_FILE = ROOT / "data" / "audit_results.json"
REPORT_DIR = ROOT / "reports"

REPORT_DIR.mkdir(exist_ok=True)


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} must contain a JSON array.")

    return data


def get_evidence(record):
    evidence = (
        record.get("evidence_url")
        or record.get("evidence_urls")
        or []
    )

    if isinstance(evidence, str):
        return [evidence] if evidence.strip() else []

    if isinstance(evidence, list):
        return [url for url in evidence if isinstance(url, str) and url.strip()]

    return []


def main():
    research = load_json(RESEARCH_FILE)
    audits = load_json(AUDIT_FILE)

    audit_by_id = {}
    duplicate_audits = []

    for audit in audits:
        lead_id = audit.get("lead_id")

        if not lead_id:
            continue

        if lead_id in audit_by_id:
            duplicate_audits.append(lead_id)

        audit_by_id[lead_id] = audit

    seen_ids = set()
    duplicate_research = []
    report_lines = []
    csv_rows = []

    verdict_counts = Counter()
    problem_counts = Counter()

    report_lines.append("PERSONAL AI FREELANCING SYSTEM")
    report_lines.append("LEAD VALIDATION REPORT")
    report_lines.append("=" * 45)
    report_lines.append(f"Research records: {len(research)}")
    report_lines.append(f"Audit records: {len(audits)}")
    report_lines.append("")

    for lead in research:
        lead_id = lead.get("lead_id", "UNKNOWN")
        name = lead.get("business_name", "Unnamed business")

        issues = []

        if lead_id in seen_ids:
            duplicate_research.append(lead_id)

        seen_ids.add(lead_id)

        if lead_id == "UNKNOWN":
            issues.append("Missing lead ID")

        if name == "Unnamed business":
            issues.append("Missing business name")

        if not lead.get("website"):
            issues.append("Missing website")

        evidence = get_evidence(lead)

        if not evidence:
            issues.append("No evidence URL recorded")

        classification = (
            lead.get("problem_classification")
            or lead.get("classification")
            or "NOT_CLASSIFIED"
        )

        problem_counts[classification] += 1

        if (
            classification == "VERIFIED_PROBLEM"
            and not evidence
        ):
            issues.append("Verified problem has no evidence URL")

        audit = audit_by_id.get(lead_id)

        if audit:
            verdict = audit.get("verdict", "NO_VERDICT")
            business_status = audit.get(
                "business_verified", "UNKNOWN"
            )
            website_status = audit.get(
                "website_verified", "UNKNOWN"
            )

            verdict_counts[verdict] += 1

            if verdict == "ACCEPT" and (
                business_status != "VERIFIED"
                or website_status != "VERIFIED"
            ):
                issues.append(
                    "ACCEPT verdict requires manual verification"
                )

        else:
            verdict = "NOT_AUDITED"
            business_status = "NOT_CHECKED"
            website_status = "NOT_CHECKED"

        if not issues:
            issues.append("No automatic validation issues found")

        report_lines.extend([
            f"{lead_id} - {name}",
            f"  Classification: {classification}",
            f"  Audit verdict: {verdict}",
            f"  Business: {business_status}",
            f"  Website: {website_status}",
            f"  Evidence URLs: {len(evidence)}",
            f"  Checks: {'; '.join(issues)}",
            ""
        ])

        csv_rows.append({
            "lead_id": lead_id,
            "business_name": name,
            "website": lead.get("website", ""),
            "classification": classification,
            "audit_verdict": verdict,
            "business_verified": business_status,
            "website_verified": website_status,
            "evidence_count": len(evidence),
            "review_notes": "; ".join(issues)
        })

    report_lines.append("=" * 45)
    report_lines.append("SUMMARY")
    report_lines.append("=" * 45)
    report_lines.append(f"Research records: {len(research)}")
    report_lines.append(f"Audited records: {len(audit_by_id)}")
    report_lines.append(
        f"Not audited: {len(research) - len(audit_by_id)}"
    )
    report_lines.append(f"Duplicate research IDs: {duplicate_research}")
    report_lines.append(f"Duplicate audit IDs: {duplicate_audits}")
    report_lines.append("")
    report_lines.append("Audit verdicts:")

    for verdict, count in verdict_counts.items():
        report_lines.append(f"  {verdict}: {count}")

    report_lines.append("")
    report_lines.append("Research classifications:")

    for classification, count in problem_counts.items():
        report_lines.append(f"  {classification}: {count}")

    report_path = REPORT_DIR / "lead_validation_report.txt"
    csv_path = REPORT_DIR / "lead_review.csv"

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=csv_rows[0].keys() if csv_rows else [
                "lead_id", "business_name", "website",
                "classification", "audit_verdict",
                "business_verified", "website_verified",
                "evidence_count", "review_notes"
            ]
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    print("\nLead validation completed.")
    print(f"Research records: {len(research)}")
    print(f"Audit records: {len(audit_by_id)}")
    print(f"Not audited: {len(research) - len(audit_by_id)}")
    print(f"\nReport saved: {report_path}")
    print(f"CSV saved: {csv_path}")


if __name__ == "__main__":
    main()
