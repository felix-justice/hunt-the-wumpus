# TODO Create EscapeRope class here
from player import Player
from event import Event

class EscapeRope(Event):
    # this calls represents the rope used to escape the cave

    def encounter(self, player: Player) -> bool:
        if player.has_treasure:
            print("You climb the rope and escape with the treasure! You win!")
            player.has_escaped = True
        else:
            print("You see the rope, but you still need the treasure.")
        return False

    def percept(self) -> str:
        return "This place looks familiar..."
