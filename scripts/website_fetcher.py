
import requests
import time

from urllib.parse import urlparse
from scripts.url_safety import validate_public_url
from urllib.parse import urljoin
from scripts.crawl_policy import (
    check_robots_permission,
    USER_AGENT
)


TIMEOUT = 20
MIN_REQUEST_DELAY = 2

HEADERS = {
    "User-Agent": USER_AGENT
}


def validate_url(url):
    """Validate basic URL structure."""

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if not parsed.hostname:
        raise ValueError("Invalid website URL.")

    return url


def fetch_website(url):
    max_redirects = 5
    current_url = url
    redirect_count = 0

    while True:
        # 1. Validate the current destination.
        allowed, reason = validate_public_url(current_url)

        if not allowed:
            return {
                "requested_url": url,
                "final_url": None,
                "status_code": None,
                "response_time": None,
                "content_type": None,
                "html": None,
                "success": False,
                "error": reason,
            }

        # 2. Check robots.txt for this destination.
        permission = check_robots_permission(current_url)

        if not permission["allowed"]:
            return {
                "requested_url": url,
                "final_url": None,
                "status_code": None,
                "response_time": None,
                "content_type": None,
                "html": None,
                "success": False,
                "error": permission["reason"],
            }

        # 3. Respect the crawl delay.
        delay = max(2, permission.get("crawl_delay") or 0)
        time.sleep(delay)

        # 4. Request without automatically following redirects.
        try:
            response = requests.get(
                current_url,
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
                allow_redirects=False,
            )

        except requests.exceptions.Timeout:
            error = "Request timed out."
        except requests.exceptions.ConnectionError:
            error = "Could not connect to the website."
        except requests.exceptions.RequestException as exception:
            error = str(exception)
        else:
            # 5. Handle redirect responses manually.
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("Location")

                if not location:
                    error = "Redirect response has no Location header."
                elif redirect_count >= max_redirects:
                    error = "Maximum redirect limit reached."
                else:
                    # Resolve relative redirect URLs.
                    current_url = urljoin(current_url, location)
                    redirect_count += 1
                    continue

            else:
                return {
                    "requested_url": url,
                    "final_url": response.url,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "content_type": response.headers.get("Content-Type", ""),
                    "html": response.text,
                    "success": response.status_code == 200,
                    "error": (
                        None
                        if response.status_code == 200
                        else f"Website returned HTTP {response.status_code}"
                    ),
                }

        return {
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "response_time": None,
            "content_type": None,
            "html": None,
            "success": False,
            "error": error,
        }

if __name__ == "__main__":

    test_url = "https://labeldc.com/"

    print("Fetching website:", test_url)

    result = fetch_website(test_url)

    for key, value in result.items():

        if key == "html":
            print("HTML length:", len(value))

        else:
            print(f"{key}: {value}")
