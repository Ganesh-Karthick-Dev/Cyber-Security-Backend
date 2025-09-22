# Getting Started Guide - FastAPI for Node.js Developers

This guide will help you understand FastAPI concepts by comparing them to Node.js/Express.js patterns you already know.

## 🎯 Quick Setup (5 Minutes)

### Step 1: Install Python and Setup Project
```bash
# Navigate to your project folder
cd "D:\Cyber Security\Cyber-Security-Backend"

# Create virtual environment (like node_modules but for Python)
python -m venv venv

# Activate virtual environment (like nvm use)
# On Windows:
venv\Scripts\activate

# Install dependencies (like npm install)
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy environment file (like .env in Node.js)
copy .env.example .env

# Edit .env file with your settings (optional for now)
```

### Step 3: Run the Server
```bash
# Method 1: Simple way
python run.py

# Method 2: Using uvicorn (like nodemon)
uvicorn app.main:app --reload

# Server will start at: http://localhost:8000
```

### Step 4: Test the API
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Health Check**: http://localhost:8000/health
- **Login Test**: Use the docs UI or curl

## 🔄 Node.js vs FastAPI Comparison

### 1. Project Structure
```
Node.js/Express          FastAPI
├── routes/              ├── app/api/endpoints/
├── controllers/         ├── app/services/
├── models/              ├── app/models/
├── middleware/          ├── app/middleware/
├── utils/               ├── app/utils/
├── config/              ├── app/core/
└── app.js               └── app/main.py
```

### 2. Creating Routes
```javascript
// Express.js
const express = require('express');
const router = express.Router();

router.get('/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json({ success: true, data: users });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});
```

```python
# FastAPI
from fastapi import APIRouter
from app.utils.responses import APIResponse

router = APIRouter()

@router.get("/users")
async def get_users():
    try:
        # Your logic here
        users = []  # Fetch from database
        return APIResponse.success(data=users)
    except Exception as error:
        return APIResponse.error(message=str(error))
```

### 3. Request/Response Handling
```javascript
// Express.js
router.post('/users', async (req, res) => {
  const { username, email } = req.body;
  const userId = req.params.id;
  const page = req.query.page || 1;
  
  res.json({ message: 'User created', data: newUser });
});
```

```python
# FastAPI
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

@router.post("/users/{user_id}")
async def create_user(
    user_id: int,           # Path parameter (req.params)
    user_data: UserCreate,  # Request body (req.body)
    page: int = 1          # Query parameter (req.query)
):
    return APIResponse.success(message="User created", data=new_user)
```

### 4. Middleware
```javascript
// Express.js
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) return res.status(401).json({ message: 'Unauthorized' });
  // Verify token...
  next();
};

router.get('/protected', authMiddleware, (req, res) => {
  res.json({ message: 'Protected data' });
});
```

```python
# FastAPI
from fastapi import Depends
from app.api.endpoints.auth import oauth2_scheme

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token...
    return user

@router.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return APIResponse.success(message="Protected data")
```

### 5. Database Operations
```javascript
// Express.js with Mongoose
const User = require('../models/User');

const createUser = async (userData) => {
  const user = new User(userData);
  await user.save();
  return user;
};
```

```python
# FastAPI with SQLAlchemy
from app.models.user import User
from sqlalchemy.orm import Session

def create_user(db: Session, user_data: UserCreate):
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

## 🛠 Key FastAPI Concepts

### 1. Type Hints (Python's TypeScript)
```python
# Function with type hints
def process_user(user_id: int, name: str) -> dict:
    return {"id": user_id, "name": name}

# FastAPI uses these for automatic validation
@router.get("/users/{user_id}")
async def get_user(user_id: int):  # Automatically validates user_id as integer
    return {"user_id": user_id}
```

### 2. Pydantic Models (Like Joi/Yup validation)
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    age: int = 18  # Default value
    
    class Config:
        # Example values for API docs
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "age": 25
            }
        }
```

### 3. Dependency Injection
```python
# Database dependency (like database connection middleware)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in routes
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### 4. Automatic API Documentation
FastAPI automatically generates:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing Your API

### 1. Using the Built-in Docs
1. Go to http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and execute

### 2. Using curl (like Postman)
```bash
# Health check
curl http://localhost:8000/health

# Login to get token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secret"

# Use token for protected routes
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Using JavaScript (fetch)
```javascript
// Login
const login = async () => {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'username=admin&password=secret'
  });
  const data = await response.json();
  return data.data.access_token;
};

// Get user data
const getMe = async (token) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};
```

## 🔧 Common Development Tasks

### 1. Adding a New Endpoint
1. Create the route in `app/api/endpoints/`
2. Add any required schemas in `app/schemas/`
3. Add business logic in `app/services/`
4. Include the router in `app/api/api.py`

### 2. Adding Database Models
1. Create model in `app/models/`
2. Import in `app/db/database.py`
3. Create migration (if using Alembic)

### 3. Adding Middleware
1. Create middleware in `app/middleware/`
2. Add to main app in `app/main.py`

## 🎓 Learning Path

### Week 1: Basics
- [ ] Understand FastAPI project structure
- [ ] Create simple GET/POST endpoints
- [ ] Work with path and query parameters
- [ ] Use Pydantic models for validation

### Week 2: Intermediate
- [ ] Add database integration
- [ ] Implement authentication
- [ ] Create middleware
- [ ] Handle file uploads

### Week 3: Advanced
- [ ] Add background tasks
- [ ] Implement WebSockets
- [ ] Add testing
- [ ] Deploy to production

## 📚 Helpful Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/14/tutorial/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## 🆘 Common Issues & Solutions

### Issue: Import errors
```bash
# Solution: Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Issue: Port already in use
```bash
# Solution: Kill process or use different port
uvicorn app.main:app --reload --port 8001
```

### Issue: Database connection error
```bash
# Solution: Check .env file or use SQLite for development
DATABASE_URL=sqlite:///./test.db
```

## 🚀 Next Steps

Once you're comfortable with the basics:
1. Add real database (PostgreSQL)
2. Implement user registration
3. Add email verification
4. Create admin dashboard
5. Add file upload for malware analysis
6. Implement real-time notifications
7. Add comprehensive logging

Ready to start coding? Run `python run.py` and visit http://localhost:8000/docs!