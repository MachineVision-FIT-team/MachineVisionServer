from enum import Enum
import logging
from typing import Dict, Type


class ErrorCategory(Enum):
    """Categories of errors that can be safely communicated to clients"""

    CONNECTION_ERROR = "connection_error"
    AUTHENTICATION_ERROR = "authentication_error"
    VALIDATION_ERROR = "validation_error"
    PROCESSING_ERROR = "processing_error"
    RESOURCE_ERROR = "resource_error"


class ClientError:
    """Handles error messages that are safe to send to clients"""

    ERROR_MESSAGES: Dict[Type[Exception], tuple[ErrorCategory, str]] = {
        ConnectionError: (
            ErrorCategory.CONNECTION_ERROR,
            "Unable to establish connection. Please try again.",
        ),
        ValueError: (
            ErrorCategory.VALIDATION_ERROR,
            "Invalid input provided.",
        ),
        PermissionError: (
            ErrorCategory.AUTHENTICATION_ERROR,
            "You don't have permission to perform this action.",
        ),
        ResourceWarning: (
            ErrorCategory.RESOURCE_ERROR,
            "The requested resource is currently unavailable.",
        ),
        KeyError: (
            ErrorCategory.VALIDATION_ERROR,
            "Required field missing.",
        ),
    }

    @staticmethod
    def handle_error(error: Exception, logger: logging.Logger) -> dict:
        """
        Convert internal errors to client-safe messages

        Args:
            error: The caught exception
            logger: Logger instance for recording error details

        Returns:
            Dict containing safe error message for client
        """
        logger.error(f"Error: {type(error).__name__}: {str(error)}", exc_info=True)

        error_category, message = ClientError.ERROR_MESSAGES.get(
            type(error),
            (
                ErrorCategory.PROCESSING_ERROR,
                "An unexpected error occurred. Please try again later.",
            ),
        )

        return {
            "type": "error",
            "category": error_category.value,
            "message": message,
        }
