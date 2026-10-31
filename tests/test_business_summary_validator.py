import json

from scripts.business_summary_validator import validate_business_summary


def test_valid_business_summary():
    ai_response = json.dumps({
        "business_summary": "An online fashion retailer.",
        "products_or_services": ["Indo-Western dresses", "Coord sets"],
        "target_audience": "",
        "business_type": "Online retail store",
        "limitations": []
    })

    source_data = {
        "page_title": "Label DC",
        "meta_description": "Shop Indo-Western dresses and coord sets.",
        "headings": [
            {"tag": "h1", "text": "Indo-Western dresses"}
        ],
        "page_text": "Discover our collection of coord sets."
    }

    result = validate_business_summary(ai_response, source_data)

    assert result["valid"] is True
    assert "Indo-Western dresses" in result["accepted_products_or_services"]
    assert "Coord sets" in result["accepted_products_or_services"]


def test_rejects_unsupported_products():
    ai_response = json.dumps({
        "business_summary": "An online fashion retailer.",
        "products_or_services": ["Medical equipment"],
        "target_audience": "",
        "business_type": "Online retail store",
        "limitations": []
    })

    source_data = {
        "page_title": "Label DC",
        "meta_description": "Online fashion store.",
        "headings": [],
        "page_text": "Shop our clothing collection."
    }

    result = validate_business_summary(ai_response, source_data)

    assert result["valid"] is True
    assert len(result["rejected_products_or_services"]) == 1


def test_rejects_invalid_json():
    result = validate_business_summary(
        "This is not JSON",
        {}
    )

    assert result["valid"] is False