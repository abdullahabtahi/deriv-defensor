from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class PartnerBase(BaseModel):
    partner_id: str
    region: str
    tier: str # 'Bronze', 'Silver', 'Gold', 'Platinum'
    join_date: Optional[str] = None
    status: str = "Active"
    
class PartnerRisk(PartnerBase):
    churn_prob: float
    risk_category: Optional[str] = None
    urgency_score: Optional[int] = None
    login_trend_30d: Optional[float] = None
    payment_delay_flag: bool = False
    unresolved_ticket_count: int = 0
    ltv: float = 0.0

class InterventionCreate(BaseModel):
    partner_id: str
    action_type: str
    explanation_text: Optional[str] = None
    email_draft: Optional[str] = None
    performed_by: str = "System"

class InterventionResponse(InterventionCreate):
    id: UUID
    timestamp: datetime
    status: str
    outcome_label: Optional[str] = None
