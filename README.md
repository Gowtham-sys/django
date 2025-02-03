# Django Authentication API

## Overview
This project is a Django-based authentication system using Django REST Framework (DRF). It implements cookie-based authentication with CSRF protection, API documentation using Swagger, and security measures.

## Features
- User Registration with OTP Verification
- User Login with HTTP-only Cookie Authentication
- Protected User Details Endpoint
- Logout Functionality
- CSRF Protection
- Secure Cookie Handling
- API Documentation with Swagger

## Installation

### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- pip (Python package manager)
- virtualenv (optional but recommended)

### Setup Instructions
1. **Clone the repository**
   ```sh
   git clone <your-repository-url>
   cd <repository-folder>
   ```
2. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin access)**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

| Method | Endpoint              | Description                     |
|--------|-----------------------|---------------------------------|
| POST   | `/api/register/`      | Register a new user (send OTP) |
| POST   | `/api/register/verify/` | Verify user registration (OTP) |
| POST   | `/api/login/`        | Login and set auth cookie      |
| GET    | `/api/me/`           | Get logged-in user details     |
| POST   | `/api/logout/`       | Logout and clear auth cookie   |

## Security Features
- **CSRF Protection:** All requests require a CSRF token.
- **Cookie-based Authentication:** No token headers are used.
- **Secure Cookies:** `HttpOnly` and `Secure` flags are enabled.

## Testing the API
1. **Using Swagger UI**
   - Open [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - Test all API endpoints directly from the UI.

2. **Using Postman**
   - Make sure to include the CSRF token in each request.
   - Cookies should be automatically handled by Postman.

