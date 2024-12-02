from object import Object
from player import Player
import sys  # For exiting the game



class Dog(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

class Doll(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)


class Room:

    objects = []

    def __init__(self):
        self.room_num = 9
        self.description = (
            "You enter a room with muted pink walls and a big bed in the middle of the room.\n"
            "After more than one glance around the room you notice a door to the east and one to the south.\n"
            "In the bed there is a stuffed dog plushy and a glass doll laying on the bed.\n"
            "The floor is wet and cold but you don't see water at your feet. \n"
            
        )
        # other room setup - add the lamp and set up the exits.
        Doggy = Dog("Dog Plushy", "A small stuffed dog that is damp on the ears and tail.", True, "off", True)
        self.objects.append(Doggy)
        Dolly = Doll("Glass Doll", "A Medium sized glass doll with a crack down the center of her face.", True, "off", True)
        self.objects.append(Dolly)

        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["east", "south"]



    def enter(self, player):

        # step 1 - Print the room description
        self.describe_room()

        # step 2 - make your own command loop - watch carefully about how to parse commands:
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
            else:
                self.unknown_command()




    # Helper functions
    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["east", "e", "left", "l"]:
            print("You enter a door that looks like it is dripping wet but you can't tell what the liquid is.")
            return "east"
        elif direction in ["south", "s", "down", "d"]:
            print("You walk towards a red door with paint that is chipping along the sides. The door slowly opens as you walk towards it.")
            return "south"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "Doll":
            print("Upon closer inspection, the crack is leaking black liquid and she looks like she is about to cry.")
        if target == "Dog":
            print("Once you pick up the stuffed dog you realize the whole plush is dripping. The dog doesn't look like it is wet but clearly it is. ")
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

                # Add the object to the player's inventory and remove it from the room
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return

        # If the item was not found in the room
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
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("This room is nothing amazing. maybe go through a door?")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")