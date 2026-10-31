from scripts.website_fetcher import fetch_website
from scripts.website_parser import extract_website_data
from scripts.website_quality_checks import check_website_quality


def inspect_website(url):
    """
    Fetch a website, extract information, and run quality checks.
    """

    fetch_result = fetch_website(url)

    if not fetch_result["success"]:
        return {
            "website": url,
            "success": False,
            "error": fetch_result.get("error")
        }

    content_type = fetch_result.get("content_type", "")

    if "text/html" not in content_type.lower():
        return {
            "website": url,
            "success": False,
            "error": "Website did not return HTML content."
        }

    extracted_data = extract_website_data(
        fetch_result["html"],
        fetch_result["final_url"]
    )

    result = {
        "website": url,
        "final_url": fetch_result["final_url"],
        "success": True,
        "http_status": fetch_result["status_code"],
        "response_time": fetch_result["response_time"],
        "page_title": extracted_data["page_title"],
        "meta_description": extracted_data["meta_description"],
        "headings": extracted_data["headings"],
        "page_text": extracted_data["page_text"],
        "internal_links": extracted_data["internal_links"],
        "external_links": extracted_data["external_links"],
        "emails": extracted_data["emails"],
        "phone_candidates": extracted_data["phone_candidates"]
    }

    quality_result = check_website_quality({
        "website": url,
        "title": result["page_title"],
        "meta_description": result["meta_description"],
        "headings": result["headings"]
    })

    result["quality_checks"] = quality_result

    return result


if __name__ == "__main__":

    test_url = "https://labeldc.com/"

    print("Inspecting website:", test_url)

    result = inspect_website(test_url)

    print("\nWebsite Inspection Results")
    print("--------------------------")

    for key, value in result.items():

        if key == "page_text":
            print("Extracted text length:", len(value))

        elif key in ("internal_links", "external_links"):
            print(f"{key}: {len(value)} found")

        else:
            print(f"{key}: {value}")