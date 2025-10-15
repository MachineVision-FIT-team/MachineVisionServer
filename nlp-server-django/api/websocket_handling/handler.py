import json
from typing import Any, Optional
import logging
from .codes import WebSocketCloseCodes, WebSocketCloseReasons

logger = logging.getLogger(__name__)


class WebSocketConnectionHandler:
    """Manages WebSocket connection operations and responses"""

    @staticmethod
    async def accept(send: Any, subprotocols: Optional[list] = None) -> None:
        """Accept WebSocket connection with optional subprotocols"""
        message = {"type": "websocket.accept"}
        if subprotocols:
            message["subprotocol"] = subprotocols[0]
        await send(message)

    @staticmethod
    async def send_json_message(consumer: Any, **message_data) -> None:
        """Send JSON message through consumer"""
        await consumer.send(text_data=json.dumps(message_data))

    @staticmethod
    async def close(send: Any, code: WebSocketCloseCodes, reason: str = None) -> None:
        """Close accepted WebSocket connection with code and reason"""
        try:
            print("REASON: ", reason)
            if reason is None:
                reason = WebSocketCloseReasons.get_reason(code)
            await send(
                {
                    "type": "websocket.close",
                    "code": int(code),
                    "reason": reason,
                }
            )
        except Exception as e:
            logger.error(f"Error closing WebSocket: {str(e)}")
            raise

    @staticmethod
    async def reject(send: Any, code: WebSocketCloseCodes, reason: str = None) -> None:
        """Reject connection by accepting then immediately closing"""
        try:
            if reason is None:
                reason = WebSocketCloseReasons.get_reason(code)
            await WebSocketConnectionHandler.accept(send)
            await WebSocketConnectionHandler.close(send, code, reason)
        except Exception as e:
            logger.error(f"Error rejecting WebSocket: {str(e)}")
            raise

    @staticmethod
    async def reject_invalid_route(send: Any) -> None:
        """Reject invalid route access"""
        await WebSocketConnectionHandler.reject(send, WebSocketCloseCodes.INVALID_ROUTE)

    @staticmethod
    async def reject_invalid_api_key(send: Any) -> None:
        """Reject invalid or inactive API key"""
        await WebSocketConnectionHandler.reject(
            send, WebSocketCloseCodes.INVALID_API_KEY
        )

    @staticmethod
    async def reject_malformed_api_key(send: Any) -> None:
        """Reject malformed API key format"""
        await WebSocketConnectionHandler.reject(
            send, WebSocketCloseCodes.MALFORMED_API_KEY
        )
