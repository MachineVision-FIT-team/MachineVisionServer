"""
ASGI config for NLPServer project.

Exposes the ASGI application for production deployment.
Handles both HTTP and WebSocket protocols with custom middleware.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NLPServer.settings")

# Initialize Django ASGI application early to populate AppRegistry
django_asgi_app = get_asgi_application()

# Import after Django initialization to avoid AppRegistryNotReady errors
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
import api.routing
from api.middleware import ApiKeyValidationMiddleware, InvalidRouteErrorMiddleware

application = ProtocolTypeRouter(
    {
        # HTTP requests with static file handling
        "http": ASGIStaticFilesHandler(django_asgi_app),
        # WebSocket connections with authentication and error handling
        "websocket": InvalidRouteErrorMiddleware(
            ApiKeyValidationMiddleware(URLRouter(api.routing.websocket_urlpatterns))
        ),
    }
)
