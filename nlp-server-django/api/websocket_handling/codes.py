from enum import IntEnum
from typing import Dict


class WebSocketCloseCodes(IntEnum):
    """WebSocket close codes for application-specific errors"""

    INVALID_ROUTE = 4001
    INVALID_API_KEY = 4002
    MISMATCH_FOR_ROUTE_AND_USER = 4003
    MALFORMED_API_KEY = 4004
    INTERNAL_ERROR = 4500


class WebSocketCloseReasons:
    """Human-readable close reasons corresponding to close codes"""

    REASONS: Dict[int, str] = {
        WebSocketCloseCodes.INVALID_ROUTE: "Invalid WebSocket route",
        WebSocketCloseCodes.INVALID_API_KEY: "Invalid or inactive API key",
        WebSocketCloseCodes.MISMATCH_FOR_ROUTE_AND_USER: "Route mismatch for user type",
        WebSocketCloseCodes.MALFORMED_API_KEY: "Malformed API key format",
        WebSocketCloseCodes.INTERNAL_ERROR: "Internal server error",
    }

    @classmethod
    def get_reason(cls, code: int) -> str:
        """Get reason string for a given close code"""
        return cls.REASONS.get(code, "Unknown error")
