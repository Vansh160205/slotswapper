from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from app.models.event import EventStatus


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    start_time: datetime
    end_time: datetime
    
    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[EventStatus] = None
    
    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if v and 'start_time' in info.data and info.data['start_time']:
            if v <= info.data['start_time']:
                raise ValueError('end_time must be after start_time')
        return v


class EventResponse(EventBase):
    id: int
    status: EventStatus
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EventWithOwner(EventResponse):
    owner_name: str
    owner_email: str