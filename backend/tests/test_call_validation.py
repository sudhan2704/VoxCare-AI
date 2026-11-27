
def test_create_call_with_valid_data(client):
    response = client.post(
        "/api/v1/calls/",
        json={
            "call_reference": "VC-TEST-VALID",
            "agent_name": "Agent_Test",
            "transcript": "Customer requested appointment information."
        }
    )

    assert response.status_code == 200
    assert response.json()["call_reference"] == "VC-TEST-VALID"


def test_create_call_with_empty_transcript(client):
    response = client.post(
        "/api/v1/calls/",
        json={
            "call_reference": "VC-TEST-EMPTY",
            "agent_name": "Agent_Test",
            "transcript": ""
        }
    )

    assert response.status_code == 422


def test_create_call_with_blank_agent_name(client):
    response = client.post(
        "/api/v1/calls/",
        json={
            "call_reference": "VC-TEST-BLANK",
            "agent_name": "   ",
            "transcript": "Customer requested appointment information."
        }
    )

    assert response.status_code == 422


def test_create_call_with_blank_call_reference(client):
    response = client.post(
        "/api/v1/calls/",
        json={
            "call_reference": "   ",
            "agent_name": "Agent_Test",
            "transcript": "Customer requested appointment information."
        }
    )

    assert response.status_code == 422


def test_create_call_with_long_call_reference(client):
    response = client.post(
        "/api/v1/calls/",
        json={
            "call_reference": "A" * 101,
            "agent_name": "Agent_Test",
            "transcript": "Customer requested appointment information."
        }
    )

    assert response.status_code == 422


def test_create_call_with_duplicate_reference(client):
    payload = {
        "call_reference": "VC-DUPLICATE-001",
        "agent_name": "Agent_Test",
        "transcript": "Customer requested appointment information."
    }

    # First request should create the call
    first_response = client.post(
        "/api/v1/calls/",
        json=payload
    )

    assert first_response.status_code == 200

    # Second request should be rejected
    second_response = client.post(
        "/api/v1/calls/",
        json=payload
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Call reference already exists"
    )

