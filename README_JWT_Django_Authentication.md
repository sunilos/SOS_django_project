# JWT Authentication in Django REST Framework

## Simple Explanation for Beginners

JWT means **JSON Web Token**.

Think of JWT like an **entry pass**.

When a student enters a school, the security guard checks the ID card.  
In the same way, when a user calls a protected API, Django checks the JWT token.

If the token is valid, the user is allowed.  
If the token is missing or wrong, the user is blocked.

---

## Why Do We Need JWT?

In a Django REST API project, we may have many APIs like:

- Add student
- Update college
- Delete record
- View user profile
- Search data

These APIs should not be open for everyone.

So we use JWT authentication to make sure that only logged-in users can access protected APIs.

---

## JWT Authentication Flow

```text
1. User sends username and password
        ↓
2. Django checks username and password
        ↓
3. If correct, Django creates JWT tokens
        ↓
4. User receives access token and refresh token
        ↓
5. User sends access token with every API request
        ↓
6. Django checks the token
        ↓
7. If token is valid, API is executed
        ↓
8. If token is invalid, access is denied
```

---

## Tokens in JWT

JWT usually gives two tokens:

### 1. Access Token

This token is used to access protected APIs.

Example:

```text
Authorization: Bearer access_token_here
```

Access token usually has a short life.

### 2. Refresh Token

This token is used to generate a new access token when the access token expires.

---

## Required Package

Install SimpleJWT:

```bash
pip install djangorestframework-simplejwt
```

---

## Step 1: Update `settings.py`

Add JWT authentication in Django REST Framework settings.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

### Meaning

```python
JWTAuthentication
```

This tells Django to check JWT token in every API request.

```python
IsAuthenticated
```

This tells Django that only logged-in users can access APIs.

---

## Step 2: Update `urls.py`

Add token URLs in your main `urls.py` or app `urls.py`.

Example: `ORSAPI/urls.py`

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # your existing API routes
]
```

---

## Step 3: Login API

SimpleJWT already gives a login API:

```text
POST /api/token/
```

### Request Body

```json
{
    "username": "admin",
    "password": "admin123"
}
```

### Response

```json
{
    "refresh": "refresh_token_here",
    "access": "access_token_here"
}
```

---

## Step 4: Call Protected API

After login, send the access token in the request header.

```http
Authorization: Bearer access_token_here
```

Example:

```text
GET /ORSAPI/api/College/
```

Header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## Step 5: Refresh Access Token

When access token expires, call refresh API.

```text
POST /api/token/refresh/
```

### Request Body

```json
{
    "refresh": "refresh_token_here"
}
```

### Response

```json
{
    "access": "new_access_token_here"
}
```

---

## Step 6: Public APIs Without Token

Some APIs should be open without login:

- Login
- Forgot Password
- User Registration

For these APIs, use `AllowAny`.

Example: `UserCtl.py`

```python
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class UserLoginCtl(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Login API"})


class ForgotPasswordCtl(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Forgot Password API"})


class UserRegistrationCtl(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Registration API"})
```

---

## Protected Controller Example

Example: `CollegeCtl.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class CollegeCtl(APIView):

    def get(self, request):
        return Response({
            "message": "College list returned successfully"
        })
```

No need to write authentication code here.

Because authentication is already configured in `settings.py`.

---

## Authentication Workflow from File to File

```text
settings.py
    ↓
JWTAuthentication and IsAuthenticated are configured globally
    ↓
urls.py
    ↓
API URL is mapped to controller
    ↓
Client sends request with Bearer token
    ↓
Django REST Framework receives request
    ↓
JWTAuthentication checks token
    ↓
IsAuthenticated checks user
    ↓
If token is valid, controller method runs
    ↓
If token is invalid, error response is returned
```

---

## Detailed Python File Workflow

```text
1. settings.py
   - Defines JWTAuthentication
   - Defines IsAuthenticated

2. urls.py
   - Defines token generation URL
   - Defines token refresh URL
   - Defines application API URLs

3. UserLoginCtl.py or TokenObtainPairView
   - Takes username and password
   - Generates access and refresh tokens

4. Client Application
   - Stores token
   - Sends token in Authorization header

5. Protected Controller
   - Receives request
   - Runs only if token is valid
```

---

## Important Point

You do not manually check the token inside every controller.

This is handled automatically by Django REST Framework.

So this code is not required in every controller:

```python
# Not required
if token_is_valid:
    allow_user()
else:
    block_user()
```

DRF does this automatically.

---

## API Testing Using Postman

### 1. Get Token

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:8000/api/token/
```

Body:

```json
{
    "username": "admin",
    "password": "admin123"
}
```

---

### 2. Call Protected API

Method:

```text
GET
```

URL:

```text
http://127.0.0.1:8000/ORSAPI/api/College/
```

Header:

```http
Authorization: Bearer your_access_token_here
```

---

### 3. Refresh Token

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:8000/api/token/refresh/
```

Body:

```json
{
    "refresh": "your_refresh_token_here"
}
```

---

## Common Errors

### Error 1: Authentication credentials were not provided

Reason:

You did not send the token in the header.

Solution:

Add this header:

```http
Authorization: Bearer your_access_token_here
```

---

### Error 2: Token is invalid or expired

Reason:

Access token is expired or wrong.

Solution:

Use refresh token to get a new access token.

---

### Error 3: Public API also asking for token

Reason:

You forgot to add `AllowAny`.

Solution:

Add:

```python
permission_classes = [AllowAny]
```

---

## Final Summary

```text
JWT is like an ID card.

Login API gives token.
Client stores token.
Client sends token with every API request.
Django checks token automatically.
Valid token means access allowed.
Invalid token means access denied.
```

---

## Recommended Project Structure

```text
project/
│
├── settings.py
│   └── REST_FRAMEWORK JWT configuration
│
├── urls.py
│   └── token and refresh token URLs
│
├── ORSAPI/
│   ├── rest/
│   │   ├── UserCtl.py
│   │   │   └── public APIs with AllowAny
│   │   │
│   │   └── CollegeCtl.py
│   │       └── protected APIs
│   │
│   └── urls.py
│       └── API routes
```

---

## Best Practice

Make all APIs protected by default.

Only make required APIs public.

Public APIs:

```text
Login
Forgot Password
User Registration
```

Protected APIs:

```text
College
Student
Role
User Profile
Admin APIs
Search APIs
```

---

## Conclusion

JWT authentication makes Django REST APIs secure.

It is simple:

```text
Login → Get Token → Send Token → Access API
```

This approach is clean, secure, and easy to maintain.
