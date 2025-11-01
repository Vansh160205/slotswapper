from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.event import Event, EventStatus
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventWithOwner
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=List[EventResponse])
def get_my_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all events for the current user.
    """
    events = db.query(Event).filter(Event.user_id == current_user.id).order_by(Event.start_time).all()
    return events


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific event by ID.
    """
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return event


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new event for the current user.
    """
    new_event = Event(
        title=event_data.title,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        status=EventStatus.BUSY,
        user_id=current_user.id
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an event.
    """
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is in SWAP_PENDING status
    if event.status == EventStatus.SWAP_PENDING and event_data.status != EventStatus.SWAP_PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify event with pending swap request"
        )
    
    # Update fields
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an event.
    """
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is in SWAP_PENDING status
    if event.status == EventStatus.SWAP_PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete event with pending swap request"
        )
    
    db.delete(event)
    db.commit()
    
    return None