# Room Management

## Overview

Manages WebSocket room membership using Redis sets. Machines create persistent rooms that users join for real-time command routing.

## Architecture

```
┌──────────────┐
│   Machine    │  Creates & owns room
│ (channel_A)  │
└──────┬───────┘
       │ create room on connect
       ▼
┌─────────────────────────────┐
│  Redis Room                 │
│  "machine_<key>_room"       │
│                             │
│  Members:                   │
│  - channel_A (machine)      │
│  - channel_B (user_1)       │◄─── Users join
│  - channel_C (user_2)       │◄─── machine's room
└─────────────────────────────┘
       │
       │ Commands routed to machine
       ▼
   Machine executes
```

## Room Concept

**What is a room?**

- Redis set containing channel names
- Named after machine: `machine_<redis_key>_room`
- Persistent space for machine ↔ users communication

**Why rooms?**

- Route commands to specific machine
- Track active connections
- Enable one machine ↔ multiple users
- Clean disconnect handling

## Room Lifecycle

```
1. Machine connects → creates its room automatically
2. Users join machine's room when they want to control it
3. Commands sent to room reach the machine
4. Users leave → removed from room
5. Machine disconnects → room deleted from Redis
```

**Key Point:** Machines own rooms. Users join machines they want to control.

## Redis Structure

**Room naming:**

```
machine_<redis_key>_room
```

**Storage:** Redis Set (SADD, SREM, SMEMBERS, SCARD, DELETE)

**Example:**

```
Key: machine_cnc_001_abc123_room
Members: ["machine.channel!xyz", "user.channel!abc", "user.channel!def"]
```

## Room Operations

**Join Room**

- Adds channel to Redis set
- Tracks room locally in consumer
- Machines join on connect, users join on demand

**Leave Room**

- Removes channel from Redis set
- Clears local tracking
- Deletes Redis room if empty

**Check Join Permission**

- Returns true if room exists or member already in
- Allows multiple users per machine

**Get Room Members**

- Returns set of channel names in room
- Used for message routing

**Clear Member from All Rooms**

- Removes member from every room they're in
- Cleans up empty rooms
- Called on disconnect

**Get Room Count**

- Returns number of members in room
- Used to check if machine has active users

## Room Constraints

**Multiple users per machine:**

- Multiple operators can control same machine
- Useful for supervision, shift changes, emergency overrides
- First-come basis for command conflicts

**Room ownership:**

- Machine creates room on connect
- Room persists as long as machine is connected
- Machine disconnecting destroys the room

**Auto-cleanup:**

- Empty rooms deleted from Redis
- Prevents memory leaks
- Local tracking cleared on disconnect

## Message Routing

Commands are routed through rooms to reach target machines:

```
User joins machine room
    ↓
User sends voice command
    ↓
Command routed to all room members
    ↓
Machine receives and executes
    ↓
Machine sends status back through room
    ↓
All users in room receive update
```

## Real-World Use Cases

**Factory Floor:**

- CNC machine creates room
- Operator joins to send commands
- Supervisor joins to monitor
- Safety controller joins for emergency stop

**Multiple Machine Control:**

- User joins Machine_A room → controls Machine_A
- User joins Machine_B room → controls Machine_B
- User can switch between machines seamlessly

**Shift Handoff:**

- Operator_1 controls machine
- Operator_2 joins same room
- Operator_1 leaves
- Operator_2 continues control

## Files

- `RoomManager.py` - Room membership management with Redis
