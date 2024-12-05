from object import Object
from player import Player
import sys

class Creature(Object):
    def use(self,player):
        print("In the corner you sense something stairing at you \n"
              "You notice a tall slender \033[3mCreature\033[0m.\n"
              "It lunges at you with its huge claws \n")
        player.health = 0
        player.condition = "dead"
        print(f"Game Over! {player.name} has been killed.")
        return "You are dead."        

class Candle(Object):  
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self): 
        if "Lighter" in object:
            if self.state == "off":
                self.state = "Lit"
                print(f"{self.name} is now Lit..")
            else:
                self.state = "off"
                print(f"{self.name} is now off.")
                ("Candle", "A plain white candle, Smells like nothing.", True, "off", True)
        else:
            print(f"{self.name} can't be lit without Lighter.")
            
class Lighter(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        if self.state == "off":
            self.state = "on"
            print(f"{self.name} is now on.")
        else:
            self.state = "off"
            print(f"{self.name} is now off.")
    
class HealthPotion(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self,player):
        if self.state == "closed":
            self.state = "open"
            print(f"{player.name} is healed to max health.")
            if player.health == 100:
                print(f"{player.name} health is already max")
            else:
                player.health = 100
                player.inventory.remove(self)
                print(f"{self.name} has been removed from {player.name}'s inventory.{player.name} is now max health")
        else:
            self.state = "closed"
            print(f"{self.name} is closed.")

class Chest(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)
        self.contains = [
            HealthPotion("health potion", "A clear glass bulb shaped bottle with red glowing liquid inside", True, "closed", True)
        ]

    def use(self, player):
        if self.state == "closed":
            print(f"{self.name} is closed. This can be opened with a key.")
        elif "key" in player.inventory:
            self.state = "open"
            print(f"{player.name} has now opened the chest.\n"
                  "Inside you find a health potion that has been added to your inventory.")
            player.inventory.append(self.contains.pop())  # Add the health potion to the player's inventory
            
class Key(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)
        
    def use(self):
        print(f"{self.name} is in your inventory, but it doesn't seem to do anything right now.")
    
class Room:
    
    object = [
        Chest("chest", "A large brown chest with a big lock pad on the front", False, "closed", True),
        HealthPotion("health potion", "A clear glass bulb shapped bottle with red glowing liquid inside", True, "closed", True),
        Lighter("lighter","A small steel lighter with a gray lid on the top", True, "off", True),
        Candle("Candle", "A plain White wax candle with no scent. Looks used, but can provide light temporarily", True, "off", True),
        Key("key","A brown old key", True,"none",True)
    ]
    def __init__(self):
        self.room_num = 9
        self.description = (
            "You push the heavy door open. A cool wind hitting your face,\n"
            "You look at your surroundings trying to see if you can spot anything.\n"
            "The room's too dark for you to see anything,\n"
            "The air feels heavy, thick with an unsettling stillness,\n"
            "You strain your eyes, but the darkness seems to swallow every detail.\n"
            "A faint noise echoes from the shadows, but you can't tell if it's just your imagination.\n"
        )

        self.exits = ["west"]
    
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
        
        
    def describe_room(self):
        print(self.description)
        if self.object:
            for obj in self.object:
                if obj.visible:
                    print(f"There is a {obj.name} here.")
                    
    def move(self, direction, player):
        if direction in ["west", "w"]:
                print("You walk through the doorway to the west.")
                print("You notice a key hanging on the wall.")
                
                key = next((obj for obj in self.object if isinstance(obj, Object) and obj.name == "key"), None)
                if key and key.can_be_gotten:
                    player.inventory.append(key)
                    print(f"{player.name} has picked up the {key.name}. It has been added to your inventory.")
                    self.object.remove(key) 
                else:
                    print("There is no key to pick up.")

                return None  

        elif direction in ["east", "e"]:
            print("You see a door leading back to Room 9.")
            print("Next to the door, there’s a chest.")
            chest = next((obj for obj in self.object if isinstance(obj, Chest)), None)
            if chest:
                chest.use(player)
            return 9  
        elif direction in ["north", "n"]:
            print("You see a door leading to Room 7. You walk through it.")
            return 7 
        elif direction in ["south", "s"]:
            print("You move to the left side of the room.")
            creature = next((obj for obj in self.object if isinstance(obj, Creature)), None)
            if creature:
                print("The creature attacks!")
                creature.use(player)
                return None if player.condition == "dead" else self.id 
            else:
                print("The area is clear.")
            return None
        else:
            print("You can't go that way.")
            return None
            
    def get(self, item_name, player):
        item = next((obj for obj in self.object if obj.name.lower() == item_name), None)
        if item and item.can_be_gotten:
            if item_name == "health potion":
                print(f"You pick up the {item.name}.")
            player.inventory.append(item)
            self.object.remove(item)
            print(f"{item.name} has been added to your inventory.")
        else:
            print(f"There is no {item_name} here or it cannot be picked up.")
            
    def drop(self, item_name, player):
        item = next((obj for obj in player.inventory if obj.name.lower() == item_name), None)
        if item:
            player.inventory.remove(item)
            self.object.append(item)
            print(f"{item.name} has been dropped back in the room.")
        else:
            print(f"You don't have a {item_name} in your inventory.")

    def show_inventory(self, player):
        if player.inventory:
            print(f"{player.name}'s Inventory:")
            for item in player.inventory:
                print(f"- {item.name}")
        else:
            print(f"{player.name} has no items in their inventory.")
    
    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()
        
    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("This is the starting room. You probably ought to get the lamp and go down the well.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
    
    #quiting game
    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)
