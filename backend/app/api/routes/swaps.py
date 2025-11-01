from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.event import Event, EventStatus
from app.models.swap_request import SwapRequest, SwapRequestStatus
from app.schemas.event import EventResponse
from app.schemas.swap_request import (
    SwapRequestCreate,
    SwapResponseUpdate,
    SwapRequestResponse,
    SwapRequestDetailed
)
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/swappable-slots", response_model=List[EventResponse])
def get_swappable_slots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all swappable slots from other users.
    """
    slots = db.query(Event).filter(
        Event.status == EventStatus.SWAPPABLE,
        Event.user_id != current_user.id
    ).order_by(Event.start_time).all()
    
    return slots


@router.post("/swap-request", response_model=SwapRequestResponse, status_code=status.HTTP_201_CREATED)
def create_swap_request(
    swap_data: SwapRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a swap request.
    """
    # Verify requester's slot
    my_slot = db.query(Event).filter(
        Event.id == swap_data.my_slot_id,
        Event.user_id == current_user.id
    ).first()
    
    if not my_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your slot not found"
        )
    
    if my_slot.status != EventStatus.SWAPPABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your slot must be marked as SWAPPABLE"
        )
    
    # Verify requested slot
    their_slot = db.query(Event).filter(
        Event.id == swap_data.their_slot_id
    ).first()
    
    if not their_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested slot not found"
        )
    
    if their_slot.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot swap with your own slot"
        )
    
    if their_slot.status != EventStatus.SWAPPABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested slot is not available for swapping"
        )
    
    # Check for existing pending swap request with these slots
    existing_request = db.query(SwapRequest).filter(
        SwapRequest.status == SwapRequestStatus.PENDING,
        (
            (SwapRequest.requester_slot_id == my_slot.id) |
            (SwapRequest.requested_slot_id == my_slot.id) |
            (SwapRequest.requester_slot_id == their_slot.id) |
            (SwapRequest.requested_slot_id == their_slot.id)
        )
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or both slots already have a pending swap request"
        )
    
    # Create swap request
    swap_request = SwapRequest(
        requester_slot_id=my_slot.id,
        requested_slot_id=their_slot.id,
        requester_id=current_user.id,
        receiver_id=their_slot.user_id,
        status=SwapRequestStatus.PENDING
    )
    
    # Update slot statuses to SWAP_PENDING
    my_slot.status = EventStatus.SWAP_PENDING
    their_slot.status = EventStatus.SWAP_PENDING
    
    db.add(swap_request)
    db.commit()
    db.refresh(swap_request)
    
    return swap_request


@router.post("/swap-response/{request_id}", response_model=SwapRequestResponse)
def respond_to_swap_request(
    request_id: int,
    response_data: SwapResponseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accept or reject a swap request.
    """
    # Find the swap request
    swap_request = db.query(SwapRequest).filter(
        SwapRequest.id == request_id,
        SwapRequest.receiver_id == current_user.id
    ).first()
    
    if not swap_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swap request not found"
        )
    
    if swap_request.status != SwapRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Swap request has already been processed"
        )
    
    # Get both slots
    requester_slot = db.query(Event).filter(
        Event.id == swap_request.requester_slot_id
    ).first()
    receiver_slot = db.query(Event).filter(
        Event.id == swap_request.requested_slot_id
    ).first()
    
    if not requester_slot or not receiver_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both slots not found"
        )
    
    if response_data.accept:
        # ACCEPT: Swap the owners
        swap_request.status = SwapRequestStatus.ACCEPTED
        
        # Exchange user_ids
        temp_user_id = requester_slot.user_id
        requester_slot.user_id = receiver_slot.user_id
        receiver_slot.user_id = temp_user_id
        
        # Set both slots back to BUSY
        requester_slot.status = EventStatus.BUSY
        receiver_slot.status = EventStatus.BUSY
    else:
        # REJECT: Reset slots to SWAPPABLE
        swap_request.status = SwapRequestStatus.REJECTED
        requester_slot.status = EventStatus.SWAPPABLE
        receiver_slot.status = EventStatus.SWAPPABLE
    
    db.commit()
    db.refresh(swap_request)
    
    return swap_request


@router.get("/swap-requests/incoming", response_model=List[SwapRequestDetailed])
def get_incoming_swap_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all incoming swap requests for the current user.
    """
    requests = db.query(SwapRequest).filter(
        SwapRequest.receiver_id == current_user.id,
        SwapRequest.status == SwapRequestStatus.PENDING
    ).all()
    
    detailed_requests = []
    for req in requests:
        requester_slot = db.query(Event).filter(Event.id == req.requester_slot_id).first()
        requested_slot = db.query(Event).filter(Event.id == req.requested_slot_id).first()
        requester = db.query(User).filter(User.id == req.requester_id).first()
        
        detailed_requests.append(SwapRequestDetailed(
            id=req.id,
            requester_slot_id=req.requester_slot_id,
            requested_slot_id=req.requested_slot_id,
            requester_id=req.requester_id,
            receiver_id=req.receiver_id,
            status=req.status,
            created_at=req.created_at,
            updated_at=req.updated_at,
            requester_slot_title=requester_slot.title if requester_slot else "Unknown",
            requested_slot_title=requested_slot.title if requested_slot else "Unknown",
            requester_name=requester.name if requester else "Unknown",
            receiver_name=current_user.name
        ))
    
    return detailed_requests


@router.get("/swap-requests/outgoing", response_model=List[SwapRequestDetailed])
def get_outgoing_swap_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all outgoing swap requests for the current user.
    """
    requests = db.query(SwapRequest).filter(
        SwapRequest.requester_id == current_user.id
    ).order_by(SwapRequest.created_at.desc()).all()
    
    detailed_requests = []
    for req in requests:
        requester_slot = db.query(Event).filter(Event.id == req.requester_slot_id).first()
        requested_slot = db.query(Event).filter(Event.id == req.requested_slot_id).first()
        receiver = db.query(User).filter(User.id == req.receiver_id).first()
        
        detailed_requests.append(SwapRequestDetailed(
            id=req.id,
            requester_slot_id=req.requester_slot_id,
            requested_slot_id=req.requested_slot_id,
            requester_id=req.requester_id,
            receiver_id=req.receiver_id,
            status=req.status,
            created_at=req.created_at,
            updated_at=req.updated_at,
            requester_slot_title=requester_slot.title if requester_slot else "Unknown",
            requested_slot_title=requested_slot.title if requested_slot else "Unknown",
            requester_name=current_user.name,
            receiver_name=receiver.name if receiver else "Unknown"
        ))
    
    return detailed_requests


@router.delete("/swap-request/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_swap_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending swap request (only by requester).
    """
    swap_request = db.query(SwapRequest).filter(
        SwapRequest.id == request_id,
        SwapRequest.requester_id == current_user.id
    ).first()
    
    if not swap_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swap request not found"
        )
    
    if swap_request.status != SwapRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending requests"
        )
    
    # Get both slots and reset to SWAPPABLE
    requester_slot = db.query(Event).filter(Event.id == swap_request.requester_slot_id).first()
    receiver_slot = db.query(Event).filter(Event.id == swap_request.requested_slot_id).first()
    
    if requester_slot:
        requester_slot.status = EventStatus.SWAPPABLE
    if receiver_slot:
        receiver_slot.status = EventStatus.SWAPPABLE
    
    db.delete(swap_request)
    db.commit()
    
    return None