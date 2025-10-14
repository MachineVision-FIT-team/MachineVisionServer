from django.urls import re_path
from .consumers.UserConsumer import UserConsumer
from .consumers.MachineConsumer import MachineConsumer

websocket_urlpatterns = [
    # re_path(r'wsapi/$', consumers.YourConsumer.as_asgi()),
    re_path("wsapi/users/$", UserConsumer.as_asgi()),
    re_path("wsapi/machines/$", MachineConsumer.as_asgi()),
]
