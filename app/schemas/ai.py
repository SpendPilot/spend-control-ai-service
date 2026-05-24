from pydantic import BaseModel, Field


class ClaimExplanationRequest(BaseModel):
    claim: dict


class ClaimExplanationResponse(BaseModel):
    explanation: str
    provider_status: str


class AnomalyExplanationRequest(BaseModel):
    claim: dict
    anomaly: dict


class AnomalyExplanationResponse(BaseModel):
    explanation: str
    provider_status: str


class WeeklySummaryRequest(BaseModel):
    analytics: dict


class WeeklySummaryResponse(BaseModel):
    week_of: str
    summary: str
    highlights: list[str]
    provider_status: str


class ReceiptPostProcessRequest(BaseModel):
    merchant: str | None = None
    amount: float | None = None
    expense_date: str | None = None
    category_hint: str | None = None


class ReceiptPostProcessResponse(BaseModel):
    merchant: str | None = None
    amount: float | None = None
    expense_date: str | None = None
    category: str | None = None
    provider_status: str


class ChatRequest(BaseModel):
    user_id: int
    role: str
    question: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    provider_status: str = Field(default="unavailable")

