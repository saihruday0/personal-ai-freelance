from types import SimpleNamespace
from unittest.mock import Mock

import scripts.website_fetcher as fetcher


def make_response(status_code, url, headers=None, text=""):
    """Create a fake HTTP response for testing."""

    return SimpleNamespace(
        status_code=status_code,
        url=url,
        headers=headers or {},
        text=text,
        elapsed=SimpleNamespace(total_seconds=lambda: 0.5),
    )


def setup_fetcher(monkeypatch):
    """Mock safety checks and delays so tests don't access real websites."""

    monkeypatch.setattr(
        fetcher,
        "validate_public_url",
        lambda url: (True, "URL is public"),
    )

    monkeypatch.setattr(
        fetcher,
        "check_robots_permission",
        lambda url: {
            "allowed": True,
            "crawl_delay": None,
            "reason": "Allowed",
        },
    )

    monkeypatch.setattr(fetcher.time, "sleep", lambda seconds: None)


def test_follows_legitimate_redirect(monkeypatch):
    setup_fetcher(monkeypatch)

    responses = [
        make_response(
            301,
            "https://example.com",
            {"Location": "https://www.example.com"},
        ),
        make_response(
            200,
            "https://www.example.com",
            text="<html>Website</html>",
        ),
    ]

    mock_get = Mock(side_effect=responses)
    monkeypatch.setattr(fetcher.requests, "get", mock_get)

    result = fetcher.fetch_website("https://example.com")

    assert result["success"] is True
    assert result["final_url"] == "https://www.example.com"
    assert result["status_code"] == 200
    assert mock_get.call_count == 2


def test_blocks_private_redirect(monkeypatch):
    setup_fetcher(monkeypatch)

    def validate_url(url):
        if url == "https://example.com":
            return True, "Public URL"

        return False, "Private IP blocked"

    monkeypatch.setattr(
        fetcher,
        "validate_public_url",
        validate_url,
    )

    mock_get = Mock(
        return_value=make_response(
            302,
            "https://example.com",
            {"Location": "http://192.168.1.1"},
        )
    )

    monkeypatch.setattr(fetcher.requests, "get", mock_get)

    result = fetcher.fetch_website("https://example.com")

    assert result["success"] is False
    assert "Private IP blocked" in result["error"]
    assert mock_get.call_count == 1


def test_redirect_without_location_header(monkeypatch):
    setup_fetcher(monkeypatch)

    mock_get = Mock(
        return_value=make_response(
            301,
            "https://example.com",
        )
    )

    monkeypatch.setattr(fetcher.requests, "get", mock_get)

    result = fetcher.fetch_website("https://example.com")

    assert result["success"] is False
    assert "no Location header" in result["error"]


def test_stops_after_maximum_redirects(monkeypatch):
    setup_fetcher(monkeypatch)

    def redirect_response(url, **kwargs):
        return make_response(
            302,
            url,
            {"Location": f"https://example.com/page{redirect_response.calls}"},
        )

    redirect_response.calls = 0

    def counted_redirect(url, **kwargs):
        redirect_response.calls += 1
        return redirect_response(url, **kwargs)

    monkeypatch.setattr(fetcher.requests, "get", counted_redirect)

    result = fetcher.fetch_website("https://example.com")

    assert result["success"] is False
    assert "Maximum redirect limit" in result["error"]
    assert redirect_response.calls == 6