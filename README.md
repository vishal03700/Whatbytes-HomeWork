# Django Healthcare Backend

A comprehensive healthcare backend system built with Django, Django REST Framework, and JWT authentication.

## Features

- User registration and JWT authentication
- Patient management (CRUD operations)
- Doctor management (CRUD operations)
- Patient-doctor assignment system
- PostgreSQL database support
- Secure API with proper permissions

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Make sure your `.env` file contains:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-postgresql-url
```

### 3. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser
```

### 4. Start the Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/refresh/` | Refresh JWT token | No |

### Patients

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/patients/` | List all patients | Yes |
| POST | `/api/patients/` | Create new patient | Yes |
| GET | `/api/patients/{id}/` | Get patient details | Yes |
| PUT | `/api/patients/{id}/` | Update patient | Yes |
| DELETE | `/api/patients/{id}/` | Delete patient | Yes |
| GET | `/api/patients/{id}/doctors/` | Get patient's doctors | Yes |

### Doctors

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/doctors/` | List all doctors | Yes |
| POST | `/api/doctors/` | Create new doctor | Yes |
| GET | `/api/doctors/{id}/` | Get doctor details | Yes |
| PUT | `/api/doctors/{id}/` | Update doctor | Yes |
| DELETE | `/api/doctors/{id}/` | Delete doctor | Yes |
| GET | `/api/doctors/{id}/patients/` | Get doctor's patients | Yes |

### Patient-Doctor Mappings

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/mappings/` | List all mappings | Yes |
| POST | `/api/mappings/` | Create new mapping | Yes |
| GET | `/api/mappings/{id}/` | Get mapping details | Yes |
| PUT | `/api/mappings/{id}/` | Update mapping | Yes |
| DELETE | `/api/mappings/{id}/` | Delete mapping | Yes |
| GET | `/api/mappings/patient/{patient_id}/` | Get patient's doctors | Yes |
| DELETE | `/api/mappings/remove/` | Remove assignment | Yes |

## Testing with curl

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

Save the `access` token from the response for authenticated requests.

### 3. Create a Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "address": "123 Main St",
    "phone": "+1234567890",
    "email": "john@example.com"
  }'
```

### 4. Create a Doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Dr. Smith",
    "specialty": "Cardiology",
    "license_number": "LIC123456",
    "phone": "+1987654321",
    "email": "dr.smith@hospital.com",
    "years_of_experience": 15
  }'
```

### 5. Assign Doctor to Patient
```bash
curl -X POST http://localhost:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "is_primary": true,
    "notes": "Primary care assignment"
  }'
```

### 6. Get All Patients
```bash
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Issues and Solutions

### 401 Unauthorized Error
- Make sure you're sending the JWT token in the Authorization header
- Format: `Authorization: Bearer YOUR_ACCESS_TOKEN`
- Ensure the token hasn't expired (default: 60 minutes)

### Database Connection Issues
- Verify your DATABASE_URL in the `.env` file
- Make sure PostgreSQL is accessible
- Run migrations: `python manage.py migrate`

### CORS Issues (if using frontend)
- Install `django-cors-headers` if needed
- Configure CORS settings in `settings.py`

## Project Structure

```
healthcare/
├── healthcare/          # Main project directory
│   ├── __init__.py
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── api/                # API application
│   ├── __init__.py
│   ├── models.py       # Database models
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── urls.py         # API URL routes
│   ├── admin.py        # Django admin configuration
│   └── migrations/     # Database migrations
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── manage.py          # Django management script
└── README.md          # This file
```

## Security Features

- JWT token authentication
- User-specific patient access (users can only see their own patients)
- Password validation
- SQL injection protection via Django ORM
- CSRF protection
- Input validation and sanitization

## Next Steps

1. Add comprehensive unit tests
2. Implement API rate limiting
3. Add API documentation with Swagger/OpenAPI
4. Set up logging and monitoring
5. Configure production settings
6. Add email verification for registration