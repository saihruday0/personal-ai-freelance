
from unittest.mock import patch

from scripts.website_fetcher import fetch_website


@patch("scripts.website_fetcher.time.sleep")
@patch("scripts.website_fetcher.requests.get")
@patch("scripts.website_fetcher.check_robots_permission")
def test_fetcher_blocks_disallowed_website(
    mock_policy,
    mock_get,
    mock_sleep
):

    mock_policy.return_value = {
        "allowed": False,
        "crawl_delay": None,
        "reason": "Access disallowed by robots.txt."
    }

    result = fetch_website("https://example.com/private")

    assert result["success"] is False
    assert "robots.txt" in result["error"]

    # Website itself must not be fetched.
    mock_get.assert_not_called()

    # No delay needed because crawling was blocked.
    mock_sleep.assert_not_called()

    print("Blocked website test:", result)


@patch("scripts.website_fetcher.time.sleep")
@patch("scripts.website_fetcher.requests.get")
@patch("scripts.website_fetcher.check_robots_permission")
def test_fetcher_allows_permitted_website(
    mock_policy,
    mock_get,
    mock_sleep
):

    mock_policy.return_value = {
        "allowed": True,
        "crawl_delay": None,
        "reason": "Access permitted."
    }

    mock_response = mock_get.return_value

    mock_response.status_code = 200
    mock_response.url = "https://example.com/"
    mock_response.text = "<html>Test</html>"
    mock_response.ok = True
    mock_response.headers = {
        "Content-Type": "text/html"
    }

    result = fetch_website("https://example.com/")

    assert result["success"] is True
    assert result["status_code"] == 200

    mock_sleep.assert_called_once_with(2)

    print("Permitted website test:", result)


def test_fetcher_rejects_invalid_url():

    result = fetch_website("ftp://example.com")

    assert result["success"] is False

    print("Invalid URL test:", result)
