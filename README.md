# 🔄 SlotSwapper - Peer-to-Peer Time Slot Scheduling Application

<div align="center">

![SlotSwapper Banner](https://img.shields.io/badge/SlotSwapper-Time%20Slot%20Exchange-blue?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**A modern, full-stack web application enabling users to swap calendar time slots with each other in a peer-to-peer marketplace.**

[Features](#features) • [Tech Stack](#tech-stack) • [Quick Start](#quick-start) • [API Documentation](#api-documentation) • [Screenshots](#screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture & Design Choices](#architecture--design-choices)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Assumptions & Challenges](#assumptions--challenges)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**SlotSwapper** is a peer-to-peer time-slot scheduling application that allows users to exchange calendar events. Users can mark their busy time slots as "swappable," browse other users' available slots, and request swaps. When a swap is accepted, the calendar events are automatically exchanged between users.

### 💡 Use Case Example

1. **User A** has a "Team Meeting" on Tuesday 10:00-11:00 AM → marks as **SWAPPABLE**
2. **User B** has a "Focus Block" on Wednesday 2:00-3:00 PM → marks as **SWAPPABLE**
3. **User A** browses the marketplace, finds User B's slot, and requests a swap
4. **User B** receives a notification and **ACCEPTS** the swap
5. ✅ Calendars update automatically: User A gets Wednesday slot, User B gets Tuesday slot

---

## ✨ Features

### 🔐 Authentication
- ✅ Secure user registration and login
- ✅ JWT (JSON Web Token) based authentication
- ✅ Password hashing using Argon2
- ✅ Protected routes and API endpoints

### 📅 Calendar Management
- ✅ Create, read, update, and delete events
- ✅ Set event time ranges (start/end time)
- ✅ Mark events as BUSY, SWAPPABLE, or SWAP_PENDING
- ✅ Real-time calendar state updates

### 🔄 Swap Functionality
- ✅ Browse marketplace of swappable slots from other users
- ✅ Request swaps by offering your own swappable slot
- ✅ Accept or reject incoming swap requests
- ✅ Automatic calendar updates upon swap acceptance
- ✅ Prevents double-swapping with SWAP_PENDING status

### 🎨 User Interface
- ✅ Modern, responsive design with glass morphism effects
- ✅ Animated gradient backgrounds
- ✅ Mobile-first approach
- ✅ Smooth transitions and hover effects
- ✅ Intuitive navigation and user feedback

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Programming Language |
| **FastAPI** | 0.104+ | Modern web framework for building APIs |
| **SQLAlchemy** | 2.0+ | SQL toolkit and ORM |
| **PostgreSQL** | 15+ | Relational database |
| **Alembic** | 1.12+ | Database migrations |
| **Pydantic** | 2.5+ | Data validation using Python type hints |
| **python-jose** | 3.3+ | JWT token creation and verification |
| **Argon2** | 23.1+ | Password hashing |
| **Uvicorn** | 0.24+ | ASGI server |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2+ | UI library |
| **React Router** | 6.20+ | Client-side routing |
| **Axios** | 1.6+ | HTTP client |
| **date-fns** | 3.0+ | Date formatting utilities |
| **CSS3** | - | Styling with modern features |

### Development Tools
- **pytest** - Backend testing
- **Git** - Version control
- **Docker** - Containerization (optional)

---

## 🏗️ Architecture & Design Choices

### Backend Architecture

#### 1. **FastAPI Framework**
**Why FastAPI?**
- Automatic API documentation (Swagger/OpenAPI)
- High performance (comparable to NodeJS)
- Built-in data validation with Pydantic
- Async support for scalability
- Type hints for better code quality

#### 2. **Database Design**
```
┌─────────────┐         ┌─────────────┐         ┌─────────────────┐
│    Users    │         │   Events    │         │  SwapRequests   │
├─────────────┤         ├─────────────┤         ├─────────────────┤
│ id (PK)     │────┐    │ id (PK)     │    ┌───│ id (PK)         │
│ name        │    └───→│ user_id(FK) │    │   │ requester_id(FK)│
│ email       │         │ title       │←───┤   │ receiver_id(FK) │
│ password    │         │ start_time  │    │   │ requester_slot  │
│ created_at  │         │ end_time    │    └───│ requested_slot  │
└─────────────┘         │ status      │        │ status          │
                        │ created_at  │        │ created_at      │
                        └─────────────┘        └─────────────────┘
```

**Design Decisions:**
- **Normalized schema** to avoid data redundancy
- **Cascade deletes** to maintain referential integrity
- **Enum types** (EventStatus, SwapRequestStatus) for data consistency
- **Timestamps** for audit trails

#### 3. **Security Measures**
- **Argon2 password hashing** (more secure than bcrypt)
- **JWT tokens** with expiration (7 days default)
- **HTTPBearer authentication** for protected routes
- **SQL injection prevention** via SQLAlchemy ORM
- **CORS configuration** to control API access

#### 4. **API Design**
- **RESTful principles** for predictable endpoints
- **Proper HTTP status codes** (201 for creation, 404 for not found, etc.)
- **Structured error responses** with detail messages
- **Request/Response validation** using Pydantic schemas

### Frontend Architecture

#### 1. **Component Structure**
```
src/
├── components/       # Reusable UI components
├── pages/           # Route-based page components
├── context/         # React Context for state management
├── services/        # API integration layer
└── App.js          # Main application component
```

#### 2. **State Management**
- **React Context API** for authentication state
- **Local component state** for UI interactions
- **Axios interceptors** for automatic token attachment

#### 3. **Styling Approach**
- **Pure CSS** with CSS3 features (no framework overhead)
- **CSS Variables** for consistent theming
- **Glass morphism** and gradient effects for modern UI
- **Mobile-first responsive design**

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 16 or higher** - [Download](https://nodejs.org/)
- **PostgreSQL 15 or higher** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

### Verify Installation
```bash
python --version  # Should be 3.11+
node --version    # Should be 16+
psql --version    # Should be 15+
git --version
```

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/slotswapper.git
cd slotswapper
```

### Step 2: Database Setup

#### Option A: Using PostgreSQL

1. **Start PostgreSQL** (if not already running)

2. **Create Database**
```bash
# Open PostgreSQL CLI
psql -U postgres

# Create database
CREATE DATABASE slotswapper;

# Exit
\q
```

#### Option B: Using Docker (Recommended)

```bash
docker run --name slotswapper-db \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=slotswapper \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### Step 3: Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file**
```bash
# Create .env file in backend/ directory
# Copy from .env.example and update values
```

**`backend/.env`**
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/slotswapper
SECRET_KEY=your-super-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
ENVIRONMENT=development
DEBUG=True
```

> ⚠️ **Important:** Replace `your_password` and `SECRET_KEY` with your actual values

5. **Run database migrations** (optional - tables auto-create on startup)
```bash
# If using Alembic
alembic upgrade head
```

6. **Start the backend server**
```bash
uvicorn app.main:app --reload
```

✅ Backend should now be running at **http://localhost:8000**

### Step 4: Frontend Setup

1. **Open a new terminal** and navigate to frontend directory
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

✅ Frontend should now be running at **http://localhost:3000**

### Step 5: Verify Installation

1. **Backend API Documentation**: http://localhost:8000/api/docs
2. **Frontend Application**: http://localhost:3000
3. **Health Check**: http://localhost:8000/health

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/signup` | Register a new user | ❌ |
| `POST` | `/auth/login` | Login and receive JWT token | ❌ |
| `GET` | `/auth/me` | Get current user info | ✅ |

#### POST /auth/signup
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-01T12:00:00"
  }
}
```

#### POST /auth/login
**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-01T12:00:00"
  }
}
```

---

### Event Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/events` | Get all events for current user | ✅ |
| `GET` | `/events/{id}` | Get specific event by ID | ✅ |
| `POST` | `/events` | Create a new event | ✅ |
| `PUT` | `/events/{id}` | Update an event | ✅ |
| `DELETE` | `/events/{id}` | Delete an event | ✅ |

#### POST /events
**Request Body:**
```json
{
  "title": "Team Meeting",
  "start_time": "2025-01-15T10:00:00",
  "end_time": "2025-01-15T11:00:00"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Team Meeting",
  "start_time": "2025-01-15T10:00:00",
  "end_time": "2025-01-15T11:00:00",
  "status": "BUSY",
  "user_id": 1,
  "created_at": "2025-01-01T12:00:00",
  "updated_at": "2025-01-01T12:00:00"
}
```

#### PUT /events/{id}
**Request Body:**
```json
{
  "status": "SWAPPABLE"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Team Meeting",
  "start_time": "2025-01-15T10:00:00",
  "end_time": "2025-01-15T11:00:00",
  "status": "SWAPPABLE",
  "user_id": 1,
  "created_at": "2025-01-01T12:00:00",
  "updated_at": "2025-01-01T12:30:00"
}
```

---

### Swap Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/swappable-slots` | Get all swappable slots from other users | ✅ |
| `POST` | `/swap-request` | Create a swap request | ✅ |
| `POST` | `/swap-response/{id}` | Accept or reject a swap request | ✅ |
| `GET` | `/swap-requests/incoming` | Get incoming swap requests | ✅ |
| `GET` | `/swap-requests/outgoing` | Get outgoing swap requests | ✅ |
| `DELETE` | `/swap-request/{id}` | Cancel a pending swap request | ✅ |

#### GET /swappable-slots
**Response (200):**
```json
[
  {
    "id": 2,
    "title": "Focus Block",
    "start_time": "2025-01-16T14:00:00",
    "end_time": "2025-01-16T15:00:00",
    "status": "SWAPPABLE",
    "user_id": 2,
    "created_at": "2025-01-01T13:00:00",
    "updated_at": "2025-01-01T13:00:00"
  }
]
```

#### POST /swap-request
**Request Body:**
```json
{
  "my_slot_id": 1,
  "their_slot_id": 2
}
```

**Response (201):**
```json
{
  "id": 1,
  "requester_slot_id": 1,
  "requested_slot_id": 2,
  "requester_id": 1,
  "receiver_id": 2,
  "status": "PENDING",
  "created_at": "2025-01-01T14:00:00",
  "updated_at": "2025-01-01T14:00:00"
}
```

#### POST /swap-response/{id}
**Request Body:**
```json
{
  "accept": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "requester_slot_id": 1,
  "requested_slot_id": 2,
  "requester_id": 1,
  "receiver_id": 2,
  "status": "ACCEPTED",
  "created_at": "2025-01-01T14:00:00",
  "updated_at": "2025-01-01T14:30:00"
}
```

---

### Authentication Header

All protected endpoints require a JWT token in the Authorization header:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example API Calls

#### Using cURL
```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Get Events (with token)
curl -X GET http://localhost:8000/api/events \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Using Python (requests)
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})
token = response.json()['access_token']

# Get Events
headers = {'Authorization': f'Bearer {token}'}
events = requests.get('http://localhost:8000/api/events', headers=headers)
print(events.json())
```

### Postman Collection

Import this collection into Postman for easy API testing:

📥 **[Download Postman Collection](./SlotSwapper.postman_collection.json)**

Or access interactive API documentation at: **http://localhost:8000/api/docs**

---

## 📁 Project Structure

```
slotswapper/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── routes/
│   │   │   │   ├── auth.py    # Authentication endpoints
│   │   │   │   ├── events.py  # Event management endpoints
│   │   │   │   └── swaps.py   # Swap logic endpoints
│   │   │   └── deps.py        # Dependencies (auth, DB)
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Configuration settings
│   │   │   └── security.py    # Security utilities (JWT, hashing)
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py        # User model
│   │   │   ├── event.py       # Event model
│   │   │   └── swap_request.py # SwapRequest model
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py        # User schemas
│   │   │   ├── event.py       # Event schemas
│   │   │   ├── swap_request.py # Swap request schemas
│   │   │   └── token.py       # Token schemas
│   │   ├── database.py        # Database connection
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Backend tests
│   │   ├── test_auth.py
│   │   ├── test_events.py
│   │   └── conftest.py
│   ├── .env                   # Environment variables (gitignored)
│   ├── .env.example           # Example environment file
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
│
├── frontend/                   # React Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── Navbar.js
│   │   │   ├── ProtectedRoute.js
│   │   │   ├── EventCard.js
│   │   │   └── Modal.js
│   │   ├── context/           # React Context
│   │   │   └── AuthContext.js
│   │   ├── pages/             # Page components
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Marketplace.js
│   │   │   └── Requests.js
│   │   ├── services/          # API integration
│   │   │   └── api.js
│   │   ├── App.js             # Main component
│   │   ├── App.css            # Global styles
│   │   └── index.js           # Entry point
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend documentation
│
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Docker compose configuration
├── README.md                  # Main documentation (this file)
└── LICENSE                    # License file
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/

# Test complete swap flow
python test_complete_flow.py
```

### Test Coverage

Current test coverage includes:
- ✅ User authentication (signup, login)
- ✅ Event CRUD operations
- ✅ Swap request creation
- ✅ Swap acceptance/rejection logic
- ✅ Calendar updates after swap

### Manual Testing

1. **Start both servers** (backend and frontend)
2. **Sign up** two different users in different browser windows/incognito
3. **Create events** for both users
4. **Mark events as swappable**
5. **Request a swap** from one user
6. **Accept/reject** from the other user
7. **Verify** calendar updates

---

## 🤔 Assumptions & Challenges

### Assumptions Made

1. **Single Swap Per Slot**
   - A slot can only participate in one swap request at a time
   - Implemented via `SWAP_PENDING` status

2. **Event Ownership Transfer**
   - When a swap is accepted, the entire event (with its time and title) is transferred
   - Alternative could be: only swap time slots, not event details

3. **Time Zone Handling**
   - All times are stored in UTC
   - Frontend displays in user's local timezone
   - Assumption: Users are aware of timezone differences

4. **Authentication Token Expiry**
   - Default: 7 days (10,080 minutes)
   - Users must re-login after expiry
   - No refresh token mechanism implemented

5. **Email Uniqueness**
   - Each email can only have one account
   - No email verification implemented

6. **Event Validation**
   - End time must be after start time
   - No validation for overlapping events in user's calendar

7. **Swap Cancellation**
   - Only the requester can cancel a pending swap
   - No timeout mechanism for pending requests

### Challenges Faced & Solutions

#### 1. **Password Hashing Compatibility**
**Challenge:** Initial bcrypt/passlib version mismatch causing errors
```
ValueError: password cannot be longer than 72 bytes
```

**Solution:** 
- Switched from bcrypt to Argon2 (more modern, no compatibility issues)
- Updated `app/core/security.py` to use `argon2-cffi`

#### 2. **Database URL Encoding**
**Challenge:** PostgreSQL password with special characters (`@`) breaking connection
```
Invalid database URL
```

**Solution:**
- URL-encode special characters (`@` → `%40`)
- Document in setup instructions

#### 3. **CORS Configuration**
**Challenge:** Frontend unable to call backend API (CORS errors)

**Solution:**
- Configured FastAPI CORS middleware
- Added `http://localhost:3000` to allowed origins
- Used environment variable for flexibility

#### 4. **State Synchronization**
**Challenge:** Calendar not updating after swap without page refresh

**Solution:**
- Implemented fetch after swap acceptance/rejection
- Used React state updates to trigger re-renders
- Could enhance with WebSockets for real-time updates

#### 5. **Atomic Swap Transaction**
**Challenge:** Ensuring both calendar updates happen atomically

**Solution:**
- Used SQLAlchemy session transaction
- All updates (swap status, event owners) in single commit
- Rollback on any error to maintain consistency

#### 6. **Responsive Design**
**Challenge:** Complex layout breaking on mobile devices

**Solution:**
- Mobile-first CSS approach
- Flexbox/Grid for responsive layouts
- Media queries for different breakpoints

#### 7. **Date/Time Handling**
**Challenge:** Date formatting inconsistencies

**Solution:**
- Used `date-fns` library for consistent formatting
- ISO 8601 format for API communication
- `datetime-local` input for user-friendly date selection

---

## 🎨 Screenshots

### Authentication Pages
![Login Page](./screenshots/login.png)
![Signup Page](./screenshots/signup.png)

### Dashboard
![Dashboard](./screenshots/dashboard.png)

### Marketplace
![Marketplace](./screenshots/marketplace.png)

### Swap Requests
![Requests](./screenshots/requests.png)


---

## 🚀 Future Enhancements

### Planned Features

1. **Real-time Notifications**
   - WebSocket integration for instant swap notifications
   - Browser push notifications

2. **Email Notifications**
   - Send email when swap request is received
   - Confirmation emails for accepted swaps

3. **Advanced Filtering**
   - Filter marketplace by date range
   - Search by event title
   - Category/tags for events

4. **Calendar View**
   - Full calendar grid view (using libraries like FullCalendar)
   - Week/Month/Day views
   - Drag-and-drop event creation

5. **User Profiles**
   - Profile pictures
   - User ratings/reviews
   - Swap history

6. **Enhanced Security**
   - Two-factor authentication
   - Email verification
   - Refresh tokens
   - Rate limiting

7. **Analytics Dashboard**
   - Swap statistics
   - Most popular time slots
   - User engagement metrics

8. **Mobile App**
   - React Native mobile application
   - Native push notifications

9. **Timezone Support**
   - Explicit timezone selection
   - Automatic conversion display

10. **Batch Operations**
    - Create multiple events at once
    - Recurring events
    - Bulk status updates

---

## 🐳 Docker Deployment (Optional)

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**`docker-compose.yml`**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: slotswapper
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/slotswapper
      SECRET_KEY: your-secret-key
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Backend:** Follow PEP 8 guidelines
- **Frontend:** Use ESLint with Airbnb style guide
- **Commits:** Use conventional commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Vansh Vagadia** - [GitHub](https://github.com/Vansh160205)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- React team for excellent documentation
- PostgreSQL for robust database
- All open-source contributors

---

## 📞 Support

For support, email vanshvagadia1602@gmail.com or open an issue in the GitHub repository.

---

<div align="center">

**Built with ❤️ using FastAPI and React**

[⬆ Back to Top](#-slotswapper---peer-to-peer-time-slot-scheduling-application)

</div>
```
