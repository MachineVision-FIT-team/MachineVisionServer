#!/bin/bash
set -e

echo "Starting Django application..."

echo "Creating database migrations..."
python manage.py makemigrations --noinput

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

    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser with environment variables..."
        python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || {
            echo "ERROR: Failed to create superuser"
            exit 1
        }
        python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); user.set_password('$DJANGO_SUPERUSER_PASSWORD'); user.save()" || {
            echo "ERROR: Failed to set superuser password"
            exit 1
        }
        echo "✓ Superuser created successfully"
    else
        echo "ERROR: Missing environment variables: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD"
        exit 1
    fi
fi

echo "Setup complete. Starting server..."

exec "$@"