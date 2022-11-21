import ast
import random
from datetime import date
import json
import os
import sys
from styles import Styles as s
import time as t

class Game:
    def __init__(self, player: str) -> None:
        self.player = player
        self.session = session
        self.word, self.meaning, self.difficulty, self.space, self.index_of_space = pick_word()
        # self.word chooses a random word from the list of words
        # self.meaning is the meaning of the word
        # self.difficulty is the difficulty of the word
        # if self.space is True, then the word is probably an idiom/phrase
        # self.space is whether a space is in a word
        # self.index_of_space is the index of the space in the word
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
        self.total_points = 0

    def calculate_points(self) -> int:  # called after any probable change in points
        return len((self.guess_progress).replace("_", " ").replace(" ", "")) * 2

    def guess_letter(self, letter: str):
        lowercase_alphabets = "abcdefghijklmnopqrstuvwxyz"
        uppercase_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        punctuation = "'!?,"
        allowed_chars = lowercase_alphabets + uppercase_alphabets + punctuation
        # Validation
        if len(letter) != 1:
            os.system("cls")
            print(padding)
            print(s.pr_red("Please enter a single letter."))
            return
        if letter not in allowed_chars:
            os.system("cls")
            print(padding)
            print(s.pr_red("Please enter a valid character."))
            return
        if letter in self.previous_guesses:
            os.system("cls")
            print(padding)
            print(s.pr_red("You have already guessed that letter."))
            return
        count = 0
        if letter.lower() in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    before = self.guess_progress[: i * 2]
                    after = self.guess_progress[i * 2 + 1 :]
                    self.guess_progress = before + letter.lower() + after
                    count += 1
        if count == 0:
            self.guesses += 1
            self.incorrect_list.append(letter)
            os.system("cls")
            print(
                f"{padding}\nIncorrect! You have "
                + str(settings["guesses"] - self.guesses)
                + f" guesses left. "
            )
        elif count > 1:
            os.system("cls")
            print(
                f"{padding}\nCongratulations. There are "
                + str(count)
                + " "
                + letter
                + f"'s. "
            )
        elif count == 1:
            os.system("cls")
            print(f"{padding}\nCongratulations. There is 1 " + letter + f". ")
        self.previous_guesses.append(letter)


def end_game(log) -> None:
    with open("./game_logs.txt", "r+") as f:
        if os.stat("./game_logs.txt").st_size == 0:
            obj = []
            obj.append(log)
        else:
            obj = ast.literal_eval(f.read())
            obj.append(log)
        new = json.dumps(obj, indent=4)
        f.seek(0)
        f.truncate(0)
        f.write(str(new))
        f.close()
    print(f"You have ended the game with {s.pr_green(log['points'])} points.")
    print(
        f"Here is what we are logging: \n{padding2}\n\t  Name: {log['player']}\n\t  Points: {log['points']}\n\t  Date: {log['date']}\n{padding2}"
    )


def pick_word():
    def read_words():
        global previous_words
        try:
            with open("word_list.txt", "r") as f:
                wordlist = ast.literal_eval(f.read())
                return wordlist
        except:
            print(
                "Error, wordlist is empty. Please contact an administrator for assistance."
            )
            sys.exit()

    wordlist = read_words()
    rand_index = random.randint(0, len(wordlist) - 1)
    while rand_index in previous_words:
        rand_index = random.randint(0, len(wordlist) - 1)
    previous_words.append(rand_index)
    word, word_meaning, difficulty = (
        wordlist[rand_index]["word"],
        wordlist[rand_index]["meaning"],
        wordlist[rand_index]["difficulty"],
    )
    space = False
    index_of_space = []
    for letter in enumerate(word):
        if letter[1] == " ":
            word = word[:letter[0]] + "_" + word[letter[0] + 1 :]
            index_of_space.append(letter[0])
            space = True
    return word, word_meaning, difficulty, space, index_of_space


def menu() -> int:
    while 1:
        os.system("cls")
        print('\n\n')
        t.sleep(0.1)
        hm_banner()  # ascii art
        t.sleep(0.05)
        print(s.pr_bold(f"\n---------------------------- ~ MENU ~ -----------------------------\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        1. Start new game\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        2. Print leaderboard\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        3. Search player\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        4. Exit\n"))
        user_input = input(">> ")
        check, err = validate_input(user_input, 2)
        if check:
            return int(user_input)
        input(f"{err}\nPress Enter to continue...")


def banner(game: object, session: int, choice: int) -> None:
    if choice == 1:
        os.system("cls")
        print("Your word is " + str(len(game.word)) + " letters long. ")
    elif choice == 2:
        print(
            "Session: "
            + str(session)
            + " / "
            + str(settings["attempts"])
            + f"\n{padding}"
        )
    elif choice == 3:
        if(len(game.index_of_space) > 0):
            # replace the underscores with spaces
            new_guess_progress = game.guess_progress
            for i in game.index_of_space:
                new_guess_progress = new_guess_progress[:i*2] + ' ' + new_guess_progress[i*2+1:]
            print(f"Word: {new_guess_progress}")
        else:
            print(f"Word: " + game.guess_progress)
        print(f"Incorrect Guesses: {', '.join(game.incorrect_list)}")
        print(
            f"Correct Guesses: {', '.join(list(set(game.previous_guesses) - set(game.incorrect_list)))}"
        )
        print("Guesses remaining: " + str(settings["guesses"] - game.guesses))
        print_hangman(game.guesses)


def hm_banner():
    print(
        s.pr_red(
            r"""                                                      
    ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
    ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
    ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
    ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
    ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"""
        )
    )


def print_hangman(guess_num: int) -> str:
    if guess_num == 0:
        print(
            r"""            +---+
            |   |
                |
                |
                |
                |
            ========="""
        )
    elif guess_num == 1:
        print(
            r"""            +---+
            |   |
            O   |
            |   |
                |
                |
            ========="""
        )
    elif guess_num == 2:
        print(
            r"""            +---+
            |   |
            O   |
           /|   |
                |
                |
            ========="""
        )
    elif guess_num == 3:
        print(
            r"""            +---+
            |   |
            O   |
           /|\  |
                |
                |
            ========="""
        )
    elif guess_num == 4:
        print(
            r"""            +---+
            |   |
            O   |
           /|\  |
           /    |
                |
            ========="""
        )
    elif guess_num == 5:
        print(
            r"""            +---+
            |   |
            O   |
           /|\  |
           / \  |
                |
            ========="""
        )


def validate_input(user_input, choice: int):
    if choice == 1:
        alphabets_lower = list(map(chr, range(97, 123)))
        alphabets_upper = list(map(chr, range(65, 91)))
        special_chars = ["-", "/", "!"]
        allowed_chars = alphabets_upper + alphabets_lower + special_chars
        if (
            not all(char in allowed_chars for char in user_input)
            or len(user_input) == 0
        ):
            return False, "Please enter a valid name. "
        else:
            if os.stat("./game_logs.txt").st_size != 0:
                with open("./game_logs.txt", "r") as f:
                    game_log = ast.literal_eval(f.read())
                    for value in game_log:
                        if value["player"].lower() == user_input.lower():
                            return False, "This name is already taken. "
            return True, None
    elif choice == 2:
        if not user_input.isnumeric():
            return False, s.pr_red("Please enter a valid option.")
        options = [1, 2, 3, 4]
        for option in options:
            if int(user_input) == option:
                return True, None
        return False, s.pr_red("Please enter a valid option. ")
    elif choice == 3:
        options = ["Y", "N", "y", "n"]
        if user_input not in options:
            return False, s.pr_red("Please enter a valid option. ")
        else:
            if user_input == "Y" or user_input == "y":
                return True, None
            elif user_input == "N" or user_input == "n":
                print(s.pr_green("Thanks for playing! "))
                exit()


def print_leaderboard(num) -> None:
    def read_logs():
        try:
            with open("game_logs.txt", "r") as f:
                logs = ast.literal_eval(f.read())
                return logs
        except FileNotFoundError:
            print("Error. Game logs not found. ")

    logs = read_logs()
    logs.sort(key=lambda x: x["points"], reverse=True)
    print(f"{padding}\n LEADERBOARD (Top {num})\n{padding}")
    for i in range(len(logs)):
        print(f"{i+1}. {logs[i]['player']} - {logs[i]['points']} points")
        if i == num - 1:
            break
    print(f"{padding}\n")


def search_player() -> None:
    def read_logs():
        try:
            with open("game_logs.txt", "r") as f:
                logs = ast.literal_eval(f.read())
                return logs
        except FileNotFoundError:
            print("Error. Game logs not found. ")

    logs = read_logs()
    name = input("Enter player name: ")
    for log in logs:
        if log["player"].lower() == name.lower():
            print(f"{padding}\n{log['player']} - {log['points']} points\n{padding}")
            return
    print(f"{padding}\nPlayer not found. \n{padding}")


def game_settings() -> object:
    try:
        with open("./game_settings.txt") as f:
            game_settings = ast.literal_eval(f.read())
            game_settings["attempts"] = game_settings["number of attempts"]
            game_settings["guesses"] = game_settings["number of guesses"]
            game_settings["words"] = game_settings["number of words"]
            game_settings["top"] = game_settings["number of top players"]
            # Completely unnecessary but good for my sanity
            del (
                game_settings["number of attempts"],
                game_settings["number of words"],
                game_settings["number of top players"],
            )
            return game_settings
    except FileNotFoundError:
        print("Error. game_settings.txt not found. ")


def main():
    while 1:  # loops until check is true
        player_name = input("Enter your name: ")
        check, err = validate_input(player_name, 1)
        if check:
            begin(player_name)
            break
        else:
            print(err)


def begin(player_name: str) -> bool:
    global session
    hang_man = Game(player_name)
    if session == 1:
        banner(hang_man, session, 1)
        banner(hang_man, session, 2)
    else:
        banner(hang_man, session, 2)
    while (hang_man.guesses < settings["guesses"]) and (
        (hang_man.guess_progress).replace(" ", "") != hang_man.word
    ):
        hang_man.calculate_points()
        banner(hang_man, session, 3)
        guess = input("Guess: ")
        hang_man.guess_letter(guess)
        print(padding)
    if hang_man.guesses == settings["guesses"]:
        print(s.pr_red("\nYou have reached the maximum number of guesses. "))
    else:
        print(s.pr_green("\nWell Done! You have guessed the word. "))
    if(hang_man.space == False):
        print(f'After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. The word was "{hang_man.word}". It\'s meaning is: \'{hang_man.meaning}\'')
    else:
        formatted_word = (hang_man.word).replace('_',' ')
        print(f'After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. The word was "{formatted_word}". It\'s meaning is: \'{hang_man.meaning}\'')
    if session < settings["attempts"]:
        session += 1
        log["points"] += hang_man.calculate_points()
        print(f"Your total points are {s.pr_bold(log['points'])}.")
        begin(player_name)
    else:
        if log["points"] > 15:
            print(padding2)
            print(f"Congratulations! You have {s.pr_green('won')} the game! ")
        else:
            print(padding2)
            print(f"You have {s.pr_red('lost')} the game. ")
        log["points"] += hang_man.calculate_points()
        log["player"] = (hang_man.player).capitalize()
        end_game(log)


if __name__ == "__main__":
    settings = game_settings()
    padding = "-" * 40
    padding2 = "=" * 40
    try:
        while 1:
            choice = menu()
            if choice == 1:
                session = 1
                previous_words = []
                log = {
                    "player": "",
                    "points": 0,
                    "date": date.today().strftime("%d/%m/%y"),
                }
                main()
            elif choice == 2:
                print_leaderboard(int(settings["top"]))
            elif choice == 3:
                search_player()
            elif choice == 4:
                print(s.pr_red(("\nThank you for playing. ")))
                sys.exit()
            input("Press Enter to continue...")
    except KeyboardInterrupt:
        print(s.pr_red(("\nThank you for playing. ")))
        sys.exit()
