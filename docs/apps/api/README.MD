# API App

## Overview

The API app handles WebSocket connections, authentication, and real-time communication between users and machines. It provides the core infrastructure for the NLP server's bidirectional messaging system.

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ WebSocket + API Key
       ▼
┌─────────────────────────────┐
│  Middleware Layer           │
│  - API Key Validation       │
│  - Route Validation         │
└──────┬──────────────────────┘
       │ auth_type, auth_object
       ▼
┌─────────────────────────────┐
│  Consumer Layer             │
│  - UserConsumer             │
│  - MachineConsumer          │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Redis Channel Layer        │
│  - Room Management          │
│  - Message Routing          │
└─────────────────────────────┘
```

## WebSocket Routes

| Route          | Consumer        | Purpose                                   |
| -------------- | --------------- | ----------------------------------------- |
| `/ws/user/`    | UserConsumer    | User connections for command input        |
| `/ws/machine/` | MachineConsumer | Machine connections for command execution |

**Connection format:**

```
ws://host:port/ws/user/
Protocol header: sec-websocket-protocol: <api-key>
```

## Authentication

### API Key Models

Two types of API keys inherit from an abstract base:

**ApiKey (Abstract Base)**

- UUID-based keys
- Active/inactive status
- Auto-discovery of subclasses
- Indexed for fast lookups

**UserAPIKey**

- Links to user Profile
- Returns user object on auth

**MachineApiKey**

- Links to Machine
- Returns machine object on auth

### Authentication Flow

```
1. Client connects with API key in protocol header
2. Middleware extracts and validates key
3. Database lookup across all ApiKey subclasses
4. Sets auth_type and auth_object in scope
5. Consumer receives authenticated connection
```

## App Initialization

**spaCy Model Loading**

- NLP model (`en_core_web_sm`) loaded on app startup
- Available globally via `ApiConfig.nlp`
- Graceful error handling if model unavailable

## Key Features

- **Flexible authentication** - Abstract base allows multiple API key types
- **Protocol header auth** - Uses `sec-websocket-protocol` for WebSocket compatibility
- **Auto-discovery** - Dynamically finds all ApiKey subclasses
- **Type-safe routing** - Named URL patterns for maintainability
- **Shared NLP model** - Single spaCy instance across all consumers

## Security

- API keys are UUIDs (128-bit entropy)
- Keys can be deactivated without deletion
- Middleware validates before consumer access
- Partial key logging (first 8 chars only)
- See [Middleware Documentation](middleware.md) for validation details

## Database Schema

```
┌──────────────────┐         ┌──────────────────┐
│   UserAPIKey     │         │  MachineApiKey   │
├──────────────────┤         ├──────────────────┤
│ key (UUID)       │         │ key (UUID)       │
│ profile_id (FK)  │         │ machine_id (FK)  │
│ name             │         │ name             │
│ is_active        │         │ is_active        │
│ created_at       │         │ created_at       │
└──────────────────┘         └──────────────────┘
         │                            │
         └────────────┬───────────────┘
                      │
              ┌───────▼────────┐
              │   ApiKey       │
              │   (Abstract)   │
              └────────────────┘
```

## Files

- `models.py` - API key models and authentication
- `routing.py` - WebSocket URL patterns
- `apps.py` - App configuration and spaCy initialization
- `middleware.py` - Authentication and validation (see [Middleware](middleware.md))
- `websocket_handling/` - Connection handlers and room management
  - `handler.py` - WebSocket connection lifecycle (see [WebSocket Handling](websocket-handling.md))
  - `codes.py` - Close codes and reasons
  - `RoomManager.py` - Redis room management (see [Room Management](room-management.md))
  - `error_handler.py` - Client-safe error handling
- `consumers/` - WebSocket connection handlers (see [Consumers](consumers.md))
