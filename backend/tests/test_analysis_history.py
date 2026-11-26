from app.models.call import Call
from app.models.analysis import CallAnalysis


def create_test_call(db_session):
    call = Call(
        call_reference="TEST-1001",
        agent_name="Test_Agent",
        transcript="Customer requested appointment information."
    )

    db_session.add(call)
    db_session.commit()
    db_session.refresh(call)

    return call


def test_analysis_history_with_records(client, db_session):
    # Create a test call
    call = create_test_call(db_session)

    # Create an analysis record
    analysis = CallAnalysis(
        call_id=call.id,
        summary="Customer requested appointment information.",
        customer_intent="appointment_status",
        sentiment="neutral",
        follow_up_required=False,
        analysis_method="rule_based"
    )

    db_session.add(analysis)
    db_session.commit()

    # Call the API
    response = client.get(
        f"/api/v1/calls/{call.id}/analyses"
    )

    # Verify the response
    assert response.status_code == 200

    data = response.json()

    assert data["call_id"] == call.id
    assert data["total_analyses"] == 1
    assert len(data["analyses"]) == 1
    assert data["analyses"][0]["sentiment"] == "neutral"


def test_analysis_history_without_records(client, db_session):
    call = create_test_call(db_session)

    response = client.get(
        f"/api/v1/calls/{call.id}/analyses"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["call_id"] == call.id
    assert data["total_analyses"] == 0
    assert data["analyses"] == []


def test_analysis_history_invalid_call(client):
    response = client.get("/api/v1/calls/999/analyses")

    assert response.status_code == 404
    assert response.json()["detail"] == "Call not found"


def test_analysis_history_newest_first(client, db_session):
    call = create_test_call(db_session)

    first_analysis = CallAnalysis(
        call_id=call.id,
        summary="First analysis",
        customer_intent="appointment_status",
        sentiment="neutral",
        follow_up_required=False,
        analysis_method="rule_based"
    )

    second_analysis = CallAnalysis(
        call_id=call.id,
        summary="Second analysis",
        customer_intent="appointment_status",
        sentiment="negative",
        follow_up_required=True,
        analysis_method="rule_based"
    )

    db_session.add_all([
        first_analysis,
        second_analysis
    ])
    db_session.commit()

    response = client.get(
        f"/api/v1/calls/{call.id}/analyses"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_analyses"] == 2
    assert data["analyses"][0]["id"] == second_analysis.id
    assert data["analyses"][1]["id"] == first_analysis.id
