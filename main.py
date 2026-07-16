import random
from typing import List
from room import Room
from player import Player
from wumpus import Wumpus
from bottomlesspit import BottomlessPit
from batswarm import BatSwarm
from treasurechest import TreasureChest
from arrow import Arrow
from escaperope import EscapeRope
from event import Event
from typing import Tuple

def get_int_input(prompt: str, minimum: int, maximum: int) -> int:
    # Ask for a number and reprompt until it's between min and max
    while True:
        value = input(prompt)

        # check if this is a valdi integer string
        if value.isdigit():
            number = int(value)

            # check the allowed range
            if minimum <= number <= maximum:
                return number

        print(f"Enter a number between {minimum} and {maximum}")

def get_debug_mode() -> bool:
    # ask if the player wants to debug mode (1=yes, 0= no)
    while True:
        choice = input("Debug mode? (1=yes, 0=no): ")
        if choice == "1":
            return True
        if choice == "0":
            return False
        print("Enter 1 for yes or 0 for no.")

def create_cave(rows: int, cols: int) -> List[List[Room]]:
    # create a 2D list (grid) of empty Room objects
    return [[Room() for _ in range(cols)] for _ in range(rows)]

def place_event(event: Event, cave: List[List[Room]]) -> Tuple[int, int]:

    """Place an event into a random empty room. THis return the (row, col)
    where it was placed"""
    rows = len(cave)
    cols = len(cave[0])

    while True:
        r_index = random.randint(0, rows - 1)
        c_index = random.randint(0, cols - 1)
        room = cave[r_index][c_index]
        if not room.has_event():
            room.set_event(event)
            return r_index, c_index

def print_cave(
        cave: List[List[Room]],
        player_pos: Tuple[int, int],
        debug: bool,
) -> None:
    # display the cave grid in the terminal
    rows = len(cave)
    cols = len(cave[0])

    # each row of tooms is seperated by a horizontal line 
    print("-" * (cols * 3 + 1))
    for r_index in range(rows):
        line = "|"
        for c_index in range(cols):
            room = cave[r_index][c_index]
            # default: treat as an empty room
            symbol = " "

            # show event character only in debug mode
            if debug and room.has_event():
                event = room.get_event()
                name = type(event).__name__ if event is not None else ""
                symbol = {
                        "Wumpus": "W",
                        "BottomlessPit": "P",
                        "BatSwarm": "B",
                        "TreasureChest": "T",
                        "Arrow": "A",
                        "EscapeRope": "R",
                    }.get(name, " ")

            # if player is here, show '*' plus the event symbol (or space)
            if (r_index, c_index) == player_pos:
                line += f"*{symbol}|"
            else:
                line += f" {symbol}|"

        print(line)
        print("-" * (cols * 3 + 1))

def print_percepts(
        cave: List[List[Room]], 
        r_index: int, 
        c_index: int
) -> None:
    rows = len(cave)
    cols = len(cave[0])

    # up, down, left, right room positions
    directions = [
            (r_index - 1, c_index), # above
            (r_index + 1, c_index), # below
            (r_index, c_index - 1), # left
            (r_index, c_index + 1) # right
    ]


    # check each nearby room
    for adj_r_index, adj_c_index in directions:
        # make sure it's inside the cave
        if 0 <= adj_r_index < rows and 0 <= adj_c_index < cols:
            room = cave[adj_r_index][adj_c_index]
            # if the room has an event then print its percept message
            if room.has_event():
                event = room.get_event()
                if event is not None:
                    print(event.percept())


# reverse direction if player is confused by bats
def apply_confusion(direction: str) -> str:
    # confusion flips movement to the op;osite direction
    return {
            "w": "s",
            "s": "w",
            "a": "d",
            "d": "a"
            }.get(direction, direction)

# arrow firing logic
def fire_arrow(
        player: Player,
        cave: List[List[Room]], 
        player_pos: Tuple[int, int]
) -> bool:
    

    # p[layer must have arrows tro shoot
    if player.arrows <= 0:
        print("Out of arrows")
        return False

    direction = input(
        "What direction would you like to fire in? W/A/S/D: "
    ).lower()

    # validate firing direction
    if direction not in ["w", "a", "s", "d"]:
        print("Invalid direction")
        return False

    # reverse direction if bats confused the player
    if player.confused_turns > 0:
        direction = apply_confusion(direction)

    # remove one arrow from inventory
    player.arrows -= 1

    # how the arrow moves in rows and columns
    dr = {"w": -1, "s": 1, "a": 0, "d": 0}[direction]
    dc = {"w": 0, "s": 0, "a": -1, "d": 1}[direction]

    r_index, c_index = player_pos
    rows = len(cave)
    cols = len(cave[0])

    # arrow travels up to 3 rooms forward
    for _ in range(3):

        r_index += dr
        c_index += dc

        # stop arrow if it hits the edge
        if not (0 <= r_index < rows and 0 <= c_index < cols):
            break

        room = cave[r_index][c_index]

        # if arrow hits the Wumpus -> player wins
        if room.has_event() and isinstance(room.get_event(), Wumpus):
            print("The wumpus is defeated!")
            return True # game ends
    
    # arrow didn;t hit wumpus
    print("Your arrow misses...")
    return False


# Mo0ve the player one space iun the cave
def move_player(
        direction: str, 
        player_pos: Tuple[int, int], 
        cave: List[List[Room]], 
        player: Player
) -> Tuple[Tuple[int, int], bool]:
    



    rows = len(cave)
    cols = len(cave[0])

    r_index, c_index = player_pos

    # reverse direction if bat swarm effect is actiove
    if player.confused_turns > 0:
        direction = apply_confusion(direction)
        player.confused_turns -= 1

    # movement offsets
    dr = {"w": -1, "s": 1, "a": 0, "d": 0}.get(direction, 0)
    dc = {"w": 0, "s": 0, "a": -1, "d": 1}.get(direction, 0)

    # new target position
    new_r = r_index + dr
    new_c = c_index + dc

    # check if the move would go off the map
    if not (0 <= new_r < rows and 0 <= new_c < cols):
        print("Invalid direction!")
        return player_pos, False # did not move

    # return update position
    return (new_r, new_c), True




def main() -> None:
    # TODO Remove `pass` below, and write your main function here.
    # Remember to obey the course's style and design guide. Don't put too
    # much code here. Suggestion: Create a few more classes (e.g., a Game
    # class, a Player class, and maybe some others) to store variables about
    # the game, and put most of the game's logic in methods of those classes.

    # Ask for rows and columns with validation
    rows = get_int_input("Rows (4-20): ", 4, 20)
    cols = get_int_input("Cols (4-20): ", 4, 20)

    # ask for debug mode
    debug = get_debug_mode()

    # create the cave grid of room object

    cave = create_cave(rows, cols)

    # create a player 
    player = Player()

    # place all required evenbts into different empty rooms
    place_event(Wumpus(), cave)
    place_event(TreasureChest(), cave)

    for _ in range(2):
        place_event(BottomlessPit(), cave)

    for _ in range(2):
        place_event(BatSwarm(), cave)

    for _ in range(3):
        place_event(Arrow(), cave)

    # place escape rope and player in the same room
    rope_row, rope_col = place_event(EscapeRope(), cave)
    player_pos = (rope_row, rope_col)

    # print the cave once at the start

    print_cave(cave, player_pos, debug)
    
    # at the satrt of the game, print percepts if spawned by an event
    print_percepts(cave, player_pos[0], player_pos[1])

    # game loop
    while True:
        # ask the use what they want to do for their turn
        # WASD = move, F = fire arrow
        action = input(
            "What would you like to do? (W/A/S/D to move, F to fire an arrow): "
            ).lower()

        # Movement WASD
        if action in ["w", "a", "s", "d"]:
            # try to move, moved = False means the move wasn;t allowed
            new_pos, moved = move_player(action, player_pos, cave, player)

            if not moved:
                # this is an illegal move, so gotta restart the loop
                continue

            # update the player's position
            player_pos = new_pos

            # show percepts for events in nearby rooms
            print_percepts(cave, player_pos[0], player_pos[1])

            # check the current room for an event.
            room = cave[player_pos[0]][player_pos[1]]

            if room.has_event():
                # trigger the even'ts encounter behavior
                event = room.get_event()
                assert event is not None
                remove = event.encounter(player)

                # some events vanish after being triggers
                if remove:
                    room.set_event(None)

            # did the player die?
            if not player.is_alive:
                return

            # did the player escape wioth the treasure?
            if player.has_escaped:
                print("You escaped the cave!")
                return

            # redo the cave with ther new position
            print_cave(cave, player_pos, debug)


        # Firing an arrow (F)
        elif action == "f":

            # try to fire an arrow
            defeated = fire_arrow(player, cave, player_pos)

            # arrow hit the wumpus
            if defeated:
                return

            # show new percepts after firing
            print_percepts(cave, player_pos[0], player_pos[1])

            # redo cave
            print_cave(cave, player_pos, debug)


        # invalid action
        else:
            # input was not W/A/S/D/F
            print("Invalid action")


    
if __name__ == '__main__':
    main()
