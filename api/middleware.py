from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user_or_machine_from_api_key(api_key: str) -> Dict[str, Any]:
    from .models import APIKey, MachineApiKey

    api_key_models = [APIKey, MachineApiKey]

    for model in api_key_models:
        try:
            api_key_obj = model.objects.get(key=api_key, is_active=True)
            if isinstance(api_key_obj, APIKey):
                #logger.info("Valid user API key used")
                return {'type': 'user', 'object': api_key_obj.profile.user}
            elif isinstance(api_key_obj, MachineApiKey):
                #logger.info("Valid machine API key used")  
                return {'type': 'machine', 'object': api_key_obj.machine}

        except (ObjectDoesNotExist, ValidationError):
            continue


    #logger.warning(f"Invalid API key used")
    return {'type': 'error', 'object': None}

class APIWSKeyAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope: Dict[str, Any], receive: Any, send: Any) -> Any:
        headers = dict(scope['headers'])
        authorization = headers.get(b'sec-websocket-protocol', b'').decode('utf-8')

        api_key = authorization.split(' ')[-1] if authorization.startswith('Bearer ') else authorization
        if api_key:
            auth_result = await get_user_or_machine_from_api_key(api_key)
        else:                
            logger.warning("No API key found in headers")
            auth_result = {'type': 'error', 'object': None}

        if auth_result['type'] == 'error':
            # Send a close event with error code 4002
            await send({
                    'type': 'websocket.accept'
                })

            await send({
                'type': 'websocket.close',
                'code': 4002,
            })
            return

        scope['auth_type'] = auth_result['type']
        scope['auth_object'] = auth_result['object']
                
        return await super().__call__(scope, receive, send)
    

class RoutingErrorMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        except ValueError as e:
            if 'No route found' in str(e):
                # Send a close event
                await send({
                    'type': 'websocket.accept'
                })

                await send({
                    'type': 'websocket.close',
                    'reason': 'invalid route',
                    'code': 4001,
                })

            else:
                raise e
