#!/bin/sh
set -e

echo "BhaktiPath Backend Starting..."

echo "Waiting for database..."

python << 'EOF'
import os
print("DB_HOST =", repr(os.getenv("DB_HOST")))
print("DB_NAME =", repr(os.getenv("DB_NAME")))
print("DB_USER =", repr(os.getenv("DB_USER")))
print("DB_PORT =", repr(os.getenv("DB_PORT")))
EOF

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
        connect_timeout=5,
        sslmode='require',
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"DB error: {e}", file=sys.stderr)
    sys.exit(1)
EOF
do
    echo "DB not ready, retrying in 2s..."
    sleep 2
done

echo "Database ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn BhaktiVerse.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info