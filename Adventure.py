import os
import sys
from player import Player  
from object import Object  
import importlib

def load_rooms():
    rooms = []

    # Get a list of files in the current directory
    all_files = os.listdir()
    room_files = [
        file for file in all_files 
        if file.startswith("Room") and file.endswith(".py") and "_" in file
    ]

    # Sort the room files based on the room number
    try:
        room_files.sort(key=lambda x: int(x[4:].split("_")[0]))
    except ValueError as e:
        print(f"Error sorting room files: {e}")
        return []

    # Load the rooms in the correct order
    for room_file in room_files:
        room_name = room_file[:-3]  # Strip '.py' from the filename
        try:
            # Attempt to import the room module
            room_module = importlib.import_module(room_name)
            
            # Attempt to create a Room instance
            room_instance = room_module.Room()
            rooms.append(room_instance)
        except (SyntaxError, ImportError, AttributeError) as e:
            print(f"Error loading {room_file}: {e}")
            print(f"Skipping {room_file} due to the above error.")
        except Exception as e:
            print(f"Error initializing Room in {room_file}: {e}")
            print(f"Skipping {room_file} due to the above error.")

    return rooms

# Load the game map from a file
def parse_map_file(filename):
    rooms = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    current_room_index = None
    connections = {}

    for line in lines:
        line = line.strip()
        if line.startswith("Room:"):
            # When we encounter a new room, store the current room's connections
            if current_room_index is not None:
                rooms.append(connections)
            
            current_room_index = int(line.split(":")[1])  # Extract the room number
            connections = {}
        elif line:
            # Parse the connections in the format "direction,room_number"
            direction, room_number = line.split(",")
            connections[direction.strip()] = int(room_number.strip())

    # Add the last room's connections to the list
    if current_room_index is not None:
        rooms.append(connections)

    return rooms

def print_intro(player):
    print(f"Welcome, {player.name}, to the Dungeon of Ludwig the Mad!")
    print("The dungeon is filled with traps, tricks, and surprises.")
    print("Great treasure awaits the intrepid adventurer who can survive and escape.")
    print("Can you make it out alive?\n")


def print_instructions():
        print("""
Instructions:
    This is a text-based adventure game. You are trying to move from room to room gathering treasre, avoiding 
    traps and solving puzzles. You'll interact with the dungeon and its objects by issuing text commands.
    The default commands are:
        
    - move or go, accompanied by a direction (north, south, east, west, up, or down) to move to another location.
    - look <thing>: Describes the thing you are looking at. Just typing 'look' will describe the room.
    - get or take <object>: Puts the object into your inventory (if allowed).
    - drop <object>: Removes an item from your inventory.
    - inventory: Lists the objects you have in your inventory. You can 'look' at the objects for clues.
    - use <thing>: Uses objects in your inventory or sometimes in the room.
    - Custom commands: Try specific actions based on the room's features.
    - help: Lists available commands and visible exits.
    - hint: gives you a hint about what you could try in that specific room.
 """)
        



# Main game loop
def main():
    # Step 1: Load the rooms from files
    rooms = load_rooms()
    if len(rooms) < 2:
        print("This is an Adventure game engine. In order for this to run properly")
        print("you need to create a bunch of rooms. Read the README.md and follow the directions.\n")
        sys.exit(0)

    # Step 2: Load the game map
    game_map = parse_map_file("map.txt")

    # Step 3: Create the player instance
    player_name = input("Enter your name, adventurer: ")
    player = Player(
        name=player_name,
        health=100,
        condition="healthy",
        current_room=0
    )

    # Step 4: Print the game intro
    print_intro(player)

    # Step 5: Ask if the user wants instructions
    if input("Do you want instructions? (yes/no) ").lower().startswith('y'):
        print_instructions()
 
    # Step 6: Main game loop
    # start in room 0
    # Main game loop
    current_room = 0
    while True:
        # Get the result from the room's enter method
        result = rooms[current_room].enter(player)

        # Handle fasttravel
        if result == "fasttravel":
            while True:
                try:
                    target_room = int(input("Enter the room number you want to fast travel to: "))
                    if target_room < 0 or target_room >= len(rooms):
                        print(f"Room {target_room} does not exist. Please enter a valid room number.")
                    else:
                        print(f"You fast travel to Room {target_room}.")
                        current_room = target_room
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid room number.")
            continue

        # Handle standard movement commands
        next_direction = result

        # Check if the player is dead
        if not player.is_alive():
            print("You have perished in the dungeon! Game over. Your score is: ", player.score)
            return

        if next_direction == "end":
            print("You have successfully exited the dungeon! Congratulations!\n")
            player.print_stats()
            return

        if next_direction not in game_map[current_room]:
            print(f"room {current_room} tried to go {next_direction} and that's not in the game_map:")
            print(game_map[current_room])
            return

        # Set the current room to the one connected in the specified direction
        current_room = game_map[current_room][next_direction]

        

# Run the game
if __name__ == "__main__":
    main()
