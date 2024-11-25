from object import Object
from player import Player
import sys  # For exiting the game 

class Lever(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        print("You pull the lever. It moves with a creaking sound.")

class Room:

    def __init__(self):
        self.room_num = 3
        
        self.description = (
            "You find yourself in a dimly lit chamber. The walls are covered with ancient inscriptions.\n"
            "There is a heavy door to the north and a narrow passage to the south.\n"
            "Above you, there is a hatch leading upward, but it is sealed shut.\n"
            "There is a lever on the wall.\n"
        )
        
        self.exits = ["north", "south"]
        self.up_exit_unlocked = False
        
        self.objects = []
        lever = Lever("lever", "An old rusty lever fixed to the wall.", False, None, True)
        self.objects.append(lever)

    def enter(self, player):

        self.describe_room()

        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if command_base in ["move", "go"]:
                next_room = self.move(other_part)
                if next_room is not None:
                    return next_room

            elif command_base == "look":
                self.look(other_part, player)

            elif command_base in ["get", "take"]:
                self.get(other_part, player)

            elif command_base in ["drop", "put"]:
                self.drop(other_part, player)

            elif command_base == "inventory":
                self.show_inventory(player)

            elif command_base == "stats":
                self.show_stats(player)

            elif command_base == "quit":
                self.quit_game(player)

            elif command_base in ["help", "?"]:
                self.show_help()

            elif command_base == "hint":
                self.show_hint()

            elif command_base in ["pull", "use"]:
                self.use(other_part, player)

            else:
                self.unknown_command()

    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")
        exits_str = ", ".join(self.exits)
        print(f"Exits: {exits_str}")

    def move(self, direction):
        if direction in ["north", "n"]:
            print("You head through the heavy door to the north.")
            return "north"
        elif direction in ["south", "s"]:
            print("You walk down the narrow passage to the south.")
            return "south"
        elif direction in ["up", "u"]:
            if self.up_exit_unlocked:
                print("You climb up through the opened hatch.")
                return "up"
            else:
                print("The hatch above is sealed shut. Perhaps there's a way to open it.")
                return None
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if target == "":
            self.describe_room()
            return
        elif target == "lever":
            print("An old rusty lever fixed to the wall. It seems to be connected to some mechanism.")
        else:
            for obj in self.objects + player.inventory:
                if target == obj.name.lower():
                    print(obj.description)
                    if obj.state is not None:
                        print(f"The {obj.name} is {obj.state}")
                    return
            print(f"You don't see a {target} here.")

    def get(self, item_name, player):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                if not obj.can_be_gotten:
                    print(f"The {obj.name} cannot be taken.")
                    return
                if player.has_item(obj.name):
                    print(f"You already have the {obj.name}.")
                    return
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return
        print(f"There is no {item_name} here or you can't get it.")

    def drop(self, item_name, player):
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                player.inventory.remove(item)
                self.objects.append(item)
                print(f"You drop the {item.name} on the ground.")
                return
        print(f"You can't drop {item_name}. You don't have that.")

    def use(self, item_name, player):
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                item.use()
                return
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                obj.use()
                if isinstance(obj, Lever):
                    if not self.up_exit_unlocked:
                        print("You hear a grinding noise as the hatch above slowly opens.")
                        self.up_exit_unlocked = True
                        if "up" not in self.exits:
                            self.exits.append("up")
                        player.score += 10
                    else:
                        print("The hatch is already open.")
                return
        print(f"You can't use {item_name} here.")

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help, hint, pull, use")

    def show_hint(self):
        print("Maybe interacting with the lever will open a new path.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")