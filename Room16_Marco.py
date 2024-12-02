from object import Object
from player import Player
import sys

class OxygenRecycler(Object):
    def __init__(self, name, description, can_be_used, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_used, state, visible)

    def use(self):
        if self.state == "offline":
            self.state = "online"
            print("Oxygen Recycler activated. Life support systems stabilizing.")
        else:
            self.state = "offline"
            print("Oxygen Recycler shutdown. Warning: Oxygen levels decreasing!")


class Room:
    objects = []

    def __init__(self):
        self.room_num = 1
        self.description = (
            "You awaken in a damaged space station, emergency lights flickering.\n"
            "Alarms blare intermittently. The hull shows signs of micro-meteorite damage.\n"
            "A critical oxygen recycler sits in the corner, its status uncertain.\n"
            "A single airlock leads to the next section of the station.\n"
        )
        
        recycler = OxygenRecycler("Oxygen Recycler", "A complex machine maintaining life support systems", True, "offline", True)
        self.objects.append(recycler)
        
        self.exits = ["east","south"]

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

            elif command_base == "use":
                self.use(other_part, player)

            else:
                self.unknown_command()

    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                if obj.visible:
                    print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["right","r","east","e","south","s","down","d"]:
            print("You carefully navigate through the damaged airlock...")
            return 2  # Example: Transition to Room 2
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if not target:
            self.describe_room()
            return

        if target == "damage":
            print("The hull damage looks severe but repairable with the right tools.")
        else:
            for obj in self.objects + player.inventory:
                if target == obj.name.lower():
                    print(obj.description)
                    if obj.state is not None:
                        print(f"The {obj.name} is currently {obj.state}.")
                    return
            print(f"You don't see any {target} here.")

    def get(self, item_name, player):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                if not obj.can_be_used:
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
                print(f"You drop the {item.name} on the floor.")
                return 

        print(f"You can't drop {item_name}. You don't have that.")

    def use(self, item_name, player):
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                item.use()
                return

        for item in self.objects:
            if item.name.lower() == item_name.lower():
                item.use()
                return

        print(f"There is no {item_name} here or in your inventory to use.")

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, use, inventory, stats, quit, help")

    def show_hint(self):
        print("Try activating the Oxygen Recycler to stabilize life support systems.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
