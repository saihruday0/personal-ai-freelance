
from unittest.mock import patch

from scripts.website_inspector import inspect_website


@patch("scripts.website_inspector.fetch_website")
def test_successful_website_inspection(mock_fetch):

    mock_fetch.return_value = {
        "success": True,
        "final_url": "https://example.com/",
        "status_code": 200,
        "response_time": 1.2,
        "content_type": "text/html",
        "html": """
        <html>
            <head>
                <title>Example Business</title>
            </head>
            <body>
                <h1>Welcome</h1>
                <p>Contact hello@example.com</p>
                <a href="/about">About</a>
            </body>
        </html>
        """
    }

    result = inspect_website("https://example.com/")

    assert result["success"] is True
    assert result["http_status"] == 200
    assert result["page_title"] == "Example Business"
    assert len(result["headings"]) == 1
    assert "hello@example.com" in result["emails"]

    print("\nInspection test:", result)


@patch("scripts.website_inspector.fetch_website")
def test_failed_website_fetch(mock_fetch):

    mock_fetch.return_value = {
        "success": False,
        "error": "Connection failed"
    }

    result = inspect_website("https://example.com/")

    assert result["success"] is False
    assert result["error"] == "Connection failed"

    print("\nFailed fetch test:", result)


@patch("scripts.website_inspector.fetch_website")
def test_non_html_response(mock_fetch):

    mock_fetch.return_value = {
        "success": True,
        "content_type": "application/pdf"
    }

    result = inspect_website("https://example.com/document")

    assert result["success"] is False
    assert "HTML" in result["error"]

    print("\nNon-HTML test:", result)

@patch("scripts.website_inspector.fetch_website")
def test_successful_inspection_includes_quality_checks(mock_fetch):

    mock_fetch.return_value = {
        "success": True,
        "final_url": "https://example.com/",
        "status_code": 200,
        "response_time": 1.2,
        "content_type": "text/html",
        "html": """
        <html>
            <head>
                <title>Example Business</title>
                <meta name="description" content="Example description">
            </head>
            <body>
                <h1>Welcome</h1>
            </body>
        </html>
        """
    }

    result = inspect_website("https://example.com/")

    assert result["success"] is True
    assert "quality_checks" in result

    quality = result["quality_checks"]

    assert quality["checks_performed"] == 4
    assert quality["findings_count"] == 0
    assert quality["findings"] == []