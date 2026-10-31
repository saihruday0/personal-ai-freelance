import json

from scripts.analysis_validator import validate_analysis


def get_source_data():
    return {
        "website": "https://labeldc.com/",
        "phone_candidates": [
            {
                "normalized": "+919137123542",
                "original_values": ["+91 9137123542"]
            }
        ],
        "emails": [],
        "page_title": "Label DC | Indo Western Dresses",
        "page_text": "Shop Indo Western dresses and coord sets.",
    }


def test_rejects_wrong_website():
    source = get_source_data()

    ai_response = json.dumps({
        "website": "https://www.sareequeen.com",
        "findings": []
    })

    result = validate_analysis(ai_response, source)

    assert result["valid"] is False
    assert "does not match" in result["error"]


def test_rejects_invented_phone_number():
    source = get_source_data()

    ai_response = json.dumps({
        "website": "https://labeldc.com/",
        "contact_information": {
            "phone_candidates": ["+91 9999999999"],
            "email_candidates": []
        },
        "findings": []
    })

    result = validate_analysis(ai_response, source)

    assert result["valid"] is True
    assert result["contact_information"]["phones"] == []


def test_accepts_original_phone_number():
    source = get_source_data()

    ai_response = json.dumps({
        "website": "https://labeldc.com/",
        "contact_information": {
            "phone_candidates": ["+919137123542"],
            "email_candidates": []
        },
        "findings": []
    })

    result = validate_analysis(ai_response, source)

    assert result["contact_information"]["phones"] == [
        "+919137123542"
    ]


def test_rejects_unsupported_evidence():
    source = get_source_data()

    ai_response = json.dumps({
        "website": "https://labeldc.com/",
        "findings": [
            {
                "title": "Fake finding",
                "evidence": "The website has 500 broken links."
            }
        ]
    })

    result = validate_analysis(ai_response, source)

    assert len(result["accepted_findings"]) == 0
    assert len(result["rejected_findings"]) == 1


def test_rejects_invalid_json():
    source = get_source_data()

    result = validate_analysis("This is not JSON", source)

    assert result["valid"] is False
    assert result["accepted_findings"] == []