from object import Object
from player import Player
import sys

class Crystal(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        if self.state == "off":
            self.state = "on"
            print(f"The {self.name} lights up brightly.")
        else:
            self.state = "off"
            print(f"The {self.name} turns off.")

class Room:
    objects = []

    def __init__(self):
        self.room_num = 24
        self.description = (
            "You are in a round room made of stone.\n"
            "There are old markings on the walls.\n"
            "In the middle of the room is a stone table.\n"
            "You can go west through a doorway or down some stairs.\n"
            "The stairs look dark and steep.\n"
        )
        
        crystal = Crystal("crystal", "A bright crystal that can glow in the dark.", True, "off", True)
        self.objects.append(crystal)
        
        self.exits = ["west", "down"]

    def enter(self, player):
        self.describe_room()

        while True:
            command = input("> ").lower
            ().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if command_base in ["move", "go"]:
                next = self.move(other_part)
                if(next != None):
                    return next
            
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
        if direction in ["west", "w"]:
            print("You walk through the doorway to the west.")
            return 23
        elif direction in ["down", "d"]:
            # check crystal before going down
            crystal_on = False
            for obj in self.objects:
                if obj.name == "crystal" and obj.state == "on":
                    crystal_on = True
                    break
            
            if crystal_on:
                print("The crystal's light helps you see the stairs as you go down.")
                return 25
            else:
                print("It's too dark to go down the stairs safely.")
                return None
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "table":
            print("The stone table looks like it could hold something.")
        elif target == "markings":
            print("The wall markings talk about needing light to find the way.")
        else:
            for obj in self.objects + player.inventory:
                if target == obj.name.lower():
                    print(obj.description)
                    if obj.state is not None:
                        print(f"The {obj.name} is {obj.state}")
                    return
            print(f"You don't see any {target} here.")

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
        #check if player has the item
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                item.use()
                return

        #check if item is in the room
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
        print("Try turning on the crystal before going down the stairs.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")