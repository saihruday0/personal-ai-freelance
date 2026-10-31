import json
import re
from urllib.parse import urlparse


def normalize_url(url):
    """Normalize a URL for comparison."""

    if not url:
        return ""

    parsed = urlparse(url.strip())

    return (
        parsed.scheme.lower(),
        (parsed.hostname or "").lower().removeprefix("www."),
        parsed.path.rstrip("/"),
    )


def normalize_phone(phone):
    """Keep only digits for phone comparison."""

    return re.sub(r"\D", "", str(phone))


def validate_analysis(ai_response, source_data):
    """
    Validate Qwen's response against the original website data.
    Reject unsupported findings and fabricated contact details.
    """

    # Step 1: Parse Qwen's JSON.
    try:
        analysis = json.loads(ai_response)
    except (json.JSONDecodeError, TypeError):
        return {
            "valid": False,
            "error": "Qwen returned invalid JSON.",
            "accepted_findings": [],
            "rejected_findings": [],
        }

    if not isinstance(analysis, dict):
        return {
            "valid": False,
            "error": "Qwen response must be a JSON object.",
            "accepted_findings": [],
            "rejected_findings": [],
        }

    # Step 2: Verify website identity.
    expected_website = normalize_url(source_data.get("website"))
    reported_website = normalize_url(analysis.get("website"))

    if not expected_website or reported_website != expected_website:
        return {
            "valid": False,
            "error": "Website URL does not match the source data.",
            "accepted_findings": [],
            "rejected_findings": analysis.get("findings", []),
        }

    # Step 3: Build trusted source information.
    source_text = json.dumps(source_data, ensure_ascii=False).lower()

    trusted_phones = set()

    for item in source_data.get("phone_candidates", []):
        if isinstance(item, dict):
            trusted_phones.add(
                normalize_phone(item.get("normalized", ""))
            )
        else:
            trusted_phones.add(normalize_phone(item))

    trusted_emails = {
        str(email).strip().lower()
        for email in source_data.get("emails", [])
    }

    # Step 4: Validate contact information.
    contact = analysis.get("contact_information", {})

    if not isinstance(contact, dict):
        contact = {}

    accepted_phones = []
    for phone in contact.get("phone_candidates", []):
        if normalize_phone(phone) in trusted_phones:
            accepted_phones.append(phone)

    accepted_emails = []
    for email in contact.get("email_candidates", []):
        if str(email).strip().lower() in trusted_emails:
            accepted_emails.append(email)

    # Step 5: Validate findings.
    accepted_findings = []
    rejected_findings = []

    findings = analysis.get("findings", [])

    if not isinstance(findings, list):
        findings = []

    for finding in findings:
        if not isinstance(finding, dict):
            rejected_findings.append({
                "finding": finding,
                "reason": "Finding must be a JSON object."
            })
            continue

        evidence = finding.get("evidence", "")

        if not isinstance(evidence, str) or len(evidence.strip()) < 5:
            rejected_findings.append({
                "finding": finding,
                "reason": "Missing or insufficient evidence."
            })
            continue

        if evidence.lower() not in source_text:
            rejected_findings.append({
                "finding": finding,
                "reason": "Evidence not found in source data."
            })
            continue

        accepted_findings.append(finding)

    # Step 6: Return validated information.
    return {
        "valid": True,
        "website": source_data.get("website"),
        "business_summary": analysis.get("business_summary", ""),
        "accepted_findings": accepted_findings,
        "rejected_findings": rejected_findings,
        "contact_information": {
            "emails": accepted_emails,
            "phones": accepted_phones,
            "verification_note": (
                "Candidates extracted from the website; "
                "not independently verified."
            ),
        },
        "limitations": analysis.get("limitations", []),
        "overall_assessment": analysis.get("overall_assessment", ""),
    }