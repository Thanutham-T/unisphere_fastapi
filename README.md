# Unisphere FastA### 3. Install Dependencies

```bash
poetry install
```

### 4. Setup PostgreSQL Database

Install PostgreSQL on your system:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### 5. Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE USER unisphere_user WITH PASSWORD 'password123';
CREATE DATABASE unisphere_db OWNER unisphere_user;
CREATE DATABASE unisphere_test_db OWNER unisphere_user;
GRANT ALL PRIVILEGES ON DATABASE unisphere_db TO unisphere_user;
GRANT ALL PRIVILEGES ON DATABASE unisphere_test_db TO unisphere_user;
\q
```

### 6. Configure Environment Variables

Copy the `.env` file and update the database credentials if needed:

```bash
cp .env .env.local
```

Edit `.env` file with your database configuration:

```env
DATABASE_URL=postgresql://unisphere_user:password123@localhost:5432/unisphere_db
SECRET_KEY=your-super-secret-key-change-this-in-production
```his project is a backend that provides API for campus life hub mobile app using FastAPI.

## Prerequisites

- Python 3.12+
- Poetry (Python dependency management)

## Setup Instructions

### 1. Install Poetry (if not already installed)

```bash
pip install poetry
```

### 2. Install Dependencies

```bash
poetry install
```

## Running the Application

### Development Mode

Make sure PostgreSQL is running, then start the development server:

```bash
./scripts/run-api-dev
```

Or manually:

```bash
poetry run fastapi dev app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
poetry run fastapi run app/main.py
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user profile

### Courses
- `GET /api/v1/courses/` - Get user's courses
- `POST /api/v1/courses/` - Create new course
- `PUT /api/v1/courses/{course_id}` - Update course
- `DELETE /api/v1/courses/{course_id}` - Delete course

### Events
- `GET /api/v1/events/` - Get campus events
- `POST /api/v1/events/{event_id}/register` - Register for event
- `DELETE /api/v1/events/{event_id}/register` - Unregister from event

### Study Groups
- `GET /api/v1/study-groups/` - Get study groups
- `POST /api/v1/study-groups/` - Create study group
- `POST /api/v1/study-groups/{group_id}/join` - Join study group
- `DELETE /api/v1/study-groups/{group_id}/leave` - Leave study group

### Announcements
- `GET /api/v1/announcements/` - Get announcements
- `POST /api/v1/announcements/{announcement_id}/bookmark` - Bookmark announcement

### Locations
- `GET /api/v1/locations/` - Get campus locations
- `GET /api/v1/locations/search` - Search locations

## Flutter Integration

### CORS Configuration

The API is configured to allow requests from Flutter development servers:
- `http://localhost:8080` (Flutter web dev)
- `http://localhost:8081` (Flutter web dev alternative)

### API Base URL

In your Flutter app, use these base URLs:

**Development:**
```dart
const String apiBaseUrl = 'http://localhost:8000/api/v1';
```

**Production:**
```dart
const String apiBaseUrl = 'https://your-domain.com/api/v1';
```

### Example Flutter HTTP Client

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  // Login example
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'email': email, 'password': password}),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to login');
    }
  }
  
  // Get courses example
  static Future<List<dynamic>> getCourses(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/courses/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load courses');
    }
  }
}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
unisphere_fastapi/
├── app/
│   ├── __init__.py                # App entry point
│   ├── main.py                    # FastAPI application
│   ├── core/                      # Core dependencies
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   └── dependencies.py        # Dependency injection
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user_model.py          # User, authentication models
│   │   ├── course_model.py        # Course, attendance models
│   │   ├── event_model.py         # Event, study group models
│   │   └── announcement_model.py  # Announcement, location models
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py         # User request/response schemas
│   │   ├── course_schema.py       # Course request/response schemas
│   │   └── ...                    # Other schemas
│   ├── routes/                    # API routes
│   │   ├── __init__.py
│   │   └── v1/                    # API version 1
│   │       ├── __init__.py
│   │       ├── auth.py            # Authentication routes
│   │       ├── courses.py         # Course management routes
│   │       ├── events.py          # Event routes
│   │       ├── study_groups.py    # Study group routes
│   │       ├── announcements.py   # Announcement routes
│   │       └── locations.py       # Location/map routes
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── ...
│   ├── repositories/              # Database queries
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   ├── course_repo.py
│   │   └── ...
│   ├── middlewares/               # Custom middlewares
│   │   └── __init__.py
│   ├── utils/                     # Utility functions
│   │   └── __init__.py
│   └── tests/                     # Unit and integration tests
│       └── __init__.py
├── scripts/                       # Shell scripts
│   └── run-api-dev               # Development server script
├── uploads/                       # File uploads directory
├── .env                          # Environment variables
├── .gitignore                    # Git ignore
├── Dockerfile                    # Docker setup
├── pyproject.toml                # Python packages management
├── poetry.lock                   # Poetry lock file
└── README.md                     # This file
```

## Development

### Adding New Dependencies

```bash
poetry add package_name
```

### Adding Development Dependencies

```bash
poetry add --group dev package_name
```