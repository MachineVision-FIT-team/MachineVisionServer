from django.urls import path
from .consumers.UserConsumer import UserConsumer
from .consumers.MachineConsumer import MachineConsumer

websocket_urlpatterns = [
    path("ws/user/", UserConsumer.as_asgi(), name="ws_user"),
    path("ws/machine/", MachineConsumer.as_asgi(), name="ws_machine"),
]
