from pathlib import Path


def test_business_summary_prompt_exists():
    prompt_path = (
        Path(__file__).resolve().parents[1]
        / "prompts"
        / "business_summary_prompt.txt"
    )

    assert prompt_path.exists()

    prompt = prompt_path.read_text(encoding="utf-8")

    assert "business_summary" in prompt
    assert "Never invent" in prompt
    assert "valid JSON" in prompt