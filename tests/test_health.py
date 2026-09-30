# Mourad.Soltani
from fastapi.testclient import TestClient

from quotefence.app import app
from quotefence.engine import fence_quote, scan_risks

client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "quotefence"
    assert body["author"] == "Mourad.Soltani"


def test_fence_rejects_short_brief():
    response = client.post("/v1/fence", json={"brief": "tiny"})
    assert response.status_code == 422


def test_fence_flags_unlimited_and_asap():
    brief = (
        "Please rebuild the marketing site with unlimited revisions and ship ASAP. "
        "Also add a shop, blog, etc."
    )
    response = client.post(
        "/v1/fence",
        json={"brief": brief, "title": "Marketing rebuild", "validity_days": 10},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Marketing rebuild"
    assert body["validity_days"] == 10
    codes = {item["code"] for item in body["risks"]}
    assert "unlimited-work" in codes
    assert "timeline" in codes
    assert "open-ended" in codes
    assert body["risk_score"] >= 40
    assert "Change orders" in body["markdown"]
    assert "Mourad.Soltani" in body["markdown"]


def test_engine_requires_brief():
    try:
        fence_quote("")
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_scan_clean_brief_has_no_flags():
    flags = scan_risks("Build a five-page brochure site with two revision rounds.")
    assert flags == []
