# Users App

## Overview

The Users app extends Django's built-in User model with profiles. We use a separate Profile model instead of modifying Django's User directly—this is the recommended approach for adding custom user data.

## Models

| Model              | Purpose                                             |
| ------------------ | --------------------------------------------------- |
| **Profile**        | Extends User with redis_key and machine connections |
| **ProfileMachine** | Links users to their machines (tracks when added)   |

## Database Schema

```
┌─────────────┐         ┌──────────────────┐         ┌──────────────┐
│    User     │ 1─────1 │     Profile      │ M─────M │   Machine    │
│ (Django)    │         │                  │         │              │
├─────────────┤         ├──────────────────┤         ├──────────────┤
│ username    │         │ redis_key        │         │ name         │
│ email       │         │ created_at       │         │ description  │
│ password    │         │ updated_at       │         └──────────────┘
└─────────────┘         └──────────────────┘                 │
                                 │                           │
                                 └───────ProfileMachine──────┘
```

## What Happens When a User Signs Up

1. **User created** → Django creates User account
2. **Profile auto-created** → Signal creates Profile with unique redis_key
3. **API key generated** → Default API key created for authentication
4. **Ready to use** → User can now connect machines

## Key Features

- **One profile per user** - Automatic creation via signals
- **Unique redis keys** - Format: `username_<uuid>` for caching/sessions
- **Machine connections** - Users can link multiple machines
- **No duplicate machines** - Database constraint prevents duplicates
- **Timestamps** - Track when profiles and connections are created

## Files

- `models.py` - Profile and ProfileMachine models
- `signals.py` - Auto-creates profile when user registers
- `admin.py` - Admin interface for managing profiles
- `apps.py` - Loads signals on app startup
