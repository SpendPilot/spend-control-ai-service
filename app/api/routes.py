from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.clients.ollama_client import OllamaClient
from app.db.session import get_db
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
from app.services.ai_workflows import (
    explain_anomaly,
    explain_claim,
    handle_chat,
    post_process_receipt,
    summarize_weekly_finance,
)
from spend_control_shared.responses import APIEnvelope, HealthResponse

router = APIRouter()
api = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    ollama_status = "available" if OllamaClient().ping() else "unavailable"
    return HealthResponse(service="ai-service", checks={"ollama": ollama_status})


@api.post("/explanations/claim", response_model=APIEnvelope[ClaimExplanationResponse])
def claim_explanation(payload: ClaimExplanationRequest, db: Session = Depends(get_db)) -> APIEnvelope[ClaimExplanationResponse]:
    return APIEnvelope(data=explain_claim(db, payload))


@api.post("/explanations/anomaly", response_model=APIEnvelope[AnomalyExplanationResponse])
def anomaly_explanation(
    payload: AnomalyExplanationRequest, db: Session = Depends(get_db)
) -> APIEnvelope[AnomalyExplanationResponse]:
    return APIEnvelope(data=explain_anomaly(db, payload))


@api.post("/summaries/weekly", response_model=APIEnvelope[WeeklySummaryResponse])
def weekly_summary(payload: WeeklySummaryRequest, db: Session = Depends(get_db)) -> APIEnvelope[WeeklySummaryResponse]:
    return APIEnvelope(data=summarize_weekly_finance(db, payload))


@api.post("/receipt-post-process", response_model=APIEnvelope[ReceiptPostProcessResponse])
def receipt_post_process(
    payload: ReceiptPostProcessRequest, db: Session = Depends(get_db)
) -> APIEnvelope[ReceiptPostProcessResponse]:
    return APIEnvelope(data=post_process_receipt(db, payload))


@api.post("/chat", response_model=APIEnvelope[ChatResponse])
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> APIEnvelope[ChatResponse]:
    return APIEnvelope(data=handle_chat(db, payload))


router.include_router(api)

