# PLayer class representing user state

class Player:
    # tracks the players stats and status

    def __init__(self) -> None:
        self.is_alive: bool = True
        self.has_treasure: bool = False
        self.has_escaped: bool = False
        self.arrows: int = 0
        self.confused_turns: int = 0


