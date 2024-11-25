from object import Object
from player import Player
import sys

class QuizReward(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        print(f"Jeff’s words echoed… There’s a time and place for everything, but not now.")


class Room:
    def __init__(self):
        self.room_num = 22
        self.description = (
            "You enter a brightly lit room. A strange voice echoes: 'Welcome to the Quiz Room!\nAnswer my questions correctly to earn rewards, but beware, incorrect answers will cost you!'\nThe room has exits to the north and east."
        )
        self.objects = []
        self.exits = ["north", "east"]
        self.questions = [
            {"question": "Is Python a programming language? (True/False)", "answer": True, "hint": "Think about what you're coding in!"},
            {"question": "Does 2 + 2 equal 5? (True/False)", "answer": False, "hint": "Basic math can solve this!"},
            {"question": "Is Earth the third planet from the Sun? (True/False)", "answer": True, "hint": "Solar system basics."}

        ]
        self.question_index = 0

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

            elif command_base in ["solve", "answer"]:
                self.solve(other_part, player)

            elif command_base == "hint":
                self.show_hint()

            elif command_base == "inventory":
                player.show_inventory()

            elif command_base == "stats":
                player.print_stats()

            elif command_base == "quit":
                self.quit_game(player)

            elif command_base in ["help", "?"]:
                self.show_help()
            
            else:
                print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")

    def describe_room(self):
        print(self.description)

    def move(self, direction):
        if direction in self.exits:
            print(f"You head {direction}.")
            return direction
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if not target:
            print(self.description)
            return

        for obj in self.objects + player.inventory:
            if target.lower() == obj.name.lower():
                print(obj.description)
                if obj.state:
                    print(f"The {obj.name} is {obj.state}.")
                return

        print("You don't see that here.")

    def solve(self, answer, player):
        if self.question_index >= len(self.questions):
            print("You have answered all the questions!")
            return

        question = self.questions[self.question_index]
        try:
            answer_bool = answer.lower() == "true"
        except ValueError:
            print("Please answer with True or False.")
            return

        if answer_bool == question["answer"]:
            reward = QuizReward(
                name=f"Reward{self.question_index + 1}",
                description="A shiny token from the Quiz Room.",
                can_be_gotten=True,
                state="new",
                visible=True
            )
            player.inventory.append(reward)
            print("Correct! You gain a reward.")
        else:
            player.health -= 10
            print("Incorrect! You lose 10 health points.")

        self.question_index += 1
        if self.question_index < len(self.questions):
            print(f"Next Question: {self.questions[self.question_index]['question']}")

    def show_hint(self):
        if self.question_index < len(self.questions):
            print(f"Hint: {self.questions[self.question_index]['hint']}")
        else:
            print("No more hints; you have completed the quiz.")

    def show_help(self):
        print("Available commands: move, go, look, solve, answer, hint, inventory, stats, quit, help")

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)
