# TODO Create Arrow class here

from player import Player
from event import Event

class Arrow(Event):
    # represents an arrow that the player can collect

    def encounter(self, player: Player) -> bool:
        print("You found an arrow and add it to your quiver.")
        player.arrows += 1
        return True # remove from the room

    def percept(self) -> str:
        return "You step on something sharp. Ouchie!"
