import pytest
from fastapi import status


def test_signup(client):
    response = client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"


def test_signup_duplicate_email(client):
    # First signup
    client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Try to signup with same email
    response = client.post(
        "/api/auth/signup",
        json={
            "name": "Test User 2",
            "email": "test@example.com",
            "password": "testpassword456"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login(client):
    # Signup first
    client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client):
    # Signup first
    client.post(
        "/api/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED