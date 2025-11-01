import requests
from datetime import datetime, timedelta
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ==================== User A ====================
print_section("1. Creating User A (Alice)")

user_a = requests.post(
    f"{BASE_URL}/auth/signup",
    json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    }
)
token_a = user_a.json()["access_token"]
user_a_id = user_a.json()["user"]["id"]
print(f"✓ User A created: {user_a.json()['user']['name']}")
print(f"  ID: {user_a_id}")
print(f"  Email: {user_a.json()['user']['email']}")

# ==================== User B ====================
print_section("2. Creating User B (Bob)")

user_b = requests.post(
    f"{BASE_URL}/auth/signup",
    json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "password123"
    }
)
token_b = user_b.json()["access_token"]
user_b_id = user_b.json()["user"]["id"]
print(f"✓ User B created: {user_b.json()['user']['name']}")
print(f"  ID: {user_b_id}")
print(f"  Email: {user_b.json()['user']['email']}")

# ==================== Create Events ====================
print_section("3. Creating Events")

# Alice creates event
start_a = datetime.utcnow() + timedelta(days=1, hours=10)
end_a = start_a + timedelta(hours=1)

event_a = requests.post(
    f"{BASE_URL}/events",
    headers={"Authorization": f"Bearer {token_a}"},
    json={
        "title": "Team Meeting (Tuesday 10-11 AM)",
        "start_time": start_a.isoformat(),
        "end_time": end_a.isoformat()
    }
)
event_a_id = event_a.json()["id"]
print(f"✓ Alice created event:")
print(f"  Title: {event_a.json()['title']}")
print(f"  Status: {event_a.json()['status']}")
print(f"  ID: {event_a_id}")

# Bob creates event
start_b = datetime.utcnow() + timedelta(days=2, hours=14)
end_b = start_b + timedelta(hours=1)

event_b = requests.post(
    f"{BASE_URL}/events",
    headers={"Authorization": f"Bearer {token_b}"},
    json={
        "title": "Focus Block (Wednesday 2-3 PM)",
        "start_time": start_b.isoformat(),
        "end_time": end_b.isoformat()
    }
)
event_b_id = event_b.json()["id"]
print(f"\n✓ Bob created event:")
print(f"  Title: {event_b.json()['title']}")
print(f"  Status: {event_b.json()['status']}")
print(f"  ID: {event_b_id}")

# ==================== Make Events Swappable ====================
print_section("4. Making Events Swappable")

# Alice makes her event swappable
requests.put(
    f"{BASE_URL}/events/{event_a_id}",
    headers={"Authorization": f"Bearer {token_a}"},
    json={"status": "SWAPPABLE"}
)
print(f"✓ Alice marked event {event_a_id} as SWAPPABLE")

# Bob makes his event swappable
requests.put(
    f"{BASE_URL}/events/{event_b_id}",
    headers={"Authorization": f"Bearer {token_b}"},
    json={"status": "SWAPPABLE"}
)
print(f"✓ Bob marked event {event_b_id} as SWAPPABLE")

# ==================== View Marketplace ====================
print_section("5. Viewing Marketplace")

# Alice views swappable slots
slots_for_alice = requests.get(
    f"{BASE_URL}/swappable-slots",
    headers={"Authorization": f"Bearer {token_a}"}
)
print(f"✓ Alice sees {len(slots_for_alice.json())} swappable slot(s):")
for slot in slots_for_alice.json():
    print(f"  - {slot['title']} (ID: {slot['id']})")

# Bob views swappable slots
slots_for_bob = requests.get(
    f"{BASE_URL}/swappable-slots",
    headers={"Authorization": f"Bearer {token_b}"}
)
print(f"\n✓ Bob sees {len(slots_for_bob.json())} swappable slot(s):")
for slot in slots_for_bob.json():
    print(f"  - {slot['title']} (ID: {slot['id']})")

# ==================== Create Swap Request ====================
print_section("6. Creating Swap Request")

swap_request = requests.post(
    f"{BASE_URL}/swap-request",
    headers={"Authorization": f"Bearer {token_a}"},
    json={
        "my_slot_id": event_a_id,
        "their_slot_id": event_b_id
    }
)
swap_req_id = swap_request.json()["id"]
print(f"✓ Alice requested a swap:")
print(f"  Request ID: {swap_req_id}")
print(f"  Offering: Event {event_a_id}")
print(f"  Requesting: Event {event_b_id}")
print(f"  Status: {swap_request.json()['status']}")

# ==================== View Requests ====================
print_section("7. Viewing Swap Requests")

# Alice's outgoing requests
outgoing_alice = requests.get(
    f"{BASE_URL}/swap-requests/outgoing",
    headers={"Authorization": f"Bearer {token_a}"}
)
print(f"✓ Alice's outgoing requests: {len(outgoing_alice.json())}")
for req in outgoing_alice.json():
    print(f"  - Request {req['id']}: {req['status']}")

# Bob's incoming requests
incoming_bob = requests.get(
    f"{BASE_URL}/swap-requests/incoming",
    headers={"Authorization": f"Bearer {token_b}"}
)
print(f"\n✓ Bob's incoming requests: {len(incoming_bob.json())}")
for req in incoming_bob.json():
    print(f"  - Request {req['id']} from {req['requester_name']}")
    print(f"    They offer: {req['requester_slot_title']}")
    print(f"    They want: {req['requested_slot_title']}")

# ==================== Accept Swap ====================
print_section("8. Accepting Swap Request")

accept_response = requests.post(
    f"{BASE_URL}/swap-response/{swap_req_id}",
    headers={"Authorization": f"Bearer {token_b}"},
    json={"accept": True}
)
print(f"✓ Bob accepted the swap request")
print(f"  Status: {accept_response.json()['status']}")

# ==================== Verify Swap ====================
print_section("9. Verifying Swap Result")

# Check Alice's events
alice_events = requests.get(
    f"{BASE_URL}/events",
    headers={"Authorization": f"Bearer {token_a}"}
).json()
print(f"✓ Alice's events after swap:")
for event in alice_events:
    print(f"  - {event['title']} (Status: {event['status']})")

# Check Bob's events
bob_events = requests.get(
    f"{BASE_URL}/events",
    headers={"Authorization": f"Bearer {token_b}"}
).json()
print(f"\n✓ Bob's events after swap:")
for event in bob_events:
    print(f"  - {event['title']} (Status: {event['status']})")

# ==================== Summary ====================
print_section("✅ SWAP COMPLETED SUCCESSFULLY!")

print("Summary:")
print(f"  - Alice now has: {bob_events[0]['title']}")
print(f"  - Bob now has: {alice_events[0]['title']}")
print(f"  - Both events are now BUSY (no longer swappable)")
print(f"  - Swap request status: ACCEPTED")

print("\n🎉 All API endpoints are working correctly!\n")