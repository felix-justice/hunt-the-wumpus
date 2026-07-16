# TODO Create BottomlessPit class here.
from player import Player
import random
from event import Event

class BottomlessPit(Event):
    # Represents a dangerous bottomless pit


    def encounter(self, player: Player) -> bool:
        # 50% chance player falls and dies
        if random.random() < 0.5:
            print("You fell into a bottomless pit! Game over.")
            player.is_alive = False
        else:
            print("You almost fell in, but caught yourself!")
        return False

    def percept(self) -> str:
        return "You feel a breeze."
