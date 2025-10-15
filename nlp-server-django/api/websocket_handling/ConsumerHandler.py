import json
import logging
from .codes import WebSocketCloseCodes, WebSocketCloseReasons

logger = logging.getLogger(__name__)


class WebsocketConsumerHandler:
    """Manages WebSocket consumer operations"""

    @staticmethod
    async def send_json_message(consumer, **message_data) -> None:
        """Send JSON message through consumer"""
        await consumer.send(text_data=json.dumps(message_data))

    @staticmethod
    async def approve_connection(consumer) -> None:
        """Accept connection and send success message"""
        await consumer.accept()
        await WebsocketConsumerHandler.send_json_message(
            consumer,
            type="auth_response",
            message=f"{consumer.auth_type} {consumer.auth_object} successfully connected",
            status="success",
        )

    @staticmethod
    async def close(consumer, code: WebSocketCloseCodes, reason: str = None) -> None:
        """Close accepted WebSocket connection"""
        try:
            if reason is None:
                reason = WebSocketCloseReasons.get_reason(code)
            await consumer.close(code=int(code), reason=reason)
        except Exception as e:
            logger.error(f"Error closing WebSocket: {str(e)}")
            raise

    @staticmethod
    async def reject_route_mismatch(consumer) -> None:
        """Reject when user type doesn't match route"""
        await WebsocketConsumerHandler.close(
            consumer,
            WebSocketCloseCodes.MISMATCH_FOR_ROUTE_AND_USER,
        )
