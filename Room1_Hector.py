from object import Object
from player import Player
import sys

class RunningShoes(object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        if self.state == "off":
            self.state = "on"
            print(f"{self.name} is now on.")
        else:
            self.state = "off"
            print(f"{self.name} is now off.")
            ("running shows", "some nice golden running shoes", True, "off", True)

class Room:
    objects = []
    shoes = RunningShoes("running shoes", "Golden Plated Running Shoes", True, "off", True)
    object.append(shoes)
    def __init__(self):
        self.room_num = 1
        self.description = "Welcome, brave traveler, to Room 1! \n AHAHAHA!/n This is no ordinary room—it is a challenge that will test your strength, wit, and courage!\nBefore you lies a daunting obstacle course,\nsprawling across rugged terrain with treacherous surprises at every turn.\nBut behold!\nAt the very peak of this course stands a golden box, glistening with mystery,and beside it—a bold, red button!\nWill you rise to the occasion? Let the trials begin!"
        self.exists = ["south", "down"]
    
    def enter(self, player):
        print(self.description)
        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            #Do the command - You should make helper functions for each of these in your room as well.
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
            elif command_base == "run":
                self.run()
            else:
                self.unknown_command()




    # Helper functions
    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction == "down":
            print("You decided to be a coward and exit the room")
            return "down"
        elif direction == "south":
            print("You decided to be a coward and exit the room")
            return "down"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "announcer":
            print("Upon closer inspection, the Announcer seems to be trying to give you a gift")
        else:
            # Check if the object is in the room or in the player's inventory and print it description and status. You can use this code exactly.
            for obj in self.objects + player.inventory:
                if target == obj.name:
                    print(obj.description) 
                    if(obj.state != None): 
                        print(f"The {obj.name} is {obj.state}")                   
                    return
        
    # this code could also probably be used verbatim
    def get(self, item_name, player):
        # Check if the item is in the room's objects list
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():  # Case-insensitive comparison
                if not obj.can_be_gotten:
                    print(f"The {obj.name} cannot be taken.")
                    return

                # Check if the player already has the item in their inventory
                if player.has_item(obj.name):
                    print(f"You already have the {obj.name}.")
                    return
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return
        print(f"There is no {item_name} here or you can't get it.")
    
        def drop(self, item_name, player):
            # Check if the item is in the player's inventory
            for item in player.inventory:
                if item.name.lower() == item_name.lower():  # Case-insensitive comparison
                    player.inventory.remove(item)
                    self.objects.append(item)
                    print(f"You drop the {item.name} on the ground.")
                    return 

            # If the item was not found in the player's inventory
            print(f"You can't drop {item_name}. You don't have that.")

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help, run")

    def show_hint(self):
        print("This is the starting room. You probably ought to get the lamp and go down the well.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
    def run(self):
        print("you ran the course and died")
   