import sys

class SpaceDevice:
    def __init__(self, name, description, can_be_used, state, visible):
        self.name = name
        self.description = description
        self.can_be_used = can_be_used
        self.state = state
        self.visible = visible

    def use(self):
        if self.name == "Oxygen Recycler":
            if self.state == "offline":
                self.state = "online"
                print("Oxygen Recycler activated. Life support systems stabilizing.")
            else:
                self.state = "offline"
                print("Oxygen Recycler shutdown. Warning: Oxygen levels decreasing!")


class SpaceStation:
    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "You awaken in a damaged space station, emergency lights flickering.\n"
            "Alarms blare intermittently. The hull shows signs of micro-meteorite damage.\n"
            "A critical oxygen recycler sits in the corner, its status uncertain.\n"
            "A single airlock leads to the next section of the station.\n"
        )
        recycler = SpaceDevice("Oxygen Recycler", "A complex machine maintaining life support systems", True, "offline", True)
        self.objects.append(recycler)
        self.exits = ["airlock"]

    def enter(self, player):
        self.describe_room()

        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]
            other_part = parts[1] if len(parts) > 1 else ""

            if command_base in ["move", "go"]:
                next_room = self.move(other_part)
                if next_room:
                    return next_room
            
            elif command_base == "look":
                self.look(other_part, player)
            elif command_base in ["get", "take"]:
                self.get(other_part, player)
            elif command_base in ["use"]:
                self.use_device(other_part, player)
            elif command_base == "inventory":
                self.show_inventory(player)
            elif command_base == "quit":
                self.quit_game(player)
            elif command_base in ["help", "?"]:
                self.show_help()
            else:
                self.unknown_command()

    def describe_room(self):
        print(self.description)
        for obj in self.objects:
            if obj.visible:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["airlock", "forward"]:
            print("You carefully navigate through the damaged airlock...")
            return "airlock"
        print("You can't go that way.")
        return None

    def look(self, target, player):
        if not target:
            self.describe_room()
            return

        for obj in self.objects + player.inventory:
            if target.lower() == obj.name.lower():
                print(obj.description)
                if obj.state:
                    print(f"Current status: {obj.state}")
                return
        print("You don't see that here.")

    def get(self, item_name, player):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                if not obj.can_be_used:
                    print(f"The {obj.name} cannot be taken.")
                    return
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name}.")
                return
        print(f"There is no {item_name} here.")

    def use_device(self, device_name, player):
        for obj in self.objects + player.inventory:
            if device_name.lower() == obj.name.lower():
                obj.use()
                return
        print(f"You can't use {device_name}.")

    def show_inventory(self, player):
        if not player.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in player.inventory:
                print(f"- {item.name}")

    def quit_game(self, player):
        if input("Abandon mission? (yes/no) ").lower().startswith('y'):
            print("Mission aborted. Station systems failing...")
            sys.exit(0)

    def show_help(self):
        print("Commands: move, look, get, use, inventory, quit")

    def unknown_command(self):
        print("Invalid command. Type 'help' for available actions.")