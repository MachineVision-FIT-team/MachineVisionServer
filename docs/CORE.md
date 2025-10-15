# NLPServer - Core Architecture

## Overview

Django-based WebSocket server for real-time natural language command processing. Connects users to machines via authenticated WebSocket connections, processes voice/text commands, and routes them to target devices.

## Tech Stack

- **Django 5.0** - Web framework
- **Django Channels** - WebSocket support
- **Redis** - Channel layer for WebSocket message routing
- **Daphne** - ASGI server

## App Structure

| App              | Purpose                                                   |
| ---------------- | --------------------------------------------------------- |
| **users**        | User profiles with API keys and machine connections       |
| **machines**     | Machine entities with authentication and user links       |
| **api**          | WebSocket routing, middleware, and API key authentication |
| **textanalysis** | NLP keyword/verb vocabulary for command parsing           |

## Architecture Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client    │◄───WS───┤  NLPServer   │◄───WS───┤   Machine   │
│  (Browser)  │         │  (Django)    │         │  (Device)   │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               │
                        ┌──────▼──────┐
                        │    Redis    │
                        │Channel Layer│
                        └─────────────┘
```

## Key Components

### ASGI Configuration

- **HTTP** - Admin interface and static files
- **WebSocket** - Real-time bidirectional communication
- **Middleware chain** - API key validation → Error handling

### Channel Layers (Redis)

- Routes messages between WebSocket connections
- Enables machine-to-user and user-to-machine communication
- Group-based messaging for multi-user scenarios

### Authentication

- **Users** - API keys stored in Profile (via UserAPIKey)
- **Machines** - API keys linked to Machine (via MachineApiKey)
- WebSocket connections authenticated on handshake

## Connection Flow

```
1. Client/Machine connects via WebSocket with API key
2. Middleware validates API key against database
3. Connection added to Redis channel layer
4. Messages routed through Redis to target connections
5. NLP processes commands and forwards to machines
```

## Database

**SQLite** for development (configure PostgreSQL for production)

Key relationships:

- User ←→ Profile ←→ Machines (many-to-many)
- Profile → UserAPIKeys (one-to-many)
- Machine → MachineAPIKeys (one-to-many)

## Environment Variables

```bash
SECRET_KEY=your-secret-key
DEBUG=0
ALLOWED_HOSTS=localhost,yourdomain.com
REDIS_URL=redis://redis:6379
DJANGO_DB_PATH=/path/to/db.sqlite3
```

## Key Files

- `asgi.py` - ASGI application with protocol routing
- `settings.py` - Django configuration with Channels setup
- `api/routing.py` - WebSocket URL patterns
- `api/middleware.py` - Authentication and error handling
- `api/consumers.py` - WebSocket connection handlers

## Design Decisions

**Why separate User and Machine models?**

- Different authentication mechanisms
- Machines can be shared across multiple users
- Clear separation of concerns

**Why Redis for Channel Layer?**

- Enables horizontal scaling
- Persistent message queuing
- Production-ready performance

**Why WebSockets over REST?**

- Real-time bidirectional communication required
- Lower latency for voice commands
- Maintains persistent connections for streaming

**Why NLP vocabulary in database?**

- Dynamic keyword/verb management without code changes
- Admins can add new commands via Django admin
- Version control and auditing of command vocabulary
