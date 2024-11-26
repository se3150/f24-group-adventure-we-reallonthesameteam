from object import Object 
from player import Player 
import sys 

class Room:

    objects = []

    def __init__(self) -> None:
        self.room_num = 21
        self.description = (
            "You walk into a large dark room where you hear water flowing. \n"
             "Walking in further you see that there is a fountain with very magical water flowing out of it."
        )
        self.fountain_used = False
        #Other room setup - such as adding items and the exits

        self.exits = ["up", "down", "left"]

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

            print(f"This is the command_base: {command_base}")

            #Do the command - Make helper function
            if command_base in ["move", "go"]:
                next = self.move(other_part)
                if (next != None):
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

            elif command_base == "drink":
                self.drink_from_fountain(player)
            
            else:
                self.unknown_command()


    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["down", "d"]:
            print("You leave the fountain and go down.")
            return "down"
        elif direction in ["left", "east", "l"]:
            print("You leave the fountain and go left.")
            return "left"
        elif direction in ["up", "north", "u"]:
            print("You leave the fountain and go up.")
            return "up"
        else:
            print("You can't go that way.")
            return None
    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "placeholder":
            print("Placeholder")
        else:
            # check if the object is in the room or players inventory
            for obj in self.objects + player.inventory:
                if target == obj.name:
                    print(obj.description)
                    if(obj.state != None):
                        print(f"The {obj.name} is {obj.state}")
                    return 
    
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
                print(f"You take the {obj.name} and add it to your inventory")
                return 
            
        print(f"There is no {item_name} here or you can't get it.")
        
    def drop(self, item_name, player):
        for item in player.inventory:
            if item.name.lower() == item_name.lower():
                player.inventory.remove(item)
                self.objects.append(item)
                print(f"You drop the {item.name} on the ground.")
                return  
            
            print(f"You can't drop {item.name}. You don't have that.")

    def show_inventory(self, player):
        player.show_inventory()
       
    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().strip():
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Avaliable commands: move, go, look, get, take, drop, inventory, stats, quit, help")
        
    def show_hint(self):
        print("The liquid in the fountain seems like it might be worth the risk trying to drink from.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' or 'hint' for a clue.")

    def drink_from_fountain(self, player):
        if not self.fountain_used:
            print(f"You have drank from the fountain and your health has been restored! \n The water flowing out has seemed to lose its magical healing properties.")
            player.health = 100
            self.fountain_used = True
        else:
            print("You already drank from the fountain, it just tastes like normal water now.")
        


