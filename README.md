# Todo Application

A production-ready full-stack todo application demonstrating enterprise-grade development practices, security standards, and modern architecture patterns.

## Architecture

- **Backend**: FastAPI (Python 3.11+) REST API with PostgreSQL
- **Frontend**: React 18+ with TypeScript and TailwindCSS
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+ (external infrastructure)
- **Authentication**: JWT-based authentication with secure token management

## Features

- User registration and authentication with strong password requirements
- CRUD operations for todos with proper authorization
- Enterprise-grade security measures (rate limiting, security headers, input validation)
- Redis-based caching for performance optimization
- Async/await architecture for high concurrency
- Comprehensive error handling and validation
- Health check endpoints for monitoring
- Docker containerization for easy deployment

## Project Structure

```
todo/
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── core/           # Core utilities
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── repositories/   # Data access layer
│   │   ├── services/       # Business logic
│   │   ├── routers/        # API routes
│   │   └── middleware/     # Custom middleware
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   └── config/         # Configuration
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml      # Development environment
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- Node.js 20 or later
- PostgreSQL 15 or later
- Redis 7+ (external infrastructure)
- Docker and Docker Compose (optional, for containerized deployment)

### Quick Start with Docker

1. Clone the repository
2. Copy `api/.env.example` to `api/.env` and configure:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY` (minimum 32 characters)
   - `SECRET_KEY` (minimum 32 characters)
   - `REDIS_URL` (your external Redis server)
3. Run with Docker Compose:

   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`  
The frontend will be available at `http://localhost:3001`

### Manual Setup

See `api/README.md` for detailed backend setup instructions.

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT access token

### Todos (Protected - requires Bearer token)

- `GET /api/v1/todos` - Get all todos for authenticated user
- `GET /api/v1/todos/{id}` - Get a specific todo
- `POST /api/v1/todos` - Create a new todo
- `PUT /api/v1/todos/{id}` - Update a todo
- `DELETE /api/v1/todos/{id}` - Delete a todo

### Health Checks

- `GET /healthz` - Health check (process alive)
- `GET /readyz` - Readiness check (dependencies ready)

## Security Features

- **Password Requirements**: Minimum 12 characters with complexity requirements
- **Password Hashing**: Bcrypt with 12 rounds
- **JWT Authentication**: Secure token-based authentication with expiration
- **Rate Limiting**: Redis-based distributed rate limiting
- **Security Headers**: Comprehensive security headers on all responses
- **Input Validation**: Pydantic validation with custom validators
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: React escaping and Content Security Policy
- **CORS**: Properly configured for cross-origin requests

## Development

### Backend Development

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
cd api
alembic upgrade head
```

## Environment Variables

### Backend

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing (minimum 32 characters)
- `SECRET_KEY` - Application secret key (minimum 32 characters)
- `REDIS_URL` - Redis connection URL (external infrastructure)
- `REDIS_ENABLED` - Enable Redis caching (default: true)
- `DEBUG` - Enable debug mode (default: false)

### Frontend

- `VITE_API_BASE_URL` - Backend API base URL (defaults to `http://localhost:8000`)

## Production Considerations

1. **Secrets**: Use strong, randomly generated secrets (minimum 32 characters)
2. **HTTPS**: Always use HTTPS in production
3. **Database**: Use SSL connections in production
4. **CORS**: Restrict CORS origins to your frontend domain
5. **Rate Limiting**: Already implemented with Redis
6. **Monitoring**: Set up structured logging and monitoring
7. **Error Tracking**: Consider adding error tracking service
8. **Backup**: Implement database backup strategy

## License

This project demonstrates professional development practices and is suitable for portfolio purposes.
