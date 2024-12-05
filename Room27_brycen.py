from object import Object
from player import Player
import sys  # For exiting the game
import random


class Book (Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def set_variables(self):
        self.can_be_gotten = True
        self.visible = True

class Note (Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)


class Room:

    objects = []

    def __init__(self):
        self.room_num = 27
        self.entrance_description = (
            "\n\n------------ Description ------------"
            "\nAs you step into the room, you are greeted by a sight both awe-inspiring and eerie."
            "\nTowering bookshelves stretch endlessly towards the vaulted ceiling, each shelf filled with ancient tomes and scrolls."
            "\nThe air is thick with the scent of old parchment and a faint hint of mustiness. Dim, flickering candles cast dancing shadows on the walls,"
            "\nand the faint rustle of pages being turned echoes softly through the vast space. At the center of the room, a grand oak table stands,"
            " laden with manuscripts and quills, as if abandoned mid-study."
            "\nThe flickering light reveals a majestic figure perched atop a high podium — an imposing owl with piercing, luminous eyes that seem to see through your very soul."
            "\nThe guardian of this library watches your every move, its presence both regal and intimidating."
            "\nYou can't help but feel a sense of wonder and foreboding as you take in the vast expanse of knowledge contained within these walls."
            "\nYet, an uneasy tension hangs in the air, as if the library itself is alive and watching, waiting to reveal its secrets to those deemed worthy — or to punish those who are not."
            "\n"
        )

        self.move_from_entrance_description = (
            "\n\n------------ Description ------------"
            "\nYou start to enter into the libray and the owl lets out war screeches."
            "\nStartled, you look up to see the owl swoop from its perch and scale 10 times in size."
            "\nNow towering over you, the Guardian Owl demands to know your reasoning for entering."
            "\nYou can either:\n"
            "'Show' the Guardian Owl your piece of paper from the previous room"
            "-- OR --\n"
            "'Lie' and say you want to explore the vast knowledge of tomes in the Guardian Owl's collection"
            "\n"
        )

        self.library_description = (
            "\n\n------------ Description ------------"
            "\nAs you step past the owl, a sense of relief washes over you, but the grandeur of the library quickly replaces it with awe."
            "\nThe room is immense, with shelves that stretch up to a vaulted ceiling and disappear into the shadows above."
            "\nEach shelf is packed with ancient tomes, their spines worn and titles faded, hinting at the vast repository of knowledge contained within."
            "\nThe scent of old parchment and leather fills the air, mingling with the faint, lingering aroma of candle wax. Soft light filters through stained glass windows high above, casting colorful patterns on the wooden floor."
            "\nThe silence is profound, broken only by the occasional rustle of pages and the distant creak of the wooden structure settling."
            "\nIn the center of the room, a large oak table stands, covered in open books, maps, and strange artifacts, as if left in the midst of some intense research."
            "\nAs you move deeper into the library, you notice alcoves and nooks tucked away between the shelves, offering secluded spots for study and contemplation."
            "\nThe atmosphere is both inviting and intimidating, a testament to the centuries of wisdom and secrets held within these walls."
            "\n"
        )

        self.library_look_description = (
            "\n\n------------ Description ------------"
            "\nYou explore the library and its vastness. You notice numbers following the same pattern as your note along the shelves. You realize the number is an ISBN number. Of course! It's a library."
            "\nScouring through the shelves and book titles, you search of the one that may match the ISBN number on your note."
            "\nComing up empty and starting to get discouraged, you continue on. Deeper and deeper into the main hall."
            "\nThe old wood creaks with every step, and the small fires in the sconce torches dimly light the way."
            "\nIn the corner you notice a particular dark area with what seems a 'gate'. A wind rushes through, disturbing the crackling flames and turns the pages on a nearby open book, startling you."
            "\n"
        )
        
        self.move_from_library_description = (
            "\n\n------------ Description ------------"
            "\nAs you cautiously approach the dark corner, you noticed. You make out what seems an iron gate, its intricate patterns casting eerie shadows in the flickering torchlight."
            "\nYou rattle the gate, but it doesn't budge. Suddenly, from the darkness, a grotesque goblin emerges, its eyes gleaming with mischief."
            "\nWith a sly grin, the goblin blocks your path and announces, 'To pass through here, you must play a game. Guess my number, and I shall let you enter.'"
            "\n"
        )

        self.forbidden_section_description = (
            "\n\n------------ Description ------------"
            "\nBeyond, the room seems darker, the very atmosphere thick with an oppressive weight. The shelves are lined with books unlike any you’ve ever seen before — their covers pulsate, shifting colors in patterns that make your eyes ache."
            "\nThe pages within seem to move on their own, flicking open and shut as if caught in some invisible wind. Some books emit strange, otherworldly sounds — a low growl, a hissing whisper, or a crackling that sounds almost like fire."
            "\nYou take a step forward and notice something even more unnerving: one book's pages curl outward, revealing long, dark tentacles that writhe and snap at the air, as if struggling to break free. Another tome seems to exhale a swirling mist, which briefly takes the form of a fiery bird before dissipating into the air."
            "\nThe very books themselves seem alive, as though they have thoughts, intentions — and they might not be pleased to have you here. The air grows heavier with each step, as if the forbidden knowledge within these pages is aware of your presence, and not all of it is willing to stay hidden."
            "\n"
        )

        self.forbidden_look_description = (
            "\n\n------------ Description ------------"
            "\nYou scan the shelves, pulling strange books from their places. Some are made of materials you can't identify — smooth stone, pulsing metal — and the titles shift as you try to focus on them. One book opens on its own, glowing symbols rearranging before your eyes, but none match the number from your note."
            "\nThe air grows heavy with whispers, but you press on, determined. Finally, you find it: a 'book' with the number etched on its slot in the shelf, hidden in a dark corner. It has a faint golden glow coming from within the pages"
            "\n"
        )

        self.open_book_description = (
            "\n\n------------ Description ------------"
            "\nYou open the book, and the golden pages begin to flutter, slowly at first, then faster and faster, as if powered by an unseen force."
            "\nThe sound of rustling pages fills the air, growing louder with each turn, until the book seems to hum with energy. A gust of wind rushes from the pages, tugging at your clothes and hair, as the pages race towards the center."
            "\nWith a sudden burst, a swirling vortex forms in the air, glowing with otherworldly light. You lean in, drawn by the strange force, and before you can react, the wind pulls you in. The world spins, and you are sucked into the portal, vanishing from the library."
            "\n"
        )

        self.winning_statements = (
            "\n\n------------ Description ------------"
            "\nAs you get sucked into the swirling vortex, the world blurs around you, and everything goes black. When your vision clears, you suddenly find yourself in a much more familiar setting—your own bed."
            "\nThe warmth of the blankets, the soft pillow beneath your head, and the gentle morning light pouring through the window make it feel like you've just woken up from a long, restful sleep."
            "\nYou stretch, yawn, and glance around, realizing it was all... just a dream? The grand library, the mysterious note, the troll with his guessing game—none of it was real."
            "\nYou are back in the comfort of your own home, snug and cozy. The only thing that remains is the faint feeling of having been on a wild \033[3mAdventure.\033[0m"
        )

        self.message_to_players = (
            "\nThanks for playing our collaboritve game from the students of SE-3150. We hope you enjoyed it as much as we did!"
        )

        self.book = Book("Book", "A dusty old thick book, with an ominous glow from within the pages.", False, "closed", False)
        self.objects.append(self.book)

        self.note = Note("Note", "A note with an odd number: 978-1-119293-32-3", True, "Old and tattered", True)

        self.state = "entrance"

        self.exits = ["down"]
        self.hint_requests = 0



    def enter(self, player):
        player.current_room = self.room_num
        self.check_player_inventory_for_note(player)
        
        # step 1 - describe entrance
        print(self.entrance_description)

        # step 2 - manange player state within library
        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if self.state == "entrance":
                #print("now using entrance commands")
                self.handle_entrance_commands(command_base, other_part, player)
            elif self.state == "library":
                #print("now using library commands")
                self.handle_library_commands(command_base, other_part, player)
            elif self.state == "forbidden_section":
                #print("now using forbidden commands")
                self.handle_forbidden_section_commands(command_base, other_part, player)
            else:
                print("Unknown state.")
            
    def handle_entrance_commands(self, command_base, other_part, player):
        if command_base == "look":
            self.look(other_part, player)

        elif command_base in ["move", "go"]:
            self.move_from_entrance(player)

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

    def handle_library_commands(self, command_base, other_part, player):
        if command_base in ["move", "go"]:
            self.move_from_library(player)
        
        elif command_base == "look":
            self.look(other_part, player)

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

    def handle_forbidden_section_commands(self,command_base, other_part, player):
        if command_base == "look":
            self.look(other_part, player)

        elif command_base in ["move", "go"]:
            self.unknown_command()

        elif command_base in ["get", "take"]:
            self.get(other_part, player)

        elif command_base in "use":
            self.use(other_part, player)

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
        if self.state == 'entrance':
            print(self.entrance_description)
        elif self.state == 'library':
            print(self.library_description)
        elif self.state == 'forbidden_section':
            print(self.forbidden_section_description)

        if self.objects:
            for obj in self.objects:
                print(f"There are {obj.name}s here. Which one...")


    ## self.state == 'entrance' functions
    def move_from_entrance(self, player):
        print(self.move_from_entrance_description)
        ans = input("What do you do? (show/lie) ").lower().strip()
        if ans == 'show':
            self.showNote(player)
        elif ans == 'lie':
            self.Lie(player)
            self.describe_room()
        else:
            print("That's not a valid response. Try again.")
            self.move_from_entrance(player)

    def showNote(self, player):
        print("\nYou show the Guardian Owl the note. The Guardian Owl's eyes glow with anger and it lets out a deafening screech before swooping down and destroying you.")
        player.health = 0
        print("Your health has dropped to 0. You have been killed by the owl.")
        # Check player's health and exit the game if it's 0
        if not player.is_alive():
            print("\nGame Over.")
            print(f"\nFinal Score: {player.score}\n")
            sys.exit(0)

    def Lie(self, player):
        print("\nYou lie and say you want to explore the vast knowledge of tomes in the Guardian Owl's collection. The Guardian Owl eyes you suspiciously but allows you to proceed.")
        print("\nYou earned +10 points!")
        player.score += 10
        self.state = "library"



    ## self.state == 'library' functions
    def move_from_library(self, player):
        print("\nYou earned +5 points!")
        player.score += 5
        print(self.move_from_library_description)
        print("\nYou think to yourself that you don't have much choice."
              "\nYou've already explored the vast library so you agree to play the goblin's game.")  
        self.goblin_game(player)

    def goblin_game(self, player):
        max_guesses = 3
        goblin_number = random.randint(1,10)
        #print(goblin_number)
        print("\n\nThe goblin grins mischievously. 'Guess my number between 1 and 10,' it says.")
        for attempt in range(max_guesses):
            guess = input(f"\nGuess {attempt + 1} / {max_guesses}: ")
            try:
                guess = int(guess)
                if isinstance(guess, int):
                    if guess == goblin_number:
                        print("\n\nThe goblin mumbles and unlocks the gate. 'You may pass,' it grumbles."
                              "\n'Welcome to the forbidden section of the library. Don't let that old bird catch you here.' He grins and wonders off.")
                        print("\nYou earned +50 points!")
                        player.score += 50
                        self.state = 'forbidden_section'
                        self.forbidden_section()
                        return
                    elif guess > goblin_number and guess <= 10:
                        print("\nThe goblin chuckles. 'Wrong! Guess again, a little lower.'")
                        print("\nYou lost -2 points!")
                        player.score -= 2
                    elif guess < goblin_number and guess >= 1:
                        print("\nThe goblin chuckles. 'Wrong! Guess again, a little higher.'")
                        print("\nYou lost -2 points!")
                        player.score -= 2
                    else:
                        print("\nThe goblin laughs out loud at you. 'Go ahead and waste your guesses with that number!")
                        print("\nYou lost -5 points!")
                        player.score -= 5
            
            except ValueError:
                print("You wasted a guess! That's not a valid number.")
                print("\nYou lost -30 points!")
                player.score -= 30

        player.health -= 20

        if not player.is_alive():
            print("\nYou died from the goblin! Game Over.")
            print(f"\nFinal Score: {player.score}\n")
            sys.exit(0)

        print("\nThe goblin pushes you back, and you feel a bit weaker. Your health is now ", player.health)
        print("\nYou reapproach the goblin, he tells you through a disgusting burp that he thought of a new number!")
        self.goblin_game(player)

    ## self.state == 'forbidden_section' functions
    def forbidden_section(self):
        print("\nThe gate to the forbidden section creaks open...")
        self.describe_room()

    def use(self, item, player):
        if item == 'book':
            print(self.open_book_description)
            print("\nYou earned +100 points!")
            player.score += 100
            self.win_conditions(player)
        

    def look(self, target, player):
        if(target == None or target == ""):
            self.describe_room()
            return

        if target == "library":
            self.hint_requests = 0
            print(self.library_look_description)

        elif target == "shelves":
            self.hint_requests = 0
            print(self.forbidden_look_description)
            print("\nYou earned +10 points!")
            player.score += 10
            self.book.set_variables()

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

    def check_player_inventory_for_note(self, player):
        if 'note' in player.inventory or 'Note' in player.inventory:
            return
        else:
            player.inventory.append(self.note)

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        if self.state == 'forbidden_section':
            print("Available commands: move, go, look, get, take, use, drop, inventory, stats, help, hint, quit")
        else:
            print("Available commands: move, go, look, drop, inventory, stats, help, hint, quit")

    def show_hint(self):
        if self.state == 'entrance':
            print("This is the entrance to the library. Consider 'move'ing into it, but be weary of the Guardian Owl...")
        
        elif self.state == 'library':
            self.hint_requests += 1
            if self.hint_requests == 3:
                print("Run 'look library'")
            print("This is the 'library'. Keep the note hidden from the Guardian Owl. Try 'look'ing around...")

        elif self.state == 'forbidden_section':
            if self.book.visible == True:
                print("Run 'get book'")
                return
            self.hint_requests += 1
            if self.hint_requests == 3:
                print("Run 'look shelves'")
            print("This is the forbidden section. The book you're looking for has got to be here. Try 'look'ing at the 'shelves'...")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")

    def win_conditions(self, player):
        #print(self.winning_statements)
        #print(f"\n{player.name}, {self.message_to_players}")
        #print(f"Final score: {player.score}")
        #sys.exit(0)
        return "down"