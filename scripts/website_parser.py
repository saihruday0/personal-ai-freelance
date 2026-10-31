
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def normalize_phone_candidates(phone_candidates):
    """
    Normalize phone candidates and remove duplicates.

    Preserve the original extracted formats for reference.
    """

    normalized_numbers = {}

    for phone in phone_candidates:
        digits = re.sub(r"\D", "", phone)

        if not digits:
            continue

        # Normalize common Indian country-code formats.
        if len(digits) == 12 and digits.startswith("91"):
            normalized = digits
        elif len(digits) == 10:
            normalized = "91" + digits
        else:
            normalized = digits

        if normalized not in normalized_numbers:
            normalized_numbers[normalized] = {
                "normalized": "+" + normalized,
                "original_values": []
            }

        if phone not in normalized_numbers[normalized]["original_values"]:
            normalized_numbers[normalized]["original_values"].append(phone)

    return list(normalized_numbers.values())

def extract_website_data(html, base_url):
    """
    Extract useful information from website HTML.
    Does not make HTTP requests.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that don't contain useful page text.
    for element in soup([
        "script",
        "style",
        "noscript",
        "template"
    ]):
        element.decompose()

    # 1. Extract page title
    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

    # 2. Extract meta description
    meta = soup.find(
        "meta",
        attrs={"name": re.compile("^description$", re.I)}
    )

    description = meta.get("content", "") if meta else ""

    # 3. Extract headings
    headings = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(" ", strip=True)

        if text:
            headings.append({
                "tag": tag.name,
                "text": text
            })

    # 4. Extract visible text
    page_text = soup.get_text(" ", strip=True)

    # Limit text to avoid excessive processing.
    page_text = page_text[:30000]

    # 5. Extract links
    internal_links = []
    external_links = []

    base_domain = urlparse(base_url).hostname

    for tag in soup.find_all("a", href=True):

        href = tag["href"].strip()
        absolute_url = urljoin(base_url, href)

        parsed = urlparse(absolute_url)

        if parsed.scheme not in ("http", "https"):
            continue

        link_data = {
            "text": tag.get_text(" ", strip=True),
            "url": absolute_url
        }

        if parsed.hostname == base_domain:
            internal_links.append(link_data)
        else:
            external_links.append(link_data)

    # 6. Extract possible email addresses
    emails = sorted(set(
        re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            page_text
        )
    ))

    # 7. Extract possible phone numbers
    phone_candidates = re.findall(
        r"(?<!\w)\+?\d[\d\s().-]{8,}\d(?!\w)",
        page_text
    )

    phone_numbers = normalize_phone_candidates(
        [
            number.strip()
            for number in phone_candidates
            if 10 <= len(re.sub(r"\D", "", number)) <= 15
        ]
    )

    return {
        "page_title": title,
        "meta_description": description,
        "headings": headings,
        "page_text": page_text,
        "internal_links": internal_links[:100],
        "external_links": external_links[:100],
        "emails": emails,
        "phone_candidates": phone_numbers
    }