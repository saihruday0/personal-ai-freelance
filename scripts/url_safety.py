import ipaddress
import socket
from urllib.parse import urlparse


def validate_public_url(url):
    """
    Allow only HTTP/HTTPS URLs that resolve to public IP addresses.
    Reject local, private, and otherwise non-public destinations.
    """

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False, "Only HTTP and HTTPS URLs are allowed."

        if not parsed.hostname:
            return False, "URL has no hostname."

        if parsed.username or parsed.password:
            return False, "URLs containing credentials are not allowed."

        hostname = parsed.hostname

        if hostname.lower() == "localhost" or hostname.lower().endswith(".localhost"):
            return False, "Localhost URLs are not allowed."

        # Resolve the hostname to IP addresses.
        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM
        )

        if not addresses:
            return False, "Hostname could not be resolved."

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                return False, f"Non-public IP address blocked: {ip}"

        return True, "URL passed the public-address check."

    except (ValueError, socket.gaierror, OSError) as error:
        return False, f"URL validation failed: {error}"