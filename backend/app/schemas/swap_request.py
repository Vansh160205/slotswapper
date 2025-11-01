from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.models.swap_request import SwapRequestStatus


class SwapRequestCreate(BaseModel):
    my_slot_id: int = Field(..., gt=0)
    their_slot_id: int = Field(..., gt=0)


class SwapResponseUpdate(BaseModel):
    accept: bool


class SwapRequestResponse(BaseModel):
    id: int
    requester_slot_id: int
    requested_slot_id: int
    requester_id: int
    receiver_id: int
    status: SwapRequestStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SwapRequestDetailed(SwapRequestResponse):
    requester_slot_title: str
    requested_slot_title: str
    requester_name: str
    receiver_name: str