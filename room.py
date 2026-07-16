# room class for containing an optional event

from typing import Optional
from event import Event

class Room:
    # represents a single room that may hold an event

    _event: Optional[Event]

    def __init__(self) -> None:
        self._event = None

    def get_event(self) -> Optional[Event]:
        # return the event in this room, or none if empty
        return self._event

    def set_event(self, event: Optional[Event]) -> None:
        # place or remove an event freom this room
        self._event = event

    def has_event(self) -> bool:
        # returns True if the room contains an event
        return self._event is not None
