import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

USER_AGENT = "PersonalFreelanceResearchBot"

TIMEOUT = 10


def check_robots_permission(url):
    """
    Checks whether our crawler is permitted to access a URL.
    """

    parsed = urlparse(url)

    robots_url = (
        f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    )

    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
            allow_redirects=True
        )

        # No robots.txt file: no published robots rules.
        if response.status_code in (404, 410):
            return {
                "allowed": True,
                "crawl_delay": None,
                "reason": "No robots.txt file found."
            }

        # Explicit access restrictions or server errors:
        # do not crawl.
        if response.status_code != 200:
            return {
                "allowed": False,
                "crawl_delay": None,
                "reason": (
                    f"Could not safely read robots.txt: "
                    f"HTTP {response.status_code}"
                )
            }

        parser.parse(response.text.splitlines())

        allowed = parser.can_fetch(USER_AGENT, url)

        delay = parser.crawl_delay(USER_AGENT)

        return {
            "allowed": allowed,
            "crawl_delay": delay,
            "reason": (
                "Access permitted by robots.txt."
                if allowed
                else "Access disallowed by robots.txt."
            )
        }

    except requests.exceptions.RequestException as error:

        return {
            "allowed": False,
            "crawl_delay": None,
            "reason": f"Robots.txt request failed: {error}"
        }