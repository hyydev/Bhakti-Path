"""
Production Settings
===================
Yahan security sabse important hai.
DEBUG kabhi True nahi hoga yahan.
"""

import os
from .base import *


# ─── DEBUG ───
# KABHI True mat karna
# True hone pe:
#   → Stack traces publicly visible
#   → DB queries visible
#   → Secret settings visible
DEBUG = False


# ─── ALLOWED HOSTS ───
# Sirf tere domain se requests allow hongi
# .env mein: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# .split(',') → ['yourdomain.com', 'www.yourdomain.com']
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost'
).split(',')


# ─── CORS ───
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000'
).split(',')


# ─── WHITENOISE — Static Files ───
# Django khud static files serve karta hai
# Nginx ke bina bhi kaam karta hai
#
# MIDDLEWARE mein index 1 pe insert karo
# SecurityMiddleware (index 0) ke baad aana chahiye
# Kyunki security checks pehle honi chahiye
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# CompressedManifestStaticFilesStorage:
#   → Static files compress karta hai (gzip)
#   → Filename mein hash lagata hai
#   → style.css → style.abc123.css (cache busting)
#   → Browser same file dobara download nahi karta
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─── EMAIL — SendGrid SMTP ───
# Production mein actual emails jaayengi
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'                        # ← literally "apikey" string
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')  # ← actual API key


# ─── SECURITY HEADERS ───
# Yeh sab HTTP response headers hain
# Browser ko batate hain kaise behave karna hai

# Agar HTTP pe request aaye → HTTPS pe redirect karo
SECURE_SSL_REDIRECT = config(
    'SECURE_SSL_REDIRECT',
    default=True,
    cast=bool
)

# Cookie sirf HTTPS pe jaaye
# HTTP pe intercept nahi ho sakti
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS: Browser ko batao "hamesha HTTPS use karo"
# 31536000 seconds = 1 year
# Ek baar browser ne dekha → 1 year tak sirf HTTPS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Browser content-type sniff mat karo
# "main JavaScript bhej raha hoon" → browser trust kare
SECURE_CONTENT_TYPE_NOSNIFF = True

# Tera page kisi aur site ke iframe mein nahi khuleg
# Clickjacking attack rokta hai
X_FRAME_OPTIONS = 'DENY'

# Nginx/Docker ke peeche hone pe
# Actual protocol batata hai (https)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ─── LOGGING ───
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            # ERROR 2024-01-15 10:30:00 views 1234 Message here
            'format': '{levelname} {asctime} {module} {process:d} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            # Docker logs mein dikhega
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'formatter': 'verbose',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}