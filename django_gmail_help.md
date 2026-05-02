# Help / Troubleshooting: Gmail Setup in Django Application

## Problem

Your Django application is not able to send email through Gmail.

You may see this error:

```
535, b'5.7.8 Username and Password not accepted'
SMTPAuthenticationError: BadCredentials
```

---

## Root Cause

In `settings.py`, Gmail credentials are still placeholders:

```python
EMAIL_HOST_USER = 'abc@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
```

These are fake values. Gmail requires real Gmail credentials with an **App Password**, not your normal Gmail account password.

---

# How to Fix Gmail SMTP in Django

## Step 1: Enable 2-Step Verification

Open:
https://myaccount.google.com/security

Under **How you sign in to Google**, enable:
2-Step Verification

---

## Step 2: Generate Gmail App Password

Open:
https://myaccount.google.com/apppasswords

Steps:
1. Select app name as Django
2. Click Create
3. Google will generate a 16-character password like:
abcd efgh ijkl mnop

Remove the spaces before using it.

---

## Step 3: Update settings.py

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'
```

---

## Why Normal Gmail Password Does Not Work

Google stopped allowing direct SMTP login using normal account passwords in May 2022.

---

## HTML Email Issue

```python
from django.core.mail import send_mail

send_mail(
    subject='Welcome',
    message='This is plain text fallback.',
    from_email='yourgmail@gmail.com',
    recipient_list=['user@example.com'],
    html_message='<h1>Welcome</h1><p>This is an HTML email.</p>',
)
```

---

## Final Checklist

- Gmail account is real
- 2-Step Verification is enabled
- App Password is generated
- Spaces removed from App Password
- settings.py updated
- EMAIL_USE_TLS = True
- EMAIL_PORT = 587
