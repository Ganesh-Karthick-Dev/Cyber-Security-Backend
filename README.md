# FastAPI Cyber Security Backend

A comprehensive, production-ready FastAPI backend server specifically designed for cyber security applications. This project is structured for scalability, maintainability, and follows best practices for Python web development.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- PostgreSQL database (optional - can use SQLite for development)
- Redis (optional - for caching and rate limiting)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd "D:\Cyber Security\Cyber-Security-Backend"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env file with your configuration
   ```

5. **Run the development server:**
   ```bash
   # Method 1: Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Method 2: Using Python
   python -m app.main
   ```

6. **Access the application:**
   - API: http://localhost:8000
   - Interactive Docs (Swagger): http://localhost:8000/docs
   - Alternative Docs (ReDoc): http://localhost:8000/redoc

## 📁 Project Structure

```
Cyber-Security-Backend/
├── app/
│   ├── api/                    # API routes
│   │   ├── endpoints/          # Individual endpoint files
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── users.py        # User management endpoints
│   │   │   └── security_events.py # Security events endpoints
│   │   └── api.py              # Main API router
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Application settings
│   │   └── security.py         # Security utilities (JWT, passwords)
│   ├── db/                     # Database configuration
│   │   └── database.py         # Database connection and session
│   ├── models/                 # Database models (SQLAlchemy)
│   │   ├── user.py             # User model
│   │   └── security_event.py   # Security event model
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── auth.py             # Authentication schemas
│   │   └── user.py             # User schemas
│   ├── services/               # Business logic
│   │   └── auth_service.py     # Authentication service
│   ├── utils/                  # Utility functions
│   │   ├── responses.py        # Standardized API responses
│   │   └── exceptions.py       # Custom exceptions
│   ├── middleware/             # Custom middleware
│   │   └── rate_limiting.py    # Rate limiting middleware
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables example
└── README.md                  # This file
```

## 🔑 Key Features

### 1. Authentication & Security
- **JWT Token Authentication** - Secure token-based auth
- **Password Hashing** - Using bcrypt for secure password storage
- **Rate Limiting** - Prevents API abuse and DDoS attacks
- **CORS Configuration** - Secure cross-origin resource sharing

### 2. Database Integration
- **SQLAlchemy ORM** - Object-relational mapping for database operations
- **Alembic Migrations** - Database schema versioning
- **PostgreSQL Support** - Production-ready database
- **Connection Pooling** - Efficient database connections

### 3. API Design
- **RESTful Endpoints** - Standard HTTP methods and status codes
- **Automatic Documentation** - Swagger/OpenAPI docs generation
- **Request Validation** - Pydantic schemas for data validation
- **Standardized Responses** - Consistent API response format

### 4. Cyber Security Specific
- **Security Events Tracking** - Monitor and log security incidents
- **Threat Dashboard** - Real-time security metrics
- **IP Monitoring** - Track suspicious IP addresses
- **File Hash Analysis** - Malware detection capabilities

## 🛠 API Endpoints

### Authentication
```
POST /api/v1/auth/login         # User login
POST /api/v1/auth/register      # User registration
GET  /api/v1/auth/me           # Get current user info
```

### Users
```
GET    /api/v1/users           # Get all users (paginated)
GET    /api/v1/users/{id}      # Get user by ID
POST   /api/v1/users           # Create new user
PUT    /api/v1/users/{id}      # Update user
DELETE /api/v1/users/{id}      # Delete user
```

### Security Events
```
GET /api/v1/security/events             # Get security events (with filtering)
GET /api/v1/security/events/{id}        # Get specific security event
GET /api/v1/security/dashboard          # Get security dashboard metrics
```

## 🧪 Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

### 2. User Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secret"
```

### 3. Access Protected Endpoint
```bash
# Replace YOUR_TOKEN with the token from login response
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Get Security Events
```bash
curl -X GET "http://localhost:8000/api/v1/security/events" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Configuration

### Environment Variables (.env file)
```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/cybersecurity_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
ENVIRONMENT=development

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 📊 Database Models

### User Model
- `id` - Primary key
- `username` - Unique username
- `email` - User email address
- `hashed_password` - Securely hashed password
- `role` - User role (user/admin/analyst)
- `is_active` - Account status
- `created_at`, `updated_at` - Timestamps

### Security Event Model
- `id` - Primary key
- `event_type` - Type of security event
- `severity` - Event severity (low/medium/high/critical)
- `source_ip` - Source IP address
- `description` - Event description
- `metadata` - Additional event data (JSON)
- `status` - Event status (active/blocked/resolved)
- `created_at`, `updated_at` - Timestamps

## 🚀 Deployment

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Using Gunicorn with Uvicorn workers
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 For Node.js/Express Developers

If you're coming from Node.js/Express, here are the key comparisons:

### Express.js vs FastAPI
| Express.js | FastAPI |
|------------|---------|
| `app.get()` | `@router.get()` |
| `app.post()` | `@router.post()` |
| `req.params` | Path parameters in function |
| `req.query` | Query parameters with `Query()` |
| `req.body` | Pydantic models |
| `res.json()` | `return APIResponse.success()` |
| Middleware functions | Dependency injection with `Depends()` |
| `express.Router()` | `APIRouter()` |

### Key Differences
1. **Type Safety**: FastAPI uses Python type hints for automatic validation
2. **Documentation**: Automatic OpenAPI/Swagger docs generation
3. **Async Support**: Native async/await support (like modern Node.js)
4. **Dependency Injection**: Built-in DI system instead of middleware chains
5. **Pydantic Models**: Similar to Joi validation but with Python classes

## 📚 Learn More

### FastAPI Concepts
1. **Path Operations** - Similar to Express routes
2. **Dependencies** - Like Express middleware but more powerful
3. **Pydantic Models** - Data validation and serialization
4. **Background Tasks** - For async operations
5. **WebSocket Support** - Real-time communication

### Next Steps
1. Add database migrations with Alembic
2. Implement user registration endpoint
3. Add file upload capabilities for malware analysis
4. Create real-time notifications with WebSockets
5. Add comprehensive logging and monitoring
6. Implement email notifications
7. Add API versioning
8. Create admin dashboard

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use**: Change port in command or kill existing process
2. **Database connection error**: Check DATABASE_URL in .env file
3. **Import errors**: Ensure virtual environment is activated
4. **Permission errors**: Check file permissions and user access

### Getting Help
- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Review the logs for error details
- Use the interactive docs at `/docs` for API testing

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.