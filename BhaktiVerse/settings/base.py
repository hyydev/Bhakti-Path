"""
Base Settings — BhaktiPath Project
====================================
Yeh file dev aur prod dono mein use hoti hai.
Environment-specific cheezein yahan nahi aayengi.

Kya yahan hai:
  - INSTALLED_APPS
  - MIDDLEWARE
  - DATABASE structure (values .env se)
  - REST_FRAMEWORK config
  - JWT config (fixed bugs)
  - Redis cache
  - Razorpay credentials
  - Email config structure
  - Sentry config

Kya yahan nahi hai:
  - DEBUG (dev/prod mein alag)
  - ALLOWED_HOSTS (dev/prod mein alag)
  - CORS origins (dev/prod mein alag)
  - Security headers (sirf prod mein)
  - Logging (sirf prod mein detailed)
"""

import os
import sentry_sdk
from datetime import timedelta
from pathlib import Path
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# ─── BASE DIR ───
# Pehle settings.py mein:
#   BASE_DIR = Path(__file__).resolve().parent.parent
#   __file__ = BhaktiVerse/settings.py
#   .parent  = BhaktiVerse/
#   .parent  = Bhakti-Path-main/  ← project root ✓

# Ab base.py mein:
#   __file__ = BhaktiVerse/settings/base.py
#   .parent  = BhaktiVerse/settings/
#   .parent  = BhaktiVerse/
#   .parent  = Bhakti-Path-main/  ← project root ✓
#   Ek extra .parent isliye
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ─── SECRET KEY ───
# .env se lo — kabhi hardcode mat karo
# config() → python-decouple → .env file padhta hai
# Agar .env mein nahi mila → UndefinedValueError throw karega
# Yeh intentional hai — bina SECRET_KEY ke server start hi nahi hoga
SECRET_KEY = config('SECRET_KEY')


# ─── INSTALLED APPS ───
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders',
    'django_filters',

    # Our apps
    'apps.User.apps.UserConfig',
    'apps.Auth',
    'apps.ProductsManagement.apps.ProductsManagementConfig',
    'apps.Order',
    'apps.Payments',
]


# ─── MIDDLEWARE ───
# Order matters! Upar wala pehle chalta hai
# CorsMiddleware → CommonMiddleware se pehle aana zaroori hai
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise production.py mein index 1 pe inject hoga
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─── URLS + WSGI ───
ROOT_URLCONF = 'BhaktiVerse.urls'
WSGI_APPLICATION = 'BhaktiVerse.wsgi.application'


# ─── TEMPLATES ───
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ─── CUSTOM USER MODEL ───
AUTH_USER_MODEL = 'User.User'


# ─── DATABASE ───
# Structure same hai dev aur prod mein
# Sirf values change hongi (.env se)
#
# CONN_MAX_AGE = 60:
#   Har request pe naya DB connection mat banao
#   60 seconds tak connection reuse karo
#   Performance improvement especially under load
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST',    default='localhost'),
        'PORT':     config('DB_PORT',    default='5432'),
        'CONN_MAX_AGE': config('CONN_MAX_AGE', default=60, cast=int),
    }
}


# ─── PASSWORD VALIDATION ───
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── REST FRAMEWORK ───
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Sirf JSON — BrowsableAPI dev mein on hoga (development.py mein)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # Rate limiting — dev mein off hoga (development.py mein)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/hour',
        'user': '2000/hour',
    },
}


# ─── JWT ───
# Bug fixes:
#   ACCESS_TOKEN_LIFETIME: 30 days → 15 minutes
#   ROTATE_REFRESH_TOKENS: False   → True
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}


# ─── INTERNATIONALIZATION ───
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'    # UTC se fix — India timezone
USE_I18N = True
USE_TZ = True


# ─── STATIC + MEDIA ───
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# collectstatic command sab static files yahan laata hai
# WhiteNoise production mein yahan se serve karega

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ─── DEFAULT AUTO FIELD ───
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─── REDIS CACHE ───
# LOCATION .env se aata hai
# Dev:    redis://127.0.0.1:6379/1  (localhost)
# Docker: redis://redis:6379/1      (container name)
#
# IGNORE_EXCEPTIONS: True
#   Redis down hone pe site crash nahi karegi
#   Cache miss treat karega silently
#   DB se fresh data fetch karega
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": 60 * 60,
    }
}


# ─── RAZORPAY ───
RAZORPAY_KEY_ID       = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET   = config('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = config('RAZORPAY_WEBHOOK_SECRET')


# ─── EMAIL ───
# Dev mein development.py override karega → console backend
# Prod mein production.py override karega → SendGrid SMTP
SENDGRID_API_KEY  = config('SENDGRID_API_KEY',  default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@bhaktipath.com')
DEFAULT_FROM_NAME  = config('DEFAULT_FROM_NAME',  default='BhaktiPath')


# ─── CORS — Base config ───
# Origins dev/prod mein alag files mein define honge
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_METHODS = [
    "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
    "x-razorpay-signature",
]


# ─── SENTRY ───
# DSN available hone pe initialize karo
# Dev mein DSN .env mein ho toh dev errors bhi capture honge
# Prod mein alag DSN hogi
SENTRY_DSN = config('SENTRY_DSN', default='')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(transaction_style='url'),
            RedisIntegration(),
        ],
        traces_sample_rate=config(
            'SENTRY_TRACES_SAMPLE_RATE',
            default=1.0,
            cast=float
        ),
        environment=config('SENTRY_ENVIRONMENT', default='development'),
        send_default_pii=False,
    )