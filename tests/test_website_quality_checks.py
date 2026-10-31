
from scripts.website_quality_checks import check_website_quality


def test_complete_website_has_no_findings():
    website = {
        "website": "https://example.com",
        "title": "Example Store",
        "meta_description": "Welcome to our store.",
        "headings": [
            {"tag": "h1", "text": "Welcome"}
        ],
    }

    result = check_website_quality(website)

    assert result["findings_count"] == 0


def test_missing_title_is_detected():
    website = {
        "website": "https://example.com",
        "title": "",
        "meta_description": "Description",
        "headings": [
            {"tag": "h1", "text": "Welcome"}
        ],
    }

    result = check_website_quality(website)

    assert "WQ001" in [
        item["id"] for item in result["findings"]
    ]


def test_missing_h1_is_detected():
    website = {
        "website": "https://example.com",
        "title": "Example",
        "meta_description": "Description",
        "headings": [],
    }

    result = check_website_quality(website)

    assert "WQ003" in [
        item["id"] for item in result["findings"]
    ]


def test_multiple_h1_headings_are_detected():
    website = {
        "website": "https://example.com",
        "title": "Example",
        "meta_description": "Description",
        "headings": [
            {"tag": "h1", "text": "First"},
            {"tag": "h1", "text": "Second"},
        ],
    }

    result = check_website_quality(website)

    assert "WQ004" in [
        item["id"] for item in result["findings"]
    ]
