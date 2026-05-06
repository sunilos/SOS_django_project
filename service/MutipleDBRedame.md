# Django Multiple Database Configuration Tutorial

This tutorial explains how to configure and use multiple databases in Django.

Supported Databases:
- SQLite
- MySQL
- PostgreSQL
- MongoDB

---

# 1. Default SQLite Configuration

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

# 2. Configure Multiple Databases

```python
# settings.py

DATABASES = {

    # SQLite Database
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    # MySQL Database
    'mysql_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'orsdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    },

    # PostgreSQL Database
    'postgres_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'orsdb',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# 3. Install Database Drivers

## MySQL Driver

```bash
pip install mysqlclient
```

OR

```bash
pip install pymysql
```

If using pymysql:

```python
# __init__.py

import pymysql
pymysql.install_as_MySQLdb()
```

---

## PostgreSQL Driver

```bash
pip install psycopg2
```

---

# 4. Using Multiple Databases

## Save Data in Specific Database

```python
Student.objects.using('mysql_db').create(
    name="Sunil",
    email="sunil@gmail.com"
)
```

---

## Read Data from Specific Database

```python
students = Student.objects.using('postgres_db').all()
```

---

# 5. Database Router (Enterprise Approach)

Create file:

```bash
ors_db_router.py
```

Add router logic:

```python
class ORSDBRouter:

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'studentapp':
            return 'mysql_db'

        return 'default'


    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'studentapp':
            return 'mysql_db'

        return 'default'
```

---

# 6. Register Router

```python
# settings.py

DATABASE_ROUTERS = [
    'project.ors_db_router.ORSDBRouter'
]
```

---

# 7. Migration Commands

## Default Database

```bash
python manage.py migrate
```

---

## MySQL Database

```bash
python manage.py migrate --database=mysql_db
```

---

## PostgreSQL Database

```bash
python manage.py migrate --database=postgres_db
```

---

# 8. Runtime Database Switching

Useful when clients want dynamic DB switching.

```python
# settings.py

ACTIVE_DB = "mysql_db"
```

Use dynamically:

```python
from django.conf import settings

students = Student.objects.using(
    settings.ACTIVE_DB
).all()
```

Switch DB anytime:

```python
ACTIVE_DB = "postgres_db"
```

---

# 9. Configure MongoDB

Install Djongo:

```bash
pip install djongo
```

Configuration:

```python
DATABASES = {

    'default': {
        'ENGINE': 'djongo',
        'NAME': 'orsdb',
        'HOST': 'localhost',
        'PORT': 27017,
    }
}
```

---

# 10. Enterprise Architecture Recommendation

| Database | Usage |
|----------|--------|
| MySQL | Transactional Data |
| PostgreSQL | Analytics |
| MongoDB | JSON / Logs / AI |
| Redis | Cache / Sessions |

---

# 11. Recommended Project Structure

```text
project/
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── ors_db_router.py
│   └── wsgi.py
│
├── studentapp/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
```

---

# 12. Best Practices

- Use database routers for large projects
- Keep transactional and analytics DB separate
- Use Redis for caching
- Use MongoDB for AI and logging
- Use environment variables for passwords
- Never hardcode credentials

Example:

```python
import os

PASSWORD = os.getenv("DB_PASSWORD")
```

---

# 13. Common Errors

## MySQL Error

```text
No module named MySQLdb
```

Solution:

```bash
pip install pymysql
```

---

## PostgreSQL Error

```text
Error loading psycopg2 module
```

Solution:

```bash
pip install psycopg2
```

---

# 14. Conclusion

Django supports:
- Multiple SQL databases
- NoSQL databases
- Runtime database switching
- Enterprise-level routing

This architecture is widely used in scalable enterprise applications.

---
