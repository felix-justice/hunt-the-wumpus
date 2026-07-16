# TODO Create abstract Event class here. Remember to inherit from ABC and
# decorate abstract methods with @abstractmethod
from player import Player
from abc import ABC, abstractmethod

class Event(ABC):
    # abstract base class fro all ccave events

    @abstractmethod
    def encounter(self, player: Player) -> bool:
        """Trigger this event's effect on the playe, returns True if the event 
        will be removed from the room (ex: arrow or treasure cheast picked up)
        """
        pass

    @abstractmethod
    def percept(self) -> str:
        # return the percept message for nearby rooms
        pass
