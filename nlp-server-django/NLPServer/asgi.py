"""
ASGI config for NLPServer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NLPServer.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Now import your routing and middleware AFTER Django is initialized
from channels.routing import ProtocolTypeRouter, URLRouter
import api.routing
from api.middleware import ApiKeyValidationMiddleware, InvalidRouteErrorMiddleware
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

application = ProtocolTypeRouter(
    {
        "http": ASGIStaticFilesHandler(django_asgi_app),  # Wrap with static handler
        "websocket": InvalidRouteErrorMiddleware(
            ApiKeyValidationMiddleware(URLRouter(api.routing.websocket_urlpatterns))
        ),
    }
)
