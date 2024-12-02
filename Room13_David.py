from object import Object
from player import Player
import sys

class Crow(Object):
    def use(self, player):
        if player.inventory:
            lost_item = player.inventory.pop(0)
            print(f"The crow screeches and you lose the {lost_item.name} from your inventory.")
        else:
            print("The crow screeches but you have nothing to lose.")

class Chucky(Object):
    def use(self, player):
        print("You touch Chucky, and he suddenly springs to life with a menacing grin. You scream in terror as he slashes at you, killing you instantly.")
        player.health = 0
        player.condition = "dead"
        print(f"Game Over! {player.name} has perished.")
        return "You are dead."

class Clown(Object):
    def use(self, player):
        print("The clown's smile widens unnaturally. It whispers, 'The only way out is through the well.'")

class Grave(Object):
    def use(self, player):
        print("You examine the grave, and a chilling breeze sweeps over you. You feel weaker.")
        player.health -= 10
        if player.health <= 0:
            player.health = 0
        print(f"{player.name}'s health is now {player.health}.")

class Room:
    def __init__(self):
        self.objects = [Crow("Crow", "A menacing crow with sharp eyes.", True, None, True),
                        Chucky("Chucky Doll", "A creepy Chucky doll with a knife.", True, None, True),
                        Clown("Clown", "A terrifying clown with a crooked smile.", True, None, True),
                        Grave("Grave", "A freshly dug grave, the soil still loose.", False, None, True)]
        self.description = (
            "You enter a dark, cursed room. The air is cold and still. A crow caws ominously in the corner, "
            "and you feel a sinister presence around you. A Chucky doll stands eerily still in the center of the room, "
            "and a clown watches you with a grin that seems too wide to be real. A grave rests in one corner of the room, "
            "its earth freshly disturbed."
        )
        self.exits = ["east", "down"]

    def check_health(self, player):
        if player.health <= 0:
            print(f"{player.name}, you have died. Game Over!")
            sys.exit(0)

    def describe(self, item=None, player=None):
        if item:
            for obj in self.objects:
                if obj.name.lower() == item.lower():
                    print(f"Item: {obj.name} - {obj.description}")
                    return
            return "You don't see that here."
        else:
            print(self.description)
            for obj in self.objects:
                print(f"There is a {obj.name} here.")
            return

    def move(self, direction):
        print(f"You try to move {direction}, but the path is blocked. There is no way out.")
        return

    def help(self):
        print("""
Available Commands:
- move <direction> / go <direction>: Move in a specified direction (north, south, east, west, etc.)
- look <item>: Look at an item or get the room description (if no item specified).
- use <item>: Interact with an item in the room (e.g., use the crow or Chucky doll).
- inventory: Show the player's current inventory.
- stats: Show the player's stats (health, condition, etc.).
- quit: Attempt to leave the room (you cannot leave this room).
- help: Display this list of available commands.
        """)

    def enter(self, player):
        self.describe()

        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if command_base in ["move", "go"]:
                self.move(other_part)
            elif command_base == "look":
                self.describe(other_part, player)
            elif command_base in ["get", "take"]:
                print("You can't take anything in this room.")
            elif command_base == "use":
                for obj in self.objects:
                    if obj.name.lower() == other_part.lower():
                        obj.use(player)
                        break
                else:
                    print("That item is not here.")
            elif command_base == "inventory":
                player.show_inventory()
            elif command_base == "stats":
                player.print_stats()
            elif command_base == "quit":
                print("You cannot escape this room. There is no escape.")
                return
            elif command_base == "help":
                self.help()
            else:
                print("Unknown command.")
            
            self.check_health(player)


