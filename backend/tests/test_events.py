import pytest
from datetime import datetime, timedelta
from fastapi import status


def get_auth_header(client):
    response = client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_event(client):
    headers = get_auth_header(client)
    
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    response = client.post(
        "/api/events",
        json={
            "title": "Test Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        headers=headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Event"
    assert data["status"] == "BUSY"


def test_get_events(client):
    headers = get_auth_header(client)
    
    # Create an event
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    client.post(
        "/api/events",
        json={
            "title": "Test Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        headers=headers
    )
    
    # Get events
    response = client.get("/api/events", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Event"


def test_update_event(client):
    headers = get_auth_header(client)
    
    # Create an event
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    create_response = client.post(
        "/api/events",
        json={
            "title": "Test Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        headers=headers
    )
    event_id = create_response.json()["id"]
    
    # Update the event
    response = client.put(
        f"/api/events/{event_id}",
        json={"status": "SWAPPABLE"},
        headers=headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "SWAPPABLE"


def test_delete_event(client):
    headers = get_auth_header(client)
    
    # Create an event
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    create_response = client.post(
        "/api/events",
        json={
            "title": "Test Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        headers=headers
    )
    event_id = create_response.json()["id"]
    
    # Delete the event
    response = client.delete(f"/api/events/{event_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deletion
    get_response = client.get("/api/events", headers=headers)
    assert len(get_response.json()) == 0