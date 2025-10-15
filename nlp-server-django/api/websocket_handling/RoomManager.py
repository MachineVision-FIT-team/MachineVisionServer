class RoomManager:
    """Manages WebSocket room membership using Redis"""

    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.active_rooms = set()

    def _get_room_name(self, machine_key: str) -> str:
        """Generate consistent room name from machine key"""
        return f"machine_{machine_key}_room"

    async def join_room(self, machine_key: str, channel_name: str) -> bool:
        """Add member to room"""
        room_name = self._get_room_name(machine_key)
        self.active_rooms.add(room_name)
        await self.redis_client.sadd(room_name, channel_name)
        return True

    async def leave_room(self, machine_key: str, channel_name: str) -> bool:
        """Remove member from room and clean up"""
        room_name = self._get_room_name(machine_key)
        await self.redis_client.srem(room_name, channel_name)

        # Clean up room tracking
        self.active_rooms.discard(room_name)

        # Also clean up the Redis set if empty
        remaining = await self.redis_client.scard(room_name)
        if remaining == 0:
            await self.redis_client.delete(room_name)

        return True

    async def get_room_members(self, machine_key: str) -> set:
        """Get all members in room"""
        room_name = self._get_room_name(machine_key)
        return await self.redis_client.smembers(room_name)

    async def can_join_room(self, machine_key: str, channel_name: str) -> bool:
        """Check if channel can join room"""
        room_members = await self.get_room_members(machine_key)
        # Allow if room is empty or member already in room
        return len(room_members) == 0 or channel_name in room_members

    async def clear_member_from_all_rooms(self, channel_name: str) -> None:
        """Remove member from all their active rooms"""
        for room_name in self.active_rooms.copy():
            await self.redis_client.srem(room_name, channel_name)

            # Clean up empty rooms
            remaining = await self.redis_client.scard(room_name)
            if remaining == 0:
                await self.redis_client.delete(room_name)

        # Clear all tracked rooms for this member
        self.active_rooms.clear()

    async def get_room_count(self, machine_key: str) -> int:
        """Get number of members in room"""
        room_name = self._get_room_name(machine_key)
        return await self.redis_client.scard(room_name)
