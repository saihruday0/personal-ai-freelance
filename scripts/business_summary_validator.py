
import json


def validate_business_summary(ai_response, source_data):
    """Validate business summary structure and product evidence."""

    try:
        summary = json.loads(ai_response)
    except (json.JSONDecodeError, TypeError):
        return {"valid": False, "error": "AI response is not valid JSON."}

    required_fields = {
        "business_summary": str,
        "products_or_services": list,
        "target_audience": str,
        "business_type": str,
        "limitations": list,
    }

    for field, expected_type in required_fields.items():
        if field not in summary:
            return {"valid": False, "error": f"Missing field: {field}"}
        if not isinstance(summary[field], expected_type):
            return {"valid": False, "error": f"Invalid type: {field}"}

    if not all(isinstance(x, str) for x in summary["products_or_services"]):
        return {"valid": False, "error": "Products/services must be strings."}

    if not all(isinstance(x, str) for x in summary["limitations"]):
        return {"valid": False, "error": "Limitations must be strings."}

    headings = source_data.get("headings") or []
    heading_text = " ".join(
        item.get("text", "")
        for item in headings
        if isinstance(item, dict)
    )

    evidence_text = " ".join([
        str(source_data.get("page_title") or ""),
        str(source_data.get("meta_description") or ""),
        heading_text,
        str(source_data.get("page_text") or ""),
    ]).casefold()

    accepted = []
    rejected = []

    for item in summary["products_or_services"]:
        normalized = item.strip().casefold()

        if normalized and normalized in evidence_text:
            accepted.append(item)
        else:
            rejected.append({
                "item": item,
                "reason": "No exact supporting text found."
            })

    return {
        "valid": True,
        "business_summary": summary["business_summary"],
        "business_type": summary["business_type"],
        "target_audience": summary["target_audience"],
        "accepted_products_or_services": accepted,
        "rejected_products_or_services": rejected,
        "limitations": summary["limitations"],
        "validation_note": (
            "Structure passed. Exact text matching is not proof of factual accuracy."
        )
    }
