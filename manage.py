#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # Default: development settings use karo
    # Docker/Production mein yeh env var set hoga:
    # DJANGO_SETTINGS_MODULE=BhaktiVerse.settings.production
    # Toh woh override ho jaayega
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'BhaktiVerse.settings.development'  # ← path change kiya
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()