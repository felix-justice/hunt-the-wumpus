# TODO Create BatSwarm class here.
from event import Event
from player import Player

class BatSwarm(Event):
    # represents a swarm of confusing bats

    def encounter(self, player: Player) -> bool:
        print("Bats surround you! Your controls are reversed for 5 turns!")
        player.confused_turns = 5
        return False

    def percept(self) -> str:
        return "You hear wings flapping."

