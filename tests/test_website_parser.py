from scripts.website_parser import normalize_phone_candidates
from scripts.website_parser import extract_website_data


def test_website_parser():

    html = """
    <html>
        <head>
            <title>Test Business</title>
            <meta name="description"
                  content="A test website">
        </head>

        <body>
            <h1>Welcome</h1>

            <p>
                Contact us at hello@example.com
            </p>

            <a href="/about">About</a>
        </body>
    </html>
    """

    result = extract_website_data(
        html,
        "https://example.com"
    )

    print("\nParser Results:")
    print("Title:", result["page_title"])
    print("Description:", result["meta_description"])
    print("Headings:", result["headings"])
    print("Emails:", result["emails"])
    print("Internal Links:", result["internal_links"])

def test_normalizes_duplicate_phone_numbers():
    phones = [
        "+91 9137123542",
        "+91-91371 23542",
        "+919137123542",
    ]

    result = normalize_phone_candidates(phones)

    assert len(result) == 1
    assert result[0]["normalized"] == "+919137123542"
    assert len(result[0]["original_values"]) == 3

if __name__ == "__main__":
    test_website_parser()