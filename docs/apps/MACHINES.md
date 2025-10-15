# Machines App

## Overview

The Machines app manages machine entities that can be connected to user profiles. Each machine has its own API keys for authentication and a redis key for caching/sessions.

## Models

| Model       | Purpose                                                             |
| ----------- | ------------------------------------------------------------------- |
| **Machine** | Represents a physical or virtual machine with unique identification |

## Database Schema

```
┌──────────────────┐         ┌──────────────────┐
│     Machine      │ 1─────M │  MachineApiKey   │
├──────────────────┤         ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ name             │         │ machine_id (FK)  │
│ machine_id       │         │ name             │
│ redis_key        │         │ key (UUID)       │
│ created_at       │         │ is_active        │
│ updated_at       │         │ created_at       │
└──────────────────┘         └──────────────────┘
         │
         │ M
         │
         │ M
┌──────────────────┐
│ ProfileMachine   │
├──────────────────┤
│ id (PK)          │
│ profile_id (FK)  │────────┐
│ machine_id (FK)  │        │
│ created_at       │        │
└──────────────────┘        │
                            │ M
                            │
                    ┌───────▼──────┐
                    │   Profile    │
                    ├──────────────┤
                    │ id (PK)      │
                    │ user_id (FK) │
                    │ redis_key    │
                    └──────────────┘
```

## What Happens When a Machine is Created

1. **Machine created** → Admin creates machine with name
2. **Redis key auto-generated** → Signal creates unique redis key: `machine_<name>_<uuid>`
3. **API key generated** → Default API key created for authentication
4. **Ready to connect** → Machine can now be linked to user profiles

## Key Features

- **Unique machine ID** - UUID automatically generated
- **Auto-generated redis keys** - Format: `machine_<name>_<short_uuid>`
- **Default API key** - Created automatically on machine creation
- **Multiple API keys** - Can add additional keys after creation
- **User connections** - Track which users are linked to each machine
- **Timestamps** - Track when machines are created and updated

## Admin Interface

- **List view** - Shows name, machine_id, redis_key, creation date, and connected user count
- **Search** - Find machines by name, machine_id, or redis_key
- **Filter** - Filter by creation date
- **Connected users** - Clickable links to user profiles for easy navigation
- **API key management** - Add/edit API keys inline (only after initial creation)

## Files

- `models.py` - Machine model definition
- `signals.py` - Auto-creates redis key and default API key
- `admin.py` - Admin interface for managing machines
- `apps.py` - Loads signals on app startup
