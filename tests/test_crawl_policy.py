
from unittest.mock import patch, Mock

from scripts.crawl_policy import check_robots_permission


@patch("scripts.crawl_policy.requests.get")
def test_robots_allows_page(mock_get):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
    User-agent: *
    Allow: /
    """

    mock_get.return_value = mock_response

    result = check_robots_permission(
        "https://example.com/about"
    )

    assert result["allowed"] is True

    print("Allow test:", result)


@patch("scripts.crawl_policy.requests.get")
def test_robots_blocks_page(mock_get):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
    User-agent: *
    Disallow: /private/
    """

    mock_get.return_value = mock_response

    result = check_robots_permission(
        "https://example.com/private/data"
    )

    assert result["allowed"] is False

    print("Block test:", result)


@patch("scripts.crawl_policy.requests.get")
def test_missing_robots_file(mock_get):

    mock_response = Mock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    result = check_robots_permission(
        "https://example.com/about"
    )

    assert result["allowed"] is True

    print("Missing robots.txt test:", result)
