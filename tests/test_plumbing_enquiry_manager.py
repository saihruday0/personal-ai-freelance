import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
DEMO_DIR = PROJECT_DIR / "projects" / "plumbing_enquiry_manager"

sys.path.insert(0, str(DEMO_DIR))

import database
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATA_DIR", tmp_path)
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")

    database.init_db()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_submit_enquiry(client):
    response = client.post("/submit", data={
        "customer_name": "John Smith",
        "email": "john@example.com",
        "phone": "07123456789",
        "service": "Leak Repair",
        "message": "Water leaking under kitchen sink."
    }, follow_redirects=True)

    assert b"submitted successfully" in response.data

    enquiries = database.get_enquiries()
    assert len(enquiries) == 1
    assert enquiries[0]["customer_name"] == "John Smith"
    assert enquiries[0]["status"] == "New"


def test_reject_incomplete_enquiry(client):
    response = client.post("/submit", data={
        "customer_name": "",
        "email": "john@example.com",
        "phone": "07123456789",
        "service": "Leak Repair"
    }, follow_redirects=True)

    assert b"complete all required fields" in response.data
    assert database.get_enquiries() == []


def test_update_enquiry_status(client):
    database.add_enquiry(
        "John Smith",
        "john@example.com",
        "07123456789",
        "Leak Repair",
        "Water leaking under kitchen sink."
    )

    response = client.post(
        "/update-status/1",
        data={"status": "Contacted"},
        follow_redirects=True
    )

    assert response.status_code == 200

    enquiries = database.get_enquiries()
    assert enquiries[0]["status"] == "Contacted"