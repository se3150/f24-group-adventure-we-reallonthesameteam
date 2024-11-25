from object import Object
from player import Player
import random
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function. 
    
class d_(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self, player):
        value = random.randint(1, 100)
        if value % 2 != 0:  
            print(f'You rolled {value}. Your health has increased!')
            player.health += value
        else:  
            print(f'You rolled {value}. Your health has decreased!')
            player.health -= value

        
        print(f'Your current health is now {player.health}.')
        


class Room:

    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "You walk down a hall an it gets narrow.\n"
            "You now are having to crawl.\n"
            ".\n"
            "You now unable to turn around and hearing a ranging river.\n"
            ".\n"
            ".\n"
            "As you near the end of the tunnel and enter into a narrow chasm.\n"
            "Walking to the edge you see a narrow bridge with a ticket booth in front.\n"
            
            
        )
        # other room setup - add the lamp and set up the exits.
        dice = d_("Dice", "A 20 sided die that is glowing is ", True, "off", True)
        self.objects.append(dice)
        
        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = []

        



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
            if command_base in ["ticket-booth"]:
                self.move(player)
                
            
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

    def move(self, direction, player):
        if direction in ["ticket-booth"]:
            print("You approach the ticket booth.")
            print("A sign reads: 'ROLL TO PASS. SUCCESSFUL ROLL REQUIRED.'")

            # Has the dice
            if not player.has_item("Dice"):
                print("You need the dice to proceed.")
                return

            # Ask the player if they want to roll the dice
            while True:
                choice = input("Do you want to roll the dice? (yes/no): ").lower().strip()
                if choice == "yes":
                    dice = next(obj for obj in player.inventory if obj.name.lower() == "dice")
                    dice.use(player)

                    print("The gate opens, and new paths are revealed!")
                    self.add_exits() 
                    return
                    
                elif choice == "no":
                    print("You decide not to roll the dice for now.")
                    return
                
                else:
                    print("Please answer 'yes' or 'no'.")

        else:
            print("You can't go that way.")
            return None
    
    def add_exits(self):
        if "west" not in self.exits:
            self.exits.append("west")
        if "south" not in self.exits:
            self.exits.append("south")
        print(f"New exits available: {', '.join(self.exits)}")

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "ticket-booth":
            print("You see a sign, 'ROLL TO PASS'. You also see dice that are on the ground.")
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
        print("Available commands: ticket-booth, look, get, take, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("You should approach the ticket-booth.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")