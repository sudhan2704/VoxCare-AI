from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.analysis import CallAnalysisResponse

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

class CallCreate(BaseModel):
    call_reference: str = Field(
        min_length=1,
        max_length=100
    )
    agent_name: str = Field(
        min_length=1,
        max_length=100
    )
    transcript: str = Field(
        min_length=1
    )

    model_config = ConfigDict(str_strip_whitespace=True)
