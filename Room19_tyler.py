from object import Object
from player import Player
import sys  # For exiting the game

import random

class Room:
    def __init__(self):
        self.room_num = 19
        self.description = (
            "You find yourself in a lavish room with gilded walls and sparkling chandeliers.\n"
            "The air smells of wealth and mischief. In the center of the room is a table with\n"
            "a sign reading 'Double or Nothing'. There's a slot to insert points and a large\n"
            "button that says 'PLAY'. There are exits to the south, down, and east."
        )
        self.exits = ["south, down, east"]
        self.objects = []

    def enter(self, player):
        # step 1 - Print the room description
        self.describe_room()
        print("Here are 10 points to start gambling with.")
        player.score += 10

        # step 2: command loop
        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if command_base in ["move", "go"]:
                next = self.move(other_part)
                if next:
                    return next

            elif command_base == "look":
                self.look(other_part, player)

            elif command_base in ["get", "take"]:
                self.get(other_part, player)

            elif command_base in ["drop", "put"]:
                self.drop(other_part, player)

            elif command_base in ["play", "gamble"]:
                self.gamble(player)

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
        if direction in ["south", "s"]:
            print("You leave the casino room through the southern door.")
            return "south"
        elif direction in ["down", "d"]:
            print("You leave the casino room through the downward door.")
            return "down"
        elif direction in ["east", "e"]:
            print("You leave the casino room through the eastern door.")
            return "east"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return
        if target in ["table", "sign"]:
            print("The sign reads: 'DOUBLE OR NOTHING. You can win it all!'")
        elif target in ["button", "play button"]:
            print("A big, shiny button labeled 'PLAY'. Everything could be yours")
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


    def gamble(self, player):
        if player.score <= 0:
            print("You don't have any points to gamble with! Earn some points before playing.")
            return

        print(f"You currently have {player.score} points.")
        points_to_gamble = int(input("How many points would you like to gamble? "))
        if points_to_gamble > player.score:
            print("You don't have that many points! You only have ", player.score)
            return
        player.score -= points_to_gamble
        result = random.choice(["win", "lose"])
        if result == "win":
            player.score += points_to_gamble*2
            print(f"Congratulations! You won double! You now have {player.score} points!")
        else:
            print("You lose! but you could win if you just gamble a little more")

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)
    
    def show_help(self):
        print("Available commands: move, go, play, gamble, look, get, take, drop, inventory, stats, quit, help")
    
    def show_hint(self):
        print("You could win it all if you just say play.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options.")