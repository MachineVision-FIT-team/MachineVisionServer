#!/bin/bash
set -e

# Load environment variables from .env file in the parent directory (project root)
if [ -f ../.env ]; then
    echo "Loading environment variables from ../.env file..."
    set -a  # Automatically export all variables
    source ../.env
    set +a  # Disable automatic export
else
    echo "No .env file found in parent directory, relying on existing environment variables."
fi

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

    # Check for required environment variables
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser with environment variables..."
        python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || {
            echo "ERROR: Failed to create superuser with provided credentials"
            exit 1
        }
        # Set the password separately since createsuperuser --noinput doesn't handle it
        python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); user.set_password('$DJANGO_SUPERUSER_PASSWORD'); user.save()" || {
            echo "ERROR: Failed to set superuser password"
            exit 1
        }
        echo "✓ Superuser '$DJANGO_SUPERUSER_USERNAME' created successfully"
    else
        echo "ERROR: Cannot create superuser. Missing required environment variables."
        echo "Please set the following environment variables in your ../.env file or environment:"
        echo "  - DJANGO_SUPERUSER_USERNAME"
        echo "  - DJANGO_SUPERUSER_EMAIL"
        echo "  - DJANGO_SUPERUSER_PASSWORD"
        exit 1
    fi
fi

echo ""
echo "Setup complete. Starting server..."

# Execute whatever command was passed as CMD
exec "$@"