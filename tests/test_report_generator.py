from scripts.report_generator import generate_report


def test_report_contains_business_information():
    analysis = {
        "source_data": {
            "website": "https://labeldc.com/",
            "http_status": 200,
            "page_title": "Label DC",
            "meta_description": "Indo-Western fashion",
            "headings": [
                {"tag": "h1", "text": "Shop Indo-Western Fashion"}
            ],
            "internal_links": [],
            "external_links": [],
            "emails": [],
            "phone_candidates": []
        },
        "validated_analysis": {
            "business_summary": "Online fashion retailer.",
            "business_type": "E-commerce retailer",
            "target_audience": "",
            "accepted_products_or_services": ["Indo-Western dresses"],
            "rejected_products_or_services": [],
            "limitations": ["Pricing not available"],
            "validation_note": "Structure passed."
        }
    }

    report = generate_report(analysis)

    assert "# Business Website Analysis Report" in report
    assert "Online fashion retailer." in report
    assert "Indo-Western dresses" in report
    assert "Pricing not available" in report
    assert "Manual Review Required" in report
    assert "Website Quality Checks" in report
    assert "Checks performed:** 4" in report
    assert "Findings:** 0" in report


def test_report_handles_empty_products():
    analysis = {
        "source_data": {},
        "validated_analysis": {
            "business_summary": "Unknown business.",
            "business_type": "Unknown",
            "target_audience": "",
            "accepted_products_or_services": [],
            "rejected_products_or_services": [],
            "limitations": [],
            "validation_note": ""
        }
    }

    report = generate_report(analysis)

    assert "No supported products or services identified." in report


def test_report_detects_missing_website_information():
    analysis = {
        "source_data": {
            "website": "https://example.com",
            "page_title": "",
            "meta_description": "",
            "headings": []
        },
        "validated_analysis": {
            "business_summary": "Example business.",
            "business_type": "Unknown",
            "target_audience": "",
            "accepted_products_or_services": [],
            "rejected_products_or_services": [],
            "limitations": [],
            "validation_note": ""
        }
    }

    report = generate_report(analysis)

    assert "WQ001" in report
    assert "WQ002" in report
    assert "WQ003" in report
    assert "Findings:** 3" in report