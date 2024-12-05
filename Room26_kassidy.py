from object import Object
from player import Player
import sys 

from object import Object

class Key(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self, player): 
        return

class Quilt(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        return

class Chest(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return
    
class Lock(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return

class Hutch(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return

class Dog(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return

class Door(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return

class CannedFood(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)
    
    def use(self):
        return

class Room:
    def __init__(self):
        self.room_num = 26
        self.dog_trust_earned = False
        self.description = (
            "You enter a dimly lit room with creaky wooden floors.\n"
            "Cobwebs hang from all corners of the ceiling. A row of broken bay windows dominate the left side of the room, letting in a chilly draft.\n"
            "Against the wall beneath the shattered windows lies the tattered remains of an old couch. A thick QUILT is draped over one arm of the couch.\n"
            "In the center of the room is an ornate CHEST. A heavy, rusted LOCK secures the lid.\n"
            "Opposite the couch stands a tall HUTCH, cracked and coated in a layer of dust and its doors firmly closed.\n"
            "At the far end of the room, partially obscured by shadows, is a DOG. Frightened and trembling, the dog cowers beneath a small table.\n"
            "The dog growls lowly as a warning to not approach.\n"
            "Just within reach, beneath the table and dangerously close to the dog, you notice a large, rusty KEY lying on the floor.\n"
            "Behind the dog and the table stands a DOOR, a possible escape route but unreachable for now.\n"
        )
        self.objects = [
            Key("key", "A large rusty key.", True, "on the floor next to the dog", True),
            Quilt("quilt", "A thick, crochet quilt.", True, "on couch", True),
            Chest("chest", "An ancient ornate chest.", False, "locked", True),
            Lock("lock", "A large, heavy lock securing the chest.", False, "locked", True),
            Hutch("hutch", "A tall, wooden hutch with closed doors.", False, "shut", True),
            Dog("dog", "A medium-sized, brown, skinny dog.", False, "scared, hungry, and cold", True),
            Door("door", "A wooden door at the back of the room.", False, "blocked", True),
        ]
        self.hint_message = "The dog won't let you near the key or the door. Try checking the dog's state to see how you can help"
        self.exits = ["down", "east"]

    def enter(self, player):
        print("\n--- Room 26 ---")
        print(self.description)

        while True:
            command = input("\nWhat do you want to do? ").strip().lower()

            if command in ["look"]:
                print(self.description)
                if self.objects:
                    print("You see the following items in the room:")
                    for obj in self.objects:
                        print(f"- {obj.name}: {obj.description} State: {obj.state}")
            elif command in ["inventory"]:
                print("You are carrying:")
                for item in player.inventory:
                    print(f"- {item.name}: {item.description}")
            elif command.startswith("get") or command.startswith("take"):
                item_name = command.split(maxsplit=1)[1] if len(command.split()) > 1 else ""
                if item_name in ["key"]:
                    if self.dog_trust_earned == False:
                        print("You can't get the key because the dog does not trust you yet")
                    else:
                        key = self.get_object_by_name("key")
                        key.state = "in your inventory"
                        self.get_item(item_name, player)
                else:
                    self.get_item(item_name, player)
            elif command.startswith("drop"):
                item_name = command.split(maxsplit=1)[1] if len(command.split()) > 1 else ""
                self.drop_item(item_name, player)
            elif command in ["go east", "move east"]:
                print("You move east.")
                return "east"
            elif command in ["go door", "move door"]:
                #can only do this if doors state is open 
                door = self.get_object_by_name("door")
                if door.state == "blocked":
                    print("The door is blocked, you can't leave")
                else:
                    print("You go through the door..")
                    return "down"
            elif command in ["stats"]:
                print("Player Stats:")
                print(f"Health: {player.health}")
                print(f"Score: {player.score}")
            elif command in ["hint"]:
                print(self.hint_message)
            elif command in ["help", "?"]:
                self.display_help()
            elif command in ["quit"]:
                confirm = input("Are you sure? (y/n) ").strip().lower()
                if confirm == "y":
                    print("Thanks for playing!")
                    print(f"Final Stats: Health: {player.health}, Score: {player.score}")
                    exit()
            elif command in ["befriend dog"]:
                self.befriend_dog(player)
            elif command in ["open chest"]:
                self.open_chest(player)
            elif command in ["open hutch"]:
                self.open_hutch(player)
            else:
                print("I don't understand that command. Try 'help' for a list of commands.")

    def befriend_dog(self, player):
        print("\nThe dog looks at you nervously. How will you approach it?\n")
        if self.check_inventory(player, ["food", "quilt"]):
            approach = input("1. Offer food\n2. Offer quilt\n> ").strip()

            if approach == "1" and any(item.name == "food" for item in player.inventory):
                food = next(item for item in player.inventory if item.name == "food")
                player.inventory.remove(food)
                print("You offer the dog some food. It eats happily and wags its tail!\n")
                self.dog_trust_earned = True
                dog = self.get_object_by_name("dog")
                dog.state = "happy and fed"
                door = self.get_object_by_name("door")
                door.state = "accessible"
                food.state = "eaten by dog"
                print("You can get the key now.\n")
            elif approach == "2" and any(item.name == "quilt" for item in player.inventory):
                quilt = next(item for item in player.inventory if item.name == "quilt")
                player.inventory.remove(quilt)
                print("You lay the quilt on the ground in front of the dog and pat it gently.\n")
                print("The dog carefully approaches the quilt and lays down.\n")
                self.dog_trust_earned = True
                dog = self.get_object_by_name("dog")
                dog.state = "happy and warm"
                door = self.get_object_by_name("door")
                door.state = "accessible"
                quilt.state = "warming the dog"
                print("You can get the key now.\n")
            else:
                print("That's not an option, try again.")
        else:
            player.health =- 10
            print("You have nothing to offer the dog. Go look around the room to find something to earn his trust.\n")
            print("-10 health\n")

    def open_chest(self, player):
        #use the key to change the locks state to unlocked, then the chests state to open 
        if any(item.name == "key" for item in player.inventory):
            chest = self.get_object_by_name("chest")
            lock = self.get_object_by_name("lock")
            chest.state = "opened"
            lock.state = "unlocked"
            print("You use the key to unlock the chest. Inside, you find a note with a strange ISBN number.")
            print("978-1-119293-32-3")
            print("The note has been added to your inventory.")
            player.inventory.append(Object("note", "A note with an ISBN number: 978-1-119293-32-3", True, "Old and tattered", True))
            player.score += 10
        else:
            print("The chest is locked. You need a key to open it.")

    def open_hutch(self, player):
        food = self.get_object_by_name("food")
        hutch = self.get_object_by_name("hutch")
        hutch.state = "open"
        if food not in self.objects:
            self.objects.append(
                CannedFood("food", "A can of dog food.", True, "inside the hutch", True)
            )
            print("You open the hutch and inside you find a can of dog food.\n")
        else:
            print("The hutch is empty")
    
    def check_inventory(self, player, items_needed):
        return any(item.name in items_needed for item in player.inventory)

    def get_object_by_name(self, item_name):
        for obj in self.objects:
            if obj.name == item_name:
                return obj
        return None

    def get_item(self, item_name, player):
        for obj in self.objects:
            if obj.name == item_name:
                if obj.can_be_gotten:
                    self.objects.remove(obj)
                    player.inventory.append(obj)
                    if item_name == "quilt":
                        obj.state = "in inventory"
                    if item_name == "food":
                        obj.state = "in inventory"
                    print(f"You pick up the {obj.name}.")
                else:
                    print(f"The {obj.name} cannot be picked up.")
                return
        print(f"There is no {item_name} here.")

    def drop_item(self, item_name, player):
        for obj in player.inventory:
            if obj.name == item_name:
                player.inventory.remove(obj)
                self.objects.append(obj)
                print(f"You drop the {obj.name}.")
                return
        print(f"You are not carrying a {item_name}.")

    def display_help(self):
        print("\nAvailable commands:")
        print("go <direction>, move <direction> - Move to a new room.")
        print("look - Look at the room or an item.")
        print("get <item>, take <item> - Pick up an item.")
        print("drop <item> - Drop an item.")
        print("inventory - Check your inventory.")
        print("stats - View your player stats.")
        print("hint - Get a hint for this room.")
        print("befriend dog - Try to befriend the dog.")
        print("open chest - Attempt to open the chest.")
        print("open hutch - See what is inside the hutch.")
        print("quit - Quit the game.")
