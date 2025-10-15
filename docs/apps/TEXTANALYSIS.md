# Text Analysis App

## Overview

The Text Analysis app manages keywords and action verbs used for natural language command processing. It stores the vocabulary that allows the system to parse user commands and convert them into machine-readable action identifiers.

## Models

| Model             | Purpose                                                          |
| ----------------- | ---------------------------------------------------------------- |
| **ObjectKeyword** | Objects that can be acted upon (e.g., 'light', 'door', 'window') |
| **ActionVerb**    | Actions to perform on objects (e.g., 'turn on', 'open', 'close') |

## Database Schema

```
┌──────────────────┐         ┌──────────────────┐
│  ObjectKeyword   │         │   ActionVerb     │
├──────────────────┤         ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ keyword          │         │ verb             │
│ identifier       │         │ identifier       │
│ created_at       │         │ related_words    │
│ updated_at       │         │ created_at       │
└──────────────────┘         │ updated_at       │
                             └──────────────────┘
```

## How Command Processing Works

1. **User speaks/types** → "Turn on the kitchen light"
2. **NLP analyzes** → Identifies action verb ("turn on") and object ("light")
3. **Lookup identifiers** → Maps to machine commands (ACTIVATE + LIGHT_KITCHEN)
4. **Send command** → Forwards structured command to target machine via WebSocket
5. **Machine executes** → Performs the action based on identifier

## Key Features

- **Natural language mapping** - Converts human phrases to machine commands
- **Synonym support** - Related words allow multiple ways to say the same action
- **Strict identifiers** - Uppercase alphanumeric format ensures consistency
- **Indexed lookups** - Fast keyword/verb searching for real-time processing
- **Related words** - Store alternative phrases (JSON array)
- **Timestamps** - Track when keywords were added or modified

## Example Data

**ObjectKeyword:**

- keyword: "light" → identifier: "LIGHT_001"
- keyword: "door" → identifier: "DOOR_MAIN"
- keyword: "thermostat" → identifier: "HVAC_CTRL"

**ActionVerb:**

- verb: "turn on" → identifier: "ACTIVATE" → related_words: ["switch on", "enable", "start"]
- verb: "open" → identifier: "OPEN" → related_words: ["unlock", "unseal"]
- verb: "increase" → identifier: "INCREMENT" → related_words: ["raise", "boost", "turn up"]

## Validation Rules

- **Identifiers must be:** UPPERCASE letters, numbers, and underscores only
- **Keywords/verbs must be unique** - No duplicates allowed
- **Related words stored as JSON** - Easy to query and modify

## Admin Interface

- **List view** - Shows keyword/verb, identifier, and creation date
- **Search** - Find by keyword/verb or identifier
- **Filter** - Filter by creation date
- **Related words display** - Shows comma-separated list in admin

## Files

- `models.py` - ObjectKeyword and ActionVerb models
- `admin.py` - Admin interface for managing vocabulary
- `apps.py` - App configuration
