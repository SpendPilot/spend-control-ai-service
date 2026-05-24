from app.schemas.ai import AnomalyExplanationRequest
from app.services.ai_workflows import explain_anomaly


class DummyDB:
    pass


def test_anomaly_explanation_returns_text():
    payload = AnomalyExplanationRequest(
        claim={"merchant": "Atlas Air"},
        anomaly={"type": "rounded_amount"},
    )
    result = explain_anomaly(DummyDB(), payload)
    assert result.explanation

