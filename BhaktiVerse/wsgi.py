# BhaktiVerse/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# wsgi.py production server use karta hai (Gunicorn)
# Isliye default production hai
# Docker mein bhi DJANGO_SETTINGS_MODULE env var se override hoga
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'BhaktiVerse.settings.production'
)

application = get_wsgi_application()