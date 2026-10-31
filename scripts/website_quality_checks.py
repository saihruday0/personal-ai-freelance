
def check_website_quality(website_data):
    """
    Identify basic, observable website quality issues.
    These are technical observations, not proof of lost sales.
    """

    findings = []

    title = (website_data.get("title") or "").strip()
    meta_description = (
        website_data.get("meta_description") or ""
    ).strip()

    headings = website_data.get("headings") or []

    h1_headings = [
        item.get("text", "").strip()
        for item in headings
        if isinstance(item, dict)
        and item.get("tag") == "h1"
        and item.get("text", "").strip()
    ]

    if not title:
        findings.append({
            "id": "WQ001",
            "category": "SEO",
            "severity": "warning",
            "finding": "Page title is missing.",
            "evidence": "The extracted page title is empty.",
        })

    if not meta_description:
        findings.append({
            "id": "WQ002",
            "category": "SEO",
            "severity": "info",
            "finding": "Meta description is missing.",
            "evidence": "The extracted meta description is empty.",
        })

    if not h1_headings:
        findings.append({
            "id": "WQ003",
            "category": "Structure",
            "severity": "warning",
            "finding": "No H1 heading was detected.",
            "evidence": "No non-empty H1 heading was extracted.",
        })

    elif len(h1_headings) > 1:
        findings.append({
            "id": "WQ004",
            "category": "Structure",
            "severity": "info",
            "finding": "Multiple H1 headings were detected.",
            "evidence": h1_headings,
        })

    return {
        "website": website_data.get("website", ""),
        "checks_performed": 4,
        "findings_count": len(findings),
        "findings": findings,
    }
