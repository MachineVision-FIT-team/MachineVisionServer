#!/bin/bash
set -e

echo "Starting Django application..."

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; then
    echo "✓ Superuser already exists"
else
    echo ""
    echo "=========================================="
    echo "No superuser found - creating one now"
    echo "=========================================="
    python manage.py createsuperuser
fi

echo ""
echo "Setup complete. Starting server..."

# Execute whatever command was passed as CMD
exec "$@"