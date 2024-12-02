class Room:
    def __init__(self):
        self.room_num = 1
        self.description = (
            "This is a placeholder room - waiting for Hector to finish.\n"
            "Your exits are: south, down\n"
        )
        self.exits = ["south", "down"]

    def enter(self, player):
        print(self.description)

        while True:
            command = input("What would you like to do? ").strip().lower()

            if command.startswith("go "):
                direction = command[3:]
                if direction in self.exits:
                    print(f"You chose to go {direction}.")
                    return direction
                else:
                    print(f"You can't go {direction}. It's not a valid exit.")
            else:
                print("You can't do that here - this is just a placeholder.")
                print("You should just pick an exit and get on with it.")