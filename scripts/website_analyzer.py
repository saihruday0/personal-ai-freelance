
import json
from pathlib import Path

from scripts.business_summary_validator import validate_business_summary
from scripts.ollama_client import ask_qwen


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = PROJECT_ROOT / "prompts" / "business_summary_prompt.txt"


def load_analysis_prompt():
    """Read the business summary instructions."""

    if not PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"Business summary prompt not found: {PROMPT_PATH}"
        )

    return PROMPT_PATH.read_text(encoding="utf-8")


def analyze_website(website_data):
    """Generate a focused business summary using extracted website data."""

    prompt_template = load_analysis_prompt()

    # Send only the information needed to understand the business.
    relevant_data = {
        "website": website_data.get("website"),
        "page_title": website_data.get("page_title"),
        "meta_description": website_data.get("meta_description"),
        "headings": website_data.get("headings", []),
        "page_text": (website_data.get("page_text") or "")[:6000],
    }

    website_prompt = (
        "Summarize the business using only this website data.\n\n"
        + json.dumps(relevant_data, indent=2, ensure_ascii=False)
    )

    ai_response = ask_qwen(
        website_prompt,
        system_prompt=prompt_template
    )

    # Retain the complete extracted data for Python-side validation.
    source_data = {
        "website": website_data.get("website"),
        "final_url": website_data.get("final_url"),
        "http_status": website_data.get("http_status"),
        "response_time": website_data.get("response_time"),
        "page_title": website_data.get("page_title"),
        "meta_description": website_data.get("meta_description"),
        "headings": website_data.get("headings", []),
        "page_text": website_data.get("page_text", ""),
        "emails": website_data.get("emails", []),
        "phone_candidates": website_data.get("phone_candidates", []),
        "internal_links": website_data.get("internal_links", []),
        "external_links": website_data.get("external_links", []),
    }

    validated_analysis = validate_business_summary(
        ai_response,
        source_data
    )

    return {
        "source_data": source_data,
        "ai_analysis": ai_response,
        "validated_analysis": validated_analysis,
    }


if __name__ == "__main__":
    sample_path = PROJECT_ROOT / "data" / "sample_leads" / "labeldc_sample.json"

    print("Loading saved website sample...")

    with open(sample_path, "r", encoding="utf-8") as file:
        website_data = json.load(file)

    print("Generating business summary with Qwen...")

    result = analyze_website(website_data)

    print("\nRAW QWEN RESPONSE:")
    print(result["ai_analysis"])

    print("\nVALIDATION RESULT:")
    print(json.dumps(
        result["validated_analysis"],
        indent=2,
        ensure_ascii=False
    ))
    
    output_path = PROJECT_ROOT / "data" / "sample_leads" / "labeldc_analysis.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(f"\nAnalysis saved to: {output_path}")