from dataclasses import dataclass


@dataclass
class Lead:
    business_name: str
    website: str
    observed_problem: str
    evidence_url: str
    has_relevant_contact: bool = False
    suspicious: bool = False


def qualify(lead: Lead) -> tuple[str, list[str]]:
    reasons = []

    if not lead.website.startswith(("https://", "http://")):
        reasons.append("Website URL needs verification")

    if not lead.observed_problem.strip():
        reasons.append("No specific business problem identified")

    if not lead.evidence_url.strip():
        reasons.append("No supporting evidence recorded")

    if lead.suspicious:
        reasons.append("Potential scam or trust concern")

    if reasons:
        return "needs_review", reasons

    if not lead.has_relevant_contact:
        return "qualified_needs_contact", [
            "Business fit looks plausible; find an appropriate contact"
        ]

    return "qualified", ["Evidence and contact details need human review"]


if __name__ == "__main__":
    samples = [
        Lead(
            "Example Creator",
            "https://example.com",
            "No clear enquiry process is visible in the supplied review notes",
            "https://example.com/about",
            has_relevant_contact=True,
        ),
        Lead(
            "Incomplete Business",
            "",
            "",
            "",
        ),
        Lead(
            "Unverified Prospect",
            "https://example.org",
            "Potential workflow problem",
            "https://example.org",
            suspicious=True,
        ),
    ]

    for lead in samples:
        status, reasons = qualify(lead)
        print(f"\n{lead.business_name}: {status}")
        for reason in reasons:
            print(f" - {reason}")