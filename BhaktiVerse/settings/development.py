"""
Development Settings
====================
Sirf local development ke liye.
Production mein kabhi use mat karna.

`from .base import *` — base ki saari settings
inherit ho jaati hain. Yahan sirf override karte hain
jo dev mein alag chahiye.
"""

from .base import *

# ─── DEBUG ───
# True: errors ka poora stack trace browser mein
# False: generic 500 page
# Dev mein True zaroori hai debugging ke liye
DEBUG = True


# ─── ALLOWED HOSTS ───
# Dev mein * — koi bhi host se request accept karo
# localhost, 127.0.0.1, ya koi bhi
ALLOWED_HOSTS = ['*']


# ─── CORS ───
# Dev mein sab allowed
# Frontend kisi bhi port pe chale — kaam karega
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS define karne ki zaroorat nahi
# kyunki CORS_ALLOW_ALL_ORIGINS = True sab allow karta hai


# ─── DRF OVERRIDE ───
# base.py mein sirf JSONRenderer hai
# Dev mein BrowsableAPI bhi on karo
# Browser se /api/ pe jaao → clickable interface milega
REST_FRAMEWORK = {
    **REST_FRAMEWORK,    # base ki saari settings raho
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # Dev mein throttle off — testing mein rate limit annoying hota hai
    # 200/hour hit ho jaaye toh debugging mushkil
    'DEFAULT_THROTTLE_CLASSES': [],
}


# ─── EMAIL ───
# Dev mein actual email mat bhejo
# Terminal mein print hoga — SendGrid quota waste nahi
# python manage.py runserver → email content terminal mein dikhega
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'