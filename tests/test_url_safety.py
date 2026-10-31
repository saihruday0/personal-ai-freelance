from scripts.url_safety import validate_public_url


def test_allows_public_website():
    allowed, reason = validate_public_url("https://example.com")

    assert allowed is True


def test_blocks_localhost():
    allowed, reason = validate_public_url("http://localhost:8000")

    assert allowed is False


def test_blocks_private_ip():
    allowed, reason = validate_public_url("http://192.168.1.1")

    assert allowed is False


def test_blocks_unsupported_protocol():
    allowed, reason = validate_public_url("ftp://example.com")

    assert allowed is False


def test_blocks_missing_hostname():
    allowed, reason = validate_public_url("https:///")

    assert allowed is False