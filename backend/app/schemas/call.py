
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.analysis import CallAnalysisResponse


class CallCreate(BaseModel):
    call_reference: str
    agent_name: str
    transcript: str


class CallResponse(BaseModel):
    id: int
    call_reference: str
    agent_name: str
    transcript: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CallDetailResponse(BaseModel):
    call_reference: str
    agent_name: str
    transcript: str
    status: str
    created_at: datetime
    analysis: CallAnalysisResponse | None = None

    model_config = ConfigDict(from_attributes=True)
