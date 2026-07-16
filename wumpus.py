# TODO Create Wumpus class here.
from event import Event
from player import Player

class Wumpus(Event):
    # represents the deadly wumpus creature

    def encounter(self, player: Player) -> bool:
        # player dies immediately when meeting the Wumpus
        print("The wumpus devours you whole! Game over.")
        player.is_alive = False
        return False

    def percept(self) -> str:
        return "A stench permeates the air."


