from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.clients.ollama_client import OllamaClient
from app.models import AIConversation, AIMessage
from app.schemas.ai import (
    AnomalyExplanationRequest,
    AnomalyExplanationResponse,
    ChatRequest,
    ChatResponse,
    ClaimExplanationRequest,
    ClaimExplanationResponse,
    ReceiptPostProcessRequest,
    ReceiptPostProcessResponse,
    WeeklySummaryRequest,
    WeeklySummaryResponse,
)

ollama = OllamaClient()


def _fallback_text(kind: str, context: dict) -> str:
    if kind == "anomaly":
        anomaly_type = context["anomaly"].get("type", "signal")
        merchant = context["claim"].get("merchant", "unknown vendor")
        return (
            f"Automated review flagged {anomaly_type} for {merchant}. Finance should confirm supporting details, "
            "compare with recent claims, and verify that policy evidence is complete."
        )
    if kind == "claim":
        return "This claim was reviewed with deterministic controls. Use attached receipts, merchant context, and category policy before making a decision."
    if kind == "summary":
        return "Weekly finance view is ready. Focus on flagged claims, pending approvals, and budget hotspots first."
    return "The assistant is temporarily running in fallback mode. Deterministic spend controls remain available."


def explain_claim(db: Session, payload: ClaimExplanationRequest) -> ClaimExplanationResponse:
    result = ollama.render("claim_explanation", {"claim": payload.claim})
    text = result["text"] or _fallback_text("claim", {"claim": payload.claim})
    return ClaimExplanationResponse(explanation=text, provider_status="available" if result["available"] else "fallback")


def explain_anomaly(db: Session, payload: AnomalyExplanationRequest) -> AnomalyExplanationResponse:
    result = ollama.render("anomaly_explanation", {"claim": payload.claim, "anomaly": payload.anomaly})
    text = result["text"] or _fallback_text("anomaly", payload.model_dump())
    return AnomalyExplanationResponse(explanation=text, provider_status="available" if result["available"] else "fallback")


def summarize_weekly_finance(db: Session, payload: WeeklySummaryRequest) -> WeeklySummaryResponse:
    result = ollama.render("weekly_summary", {"analytics": payload.analytics})
    metrics = payload.analytics.get("metrics", [])
    highlights = [f"{metric['label']}: {metric['value']}" for metric in metrics[:3]]
    text = result["text"] or _fallback_text("summary", payload.model_dump())
    return WeeklySummaryResponse(
        week_of=datetime.utcnow().strftime("%Y-%m-%d"),
        summary=text,
        highlights=highlights,
        provider_status="available" if result["available"] else "fallback",
    )


def post_process_receipt(db: Session, payload: ReceiptPostProcessRequest) -> ReceiptPostProcessResponse:
    suggested_category = payload.category_hint or "general"
    if payload.merchant:
        merchant_lower = payload.merchant.lower()
        if "air" in merchant_lower or "hotel" in merchant_lower:
            suggested_category = "travel"
        elif "uber" in merchant_lower or "taxi" in merchant_lower:
            suggested_category = "transport"
        elif "cafe" in merchant_lower or "restaurant" in merchant_lower:
            suggested_category = "meals"
    return ReceiptPostProcessResponse(
        merchant=payload.merchant,
        amount=payload.amount,
        expense_date=payload.expense_date,
        category=suggested_category,
        provider_status="fallback" if not ollama.ping() else "available",
    )


def handle_chat(db: Session, payload: ChatRequest) -> ChatResponse:
    conversation = None
    if payload.conversation_id is not None:
        conversation = db.query(AIConversation).filter(AIConversation.id == payload.conversation_id).first()
    if not conversation:
        conversation = AIConversation(user_id=payload.user_id, title=payload.question[:80])
        db.add(conversation)
        db.flush()

    db.add(AIMessage(conversation_id=conversation.id, role="user", content=payload.question))
    result = ollama.render("chat_assistant", payload.model_dump())
    answer = result["text"] or (
        "I can help summarize spend posture, explain flagged claims, and suggest which budgets deserve attention next."
    )
    db.add(AIMessage(conversation_id=conversation.id, role="assistant", content=answer))
    db.commit()
    return ChatResponse(
        conversation_id=conversation.id,
        answer=answer,
        provider_status="available" if result["available"] else "fallback",
    )
