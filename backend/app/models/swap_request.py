from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from datetime import datetime
import enum
from app.database import Base


class SwapRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class SwapRequest(Base):
    __tablename__ = "swap_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_slot_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    requested_slot_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(SwapRequestStatus), default=SwapRequestStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SwapRequest {self.id} - {self.status}>"