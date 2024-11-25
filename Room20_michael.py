from object import Object
from player import Player
import sys  # For exiting the game

class Creature(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        print(f"{self.name} doesn't respond to being used. Maybe you should try interacting with him some other way.")

class Room:
    objects = []

    def __init__(self):
        self.room_num = 1
        self.description = (
            "You find yourself in a large room with soft grass covering the ground.\n"
            "A small hill rises in the middle of the room, and standing atop it is a peculiar creature.\n"
            "He is wearing a name tag that says 'Hi, my name is: Dave'.\n"
            "Dave waves at you cheerfully, his mischievous grin indicating he's up to something.\n"
            "Exits lead 'up', 'down', and 'south', but they seem locked for now."
        )
        self.exits = ["up", "down", "south"]
        self.exits_locked = True

        # Add Dave to the room
        dave = Creature("Dave", "A small creature with a mischievous grin, standing atop the hill.", False, None, True)
        self.objects.append(dave)

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

            elif command_base == "high-five" and other_part.lower() == "dave":
                self.high_five_dave()

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
            else:
                self.unknown_command()

    def describe_room(self):
        print(self.description)
        for obj in self.objects:
            print(f"There is {obj.name} here.")

    def move(self, direction):
        if self.exits_locked:
            print("The exits are locked. You feel like Dave has something to do with this.")
            return None
        elif direction in self.exits:
            print(f"You move {direction}.")
            return direction
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if not target:
            self.describe_room()
            return

        for obj in self.objects + player.inventory:
            if obj.name.lower() == target.lower():
                print(obj.description)
                if obj.state:
                    print(f"The {obj.name} is {obj.state}")
                return

        print(f"You see no {target} here.")

    def get(self, item_name, player):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                if not obj.can_be_gotten:
                    print(f"You can't take the {obj.name}.")
                    return

                if player.has_item(obj.name):
                    print(f"You already have the {obj.name}.")
                    return

                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return

        print(f"There is no {item_name} here.")

    def high_five_dave(self):
        print("You walk up to Dave and raise your hand. Dave enthusiastically high-fives you!")
        print("You hear a click as the exits unlock.")
        self.exits_locked = False

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith("y"):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, high-five, inventory, stats, quit, help")

    def show_hint(self):
        print("Dave seems eager for a high-five. Try giving him one.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
