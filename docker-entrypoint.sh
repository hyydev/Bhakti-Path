#!/bin/sh
set -e

echo "BhaktiPath Backend Starting..."

echo "Waiting for database..."
while ! python << 'EOF'
import sys, os
try:
    import psycopg2
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT', '5432'),
        connect_timeout=3,
    )
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
EOF
do
    echo "DB not ready, retrying in 2s..."
    sleep 2
done

echo "Database ready!"

echo "Running migrations..."
python manage.py migrate --noinput \
    --settings=BhaktiVerse.settings.production

echo "Collecting static files..."
python manage.py collectstatic --noinput \
    --settings=BhaktiVerse.settings.production

echo "Starting Gunicorn..."
exec gunicorn BhaktiVerse.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info