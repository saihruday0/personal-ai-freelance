import json
from pathlib import Path


def test_saved_analysis_exists_and_is_valid():
    project_root = Path(__file__).resolve().parents[1]

    analysis_path = (
        project_root
        / "data"
        / "sample_leads"
        / "labeldc_analysis.json"
    )

    assert analysis_path.exists()

    with open(analysis_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert "source_data" in data
    assert "ai_analysis" in data
    assert "validated_analysis" in data

    assert data["validated_analysis"]["valid"] is True