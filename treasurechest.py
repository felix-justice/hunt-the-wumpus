# TODO Create TreasureChest class here.
from event import Event
from player import Player

class TreasureChest(Event):
    # the treasure the player must recover

    def encounter(self, player: Player) -> bool:
        print("You found the treasure chest! You pick it up.")
        player.has_treasure = True
        return True # removce fromm the room

    def percept(self) -> str:
        return "You see something shimmer in the distance."
