from object import Object
from player import Player
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function.
class Chalk(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        if self.state == "off":
            self.state = "on"
            print(f"You apply {self.name} to your hands.")
            print("Your grip feels incredibly strong!")
        else:
            self.state = "off"
            print(f"{self.name} is not being used now.")


class Room:
    def __init__(self):
        self.room_num = 0
        self.description = (
            "You come in from the west, to a dimly lit super tall room filled with cobwebs.\n"
            "You notice a bag filled with a white powdery substance that is nailed to the floor.\n"
            "There is a bright green light illuminating a huge wall that sits in front of you.\n"
            "You notice some protrusions in the wall with white marks around them that are similar to the substance in the bag.\n"
            "'I just want to see you win.' You hear a voice say.\n"
            "You immediately recall back to your youth and remember your friend Droxton.\n"
            "He used to be a rock climber before he was lost in 'The incident'.\n"
            "You smirk and say 'This is for you, Droxton. I know you'd love to see this.'\n"
        )
        self.objects = [
            Chalk(
                "chalk",
                "A bag filled with a white powdery substance that improves your grip strength.",
                False,
                "off",
                True,
            )
        ]
        self.exits = ["north", "east"]

    def enter(self, player):
        self.describe_room()

        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]
            other_part = parts[1] if len(parts) > 1 else ""

            if command_base in ["move", "go"]:
                next_room = self.move(other_part, player)
                if next_room:
                    return next_room
            elif command_base == "look":
                self.look(other_part, player)
            elif command_base in ["get", "take"]:
                self.get(other_part, player)
            elif command_base == "use":
                self.use_item(other_part, player)
            elif command_base == "quit":
                self.quit_game(player)
            elif command_base in ["help", "?"]:
                self.show_help()
            else:
                self.unknown_command()

    def move(self, direction, player):
        if direction in ["north", "n"] and player.has_item("chalk"):
            chalk = next((obj for obj in player.inventory if obj.name.lower() == "chalk"), None)
            if chalk and chalk.state == "on":
                print("You scale the wall with ease, thanks to the chalk. You reach the top platform!")
                return "next_room"  # Replace with actual next room logic
            else:
                print("The wall is too slippery to climb without chalk!")
                return None
        elif direction in ["east", "e"]:
            print("You exit the room to the east.")
            return "east_room"  # Replace with actual next room logic
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if not target:
            self.describe_room()
        elif target == "wall":
            print(
                "The wall is tall and has firm holds, but it's too slippery without some grip assistance. Perhaps the chalk could help."
            )
        else:
            for obj in self.objects + player.inventory:
                if target == obj.name.lower():
                    print(obj.description)
                    if obj.state:
                        print(f"The {obj.name} is {obj.state}")
                    return
            print(f"You don't see a {target} here.")

    def get(self, item_name, player):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                if not obj.can_be_gotten:
                    print(f"The {obj.name} cannot be taken.")
                    return
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return
        print(f"There is no {item_name} here or you can't get it.")

    def use_item(self, item_name, player):
        for obj in player.inventory:
            if obj.name.lower() == item_name.lower():
                obj.use()
                return
        print(f"You don't have {item_name} in your inventory.")

    def describe_room(self):
        print(self.description)
        for obj in self.objects:
            print(f"There is a {obj.name} here.")

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith("y"):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, use, quit, help")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options.")