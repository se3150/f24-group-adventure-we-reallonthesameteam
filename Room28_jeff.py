from object import Object
from player import Player

class Room:

    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "You are now in a long dark tunnel. A fresh breeze blows from somewhere, giving you the indication that you might be close to the exit."
        )

        self.exits = []

    def enter(self, player):

        lamp = None
        print(self.description)
        for item in player.inventory:
            if item.name == "Lamp":
                lamp = item
                break
            if item.name == "crystal":
                lamp = item
                break
            if "lighter" in item.name:
                lamp = item
        
        if lamp == None:
            print("you have nothing in your inventory to make light.")
            print("You try to feel your way forward, but the slope of the cave is to steep and you slide down uncontrollably!")
            print("You fall off the edge into a pit and die!")
            player.health = 0
            return "end"
        
        while lamp.state !="on":
            print("you will need some light in order to proceed.")
            cmd = input(">")
            if "go" in cmd:
                print(f"without your {lamp.name} on, you feel your way forward, and begin to slide uncontrollably!")
                print("You fall off the edge into a pit and die!")
                player.health = 0
                return "end"
            if "use" in cmd and ("lamp" in cmd or "crystal" in cmd): 
                lamp.state = "on"

        print(f"with your {lamp.name} on, you can see that the tunnel floor falls steeply away to the left. You surely would have died")
        print("had you tried to move through this section without light.")
        print("There is a tiny ledge to the right that you can scramble on to pass the steep hole to the left.")
        print("You walk past the pit and the ledge widens and the tunnel turns a corner.")
        print("You begin to see a light at the end of the tunnel!")
        print("You head toward the light and freedom!")

        return "end"
        
