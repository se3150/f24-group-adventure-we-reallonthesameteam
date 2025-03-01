from object import Object
from player import Player
import copy, random
import sys  # For exiting the game

class Cups(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
        self.cups = {'gold': "An ornate golden chalice, with shining gemstones all around the rim",
                     'bone': "A cup seemingly carved out of bone, with small thorns protruding from it",
                     'wood': "A simple, well made wooden cup",
                     'mug': "A mug with the phrase '#1 Boss' printed on it"}

    def use(self, player):
        print("Enter the name of a cup to drink from it\n"
              "Or type back to not drink from any\n"
              "The cups are:")
        for key in self.cups:
            print(key, ": ", self.cups[key], sep="")
        choice = input("> ").lower().strip()
        while choice not in self.cups and choice != 'back':
            print("Please enter " +', '.join("\"" + key + "\""  for key in self.cups) + ", or \"back\"")
            choice = input("> ")
        match choice:
            case 'wood':
                print("As the liquid slides down your throat, you feel a comfortably warm sensation spread through your body\n"
                      "and you feel stronger than you ever have before\n"
                      "You hear the skull to the side say:\n"
                      "\"Good job dude\"\n"
                      "(You have gained 150 health)\n"
                      "(You have gained 150 score)")
                player.health += 150
                player.score += 150
                self.visible = False
            case 'back':
                print("You back away from the cups")
            case _:
                print("As the liquid slides down your throat, you feel a burning sensation in your stomach, and you begin to age rapidly\n"
                      "You hear the skull to the side say:\n"
                      "\"You chose... poorly\"\n"
                      "(You have lost 70 health)")
                player.health -= 70
                # player.conditions.append("old")
                self.visible = False
                

class Skull(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        print("The skull begins to speak:\n"
              "\"The correct cup will bring you life, but the wrong one will bring death\"")


class Room:

    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "You enter this room, and see an exit to your north, and a ladder going up.\n"
            "All around the room, massive torches cast light to reveal a table in the center of the room.\n"
            "4 cups and a skull sit on the table, each cup filled halfway full."
        )
        # other room setup - add the lamp and set up the exits.
        cups = Cups("cups", "4 cups on a table in the center of the room", False, None, True)
        skull = Skull("skull", "A decrepit skull sitting on the table next to the cups", True, None, True)
        self.objects.append(cups)
        self.objects.append(skull)
        
        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["north", "down", "up"]

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
            
            elif command_base == 'use':
                if self.use(other_part, player) == 'dead':
                    return

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
                if obj.visible:
                    print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["up", "u"]:
            print("You climb up the ladder into the next room")
            return "up"
        if direction in ["north", "n"]:
            print("You exit north into the next room")
            return "north"
        if direction in ["down", "d"]:
            print("You climb down the ladder into the next room")
            return "down"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == ""):
            self.describe_room()
            return
        else:
            # Check if the object is in the room or in the player's inventory and print it description and status. You can use this code exactly.
            for obj in self.objects + player.inventory:
                if target == obj.name and obj.visible:
                    print(obj.description) 
                    if(obj.state != None): 
                        print(f"The {obj.name} is {obj.state}")                   
                    return
        
    def use(self, target, player):
        usable = []
        for obj in self.objects + player.inventory:
            if obj.visible and hasattr(obj, 'use'):
                usable.append(obj.name)
        
        if target not in usable:
            print("You can use:", usable)
            return

        for obj in self.objects + player.inventory:
            if target == obj.name and obj.visible:
                if target == 'cups':
                    obj.use(player)
                    if player.health < 0:
                        return 'dead'
                else:
                    obj.use()                 
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
        print("Available commands: move, go, look, get, take, use, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("It would be wise to use the skull before the cups.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")

if __name__ == "__main__":  # For testing
    room = Room()
    player = Player("me", 100, "", 5)
    room.enter(player)