# FastAPI Backend Setup Guide

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 7+ (external infrastructure)
- Docker and Docker Compose (for containerized deployment)

## Local Development Setup

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing (min 32 chars)
- `SECRET_KEY`: Application secret key (min 32 chars)
- `REDIS_URL`: Redis connection URL (external server)

### 3. Database Setup

The application will automatically create tables on first run using SQLAlchemy's `create_all()`.

For production, use Alembic migrations:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### 4. Run Application

#### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Verify Setup

- Health check: `http://localhost:8000/healthz`
- Readiness check: `http://localhost:8000/readyz`
- API docs: `http://localhost:8000/docs` (if DEBUG=True)

## Docker Deployment

### Build and Run

```bash
docker-compose up --build
```

### Environment Variables

Set in `docker-compose.yml` or use `.env` file:

```yaml
environment:
  DATABASE_URL: postgresql://postgres:postgres@postgres:5432/mandatory_todo?sslmode=disable
  JWT_SECRET_KEY: your-secret-key-min-32-chars
  SECRET_KEY: your-secret-key-min-32-chars
  REDIS_URL: redis://your-redis-host:6379/0
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Todos (Authenticated)
- `GET /api/v1/todos` - Get all todos
- `GET /api/v1/todos/{id}` - Get todo by ID
- `POST /api/v1/todos` - Create todo
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo

### Health Checks
- `GET /healthz` - Basic health check
- `GET /readyz` - Readiness check (checks database)

## Project Structure

```
api/
├── app/
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database setup
│   │   ├── security.py         # Security utilities
│   │   ├── cache.py            # Redis cache
│   │   ├── validation.py       # Input validation
│   │   └── exceptions.py       # Custom exceptions
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic
│   ├── routers/                # API routes
│   ├── middleware/             # Custom middleware
│   └── dependencies.py         # FastAPI dependencies
├── alembic/                    # Database migrations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
└── .env.example               # Environment template
```

## Database Migrations

### Create Migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

### Key Settings

- `DEBUG`: Enable debug mode (default: False)
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: JWT signing key (required, min 32 chars)
- `REDIS_URL`: Redis connection URL
- `REDIS_ENABLED`: Enable Redis caching (default: True)
- `CORS_ORIGINS`: Allowed CORS origins (JSON array)
- `RATE_LIMIT_ENABLED`: Enable rate limiting (default: True)

## Security

### Password Requirements

- Minimum 12 characters
- Requires uppercase letter
- Requires lowercase letter
- Requires number
- Requires special character

### Rate Limiting

- Login: 5 attempts per 15 minutes
- Registration: 3 attempts per hour
- API: 100 requests per minute per user

### Security Headers

All responses include security headers:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
- Content-Security-Policy
- Referrer-Policy

## Troubleshooting

### Database Connection Issues

1. Verify `DATABASE_URL` is correct
2. Check PostgreSQL is running
3. Verify network connectivity

### Redis Connection Issues

1. Verify `REDIS_URL` is correct
2. Check Redis is accessible
3. Application will work without Redis (caching disabled)

### Port Already in Use

Change port in `.env`:
```
PORT=8001
```

### Import Errors

Ensure you're in the correct directory and dependencies are installed:
```bash
pip install -r requirements.txt
```

## Testing

### Run Tests

```bash
pytest
```

### Test Coverage

```bash
pytest --cov=app
```

## Production Deployment

1. Set `DEBUG=False` in production
2. Use strong secrets (min 32 characters)
3. Enable HTTPS
4. Configure proper CORS origins
5. Set up monitoring and logging
6. Use secret management service
7. Regular security audits

## Support

For issues or questions, refer to:
- Architecture documentation: `internal/docs/ARCHITECTURE.md`
- Security documentation: `internal/docs/SECURITY.md`
- Code flow documentation: `internal/docs/CODE_FLOW.md`
- Dev Bible: `internal/docs/DEV_BIBLE.md`

