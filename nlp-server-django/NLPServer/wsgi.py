"""
WSGI config for NLPServer project.

Exposes the WSGI application for traditional HTTP deployments.
Note: This project primarily uses ASGI for WebSocket support.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NLPServer.settings")

application = get_wsgi_application()
