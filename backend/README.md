# SlotSwapper Backend API

A peer-to-peer time-slot scheduling application built with FastAPI.

## Features

- 🔐 JWT-based authentication
- 📅 Calendar event management
- 🔄 Peer-to-peer slot swapping
- 🔔 Swap request management
- ✅ Comprehensive test coverage
- 🐳 Docker support

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd backend

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/api/docs
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Create database
createdb slotswapper

# Run migrations (if using alembic)
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/me` | Get current user | Yes |

### Events

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/events` | Get user's events | Yes |
| GET | `/api/events/{id}` | Get specific event | Yes |
| POST | `/api/events` | Create new event | Yes |
| PUT | `/api/events/{id}` | Update event | Yes |
| DELETE | `/api/events/{id}` | Delete event | Yes |

### Swaps

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/swappable-slots` | Get all swappable slots | Yes |
| POST | `/api/swap-request` | Create swap request | Yes |
| POST | `/api/swap-response/{id}` | Accept/reject swap | Yes |
| GET | `/api/swap-requests/incoming` | Get incoming requests | Yes |
| GET | `/api/swap-requests/outgoing` | Get outgoing requests | Yes |
| DELETE | `/api/swap-request/{id}` | Cancel swap request | Yes |

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## Database Schema

### Users Table
- id (PK)
- name
- email (unique)
- hashed_password
- created_at
- updated_at

### Events Table
- id (PK)
- title
- start_time
- end_time
- status (BUSY, SWAPPABLE, SWAP_PENDING)
- user_id (FK)
- created_at
- updated_at

### Swap Requests Table
- id (PK)
- requester_slot_id (FK)
- requested_slot_id (FK)
- requester_id (FK)
- receiver_id (FK)
- status (PENDING, ACCEPTED, REJECTED)
- created_at
- updated_at

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Project Structure

```
app/
├── api/
│   ├── deps.py           # Dependencies
│   └── routes/           # API routes
│       ├── auth.py       # Authentication
│       ├── events.py     # Events management
│       └── swaps.py      # Swap operations
├── core/
│   ├── config.py         # Configuration
│   └── security.py       # Security utilities
├── models/               # SQLAlchemy models
├── schemas/              # Pydantic schemas
└── main.py              # Application entry point
```

## Development

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## Deployment

### Docker Production Build

```bash
docker build -t slotswapper-backend .
docker run -p 8000:8000 --env-file .env slotswapper-backend
```

### Deploy to Cloud

See deployment guides for:
- [Render](https://render.com)
- [Railway](https://railway.app)
- [Heroku](https://heroku.com)
- [AWS ECS](https://aws.amazon.com/ecs/)

## License

MIT
```

---

## To Run the Backend:

```bash
# 1. Create .env file
cp .env.example .env

# 2. Using Docker (easiest)
docker-compose up -d

# 3. Or manually
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Run tests
pytest
```

This is a complete, production-ready backend with:
- ✅ All required features
- ✅ Proper error handling
- ✅ Input validation
- ✅ Security best practices
- ✅ Comprehensive tests
- ✅ Docker support
- ✅ API documentation
- ✅ Type hints
- ✅ Clean architecture