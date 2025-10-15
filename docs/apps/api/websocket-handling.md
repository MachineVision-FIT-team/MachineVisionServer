# WebSocket Handling

## Overview

Manages WebSocket connection lifecycle, close codes, and connection state operations. Provides standardized handlers for accepting, rejecting, and closing WebSocket connections.

## Connection Handlers

Two handler classes work at different layers:

**WebSocketConnectionHandler** (Middleware Layer)

- Works with raw ASGI `send` callable
- Used before consumer instantiation
- Handles pre-connection rejections

**WebsocketConsumerHandler** (Consumer Layer)

- Works with consumer instances
- Used after connection accepted
- Handles post-connection operations

## Connection Lifecycle

```
┌─────────────────────────────────────┐
│  1. Client Connection Attempt      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  2. Middleware Validation           │
│     - Extract API key               │
│     - Validate credentials          │
└────────────┬────────────────────────┘
             │
        Valid? ├─No──► Reject (4002/4004)
             │
            Yes
             │
             ▼
┌─────────────────────────────────────┐
│  3. Consumer Accept                 │
│     - Send auth_response            │
│     - Setup room tracking           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  4. Active Connection               │
│     - Handle messages               │
│     - Route to rooms                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  5. Disconnect                      │
│     - Clean up rooms                │
│     - Close with code               │
└─────────────────────────────────────┘
```

## Close Codes

| Code | Name                        | Reason                              |
| ---- | --------------------------- | ----------------------------------- |
| 4001 | INVALID_ROUTE               | Invalid WebSocket endpoint accessed |
| 4002 | INVALID_API_KEY             | API key not found or inactive       |
| 4003 | MISMATCH_FOR_ROUTE_AND_USER | User type doesn't match route       |
| 4004 | MALFORMED_API_KEY           | API key format invalid              |
| 4500 | INTERNAL_ERROR              | Server-side error                   |

Close reasons are automatically resolved from codes via `WebSocketCloseReasons.get_reason()`.

## Error Handling

Client-safe error responses prevent exposing internal details:

**Error Categories:**

- `connection_error` - Network/connection issues
- `authentication_error` - Permission denied
- `validation_error` - Invalid input
- `processing_error` - Internal processing failure
- `resource_error` - Resource unavailable

**Error Response Format:**

```json
{
  "type": "error",
  "category": "validation_error",
  "message": "Invalid input provided."
}
```

Errors are logged server-side with full details while clients receive sanitized messages.

## Connection Examples

### Successful Connection

```
Client → Valid API key → Middleware validates → Consumer accepts
Response: {"type": "auth_response", "status": "success"}
```

### Rejected Connection

```
Client → Invalid API key → Middleware validates → Reject with code 4002
Response: Close code 4002, reason "Invalid or inactive API key"
```

### Route Mismatch

```
User → /ws/machine/ → Middleware passes → Consumer checks type → Reject with code 4003
Response: Close code 4003, reason "Route mismatch for user type"
```

## Handler Methods

### WebSocketConnectionHandler (Middleware)

- `accept()` - Accept WebSocket handshake
- `reject()` - Reject with close code and reason
- `close()` - Close active connection
- `reject_invalid_api_key()` - Convenience for invalid keys
- `reject_malformed_api_key()` - Convenience for malformed keys
- `reject_invalid_route()` - Convenience for invalid routes

### WebsocketConsumerHandler (Consumer)

- `approve_connection()` - Accept and send welcome message
- `send_json_message()` - Send JSON data through WebSocket
- `close()` - Close with code and reason
- `reject_route_mismatch()` - Reject user type mismatch

## Files

- `handler.py` - Connection handlers for middleware and consumer layers
- `codes.py` - Close code enums and reason mappings
- `error_handler.py` - Client-safe error message conversion
