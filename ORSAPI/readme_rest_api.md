# College REST API – Django (DRF)

## 📌 Overview
This document explains the REST endpoints created in:

```
ORSAPI/rest/CollegeCtl.py
```

The API supports full CRUD operations for **College**.

---

## 🌐 Base URL
```
http://127.0.0.1:8000/ORSAPI/api/College/
```

---

## 🚀 Endpoints Summary

| Method | URL | Action |
|--------|-----|--------|
| GET | /ORSAPI/api/College/ | List all colleges |
| GET | /ORSAPI/api/College/<id>/ | Get single college |
| POST | /ORSAPI/api/College/ | Create college |
| PUT | /ORSAPI/api/College/<id>/ | Update college |
| DELETE | /ORSAPI/api/College/<id>/ | Delete college |

---

## 🔗 Full URLs

| Action | URL |
|--------|-----|
| GET all | http://127.0.0.1:8000/ORSAPI/api/College/ |
| GET one | http://127.0.0.1:8000/ORSAPI/api/College/1/ |
| POST | http://127.0.0.1:8000/ORSAPI/api/College/ |
| PUT | http://127.0.0.1:8000/ORSAPI/api/College/1/ |
| DELETE | http://127.0.0.1:8000/ORSAPI/api/College/1/ |

---

## 📦 Request Body (POST / PUT)

**Content-Type:** `application/json`

```json
{
    "name": "ABC College",
    "address": "MG Road",
    "state": "Madhya Pradesh",
    "city": "Indore",
    "phoneNumber": "9876543210"
}
```

---

## 📤 Response Format

All API responses follow a consistent structure:

```json
{
    "error": false,
    "message": "Success",
    "data": {}
}
```

---

## 🧪 Testing the API

### 🔹 Browser (GET)
Open in browser:
```
http://127.0.0.1:8000/ORSAPI/api/College/
```

👉 Django REST Framework provides a **Browsable API UI**

---

### 🔹 Tools for Testing
- Postman  
- cURL  
- Browser (for GET requests)

---

## ⚙️ Notes

- Ensure Django server is running:
  ```
  python manage.py runserver
  ```

- For PUT/DELETE, use tools like **Postman**.
- `<id>` should be replaced with actual record ID.

---

## ✅ Conclusion

This API provides a clean and consistent way to:
- Create
- Read
- Update
- Delete  

College records using Django REST Framework.
