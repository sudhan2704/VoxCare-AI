
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CallAnalysisResponse(BaseModel):
    id: int
    call_id: int
    summary: str
    customer_intent: str
    sentiment: str
    follow_up_required: bool
    analysis_method: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)



class CallAnalysisHistoryResponse(BaseModel):
    call_id: int
    total_analyses: int
    analyses: list[CallAnalysisResponse]