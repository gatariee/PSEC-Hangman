import ast
import random
from datetime import date
import json
import os
import sys
from styles import Styles as s


class Game:
    def __init__(self, player: str) -> None:
        self.player = player
        self.session = session
        self.word, self.type, self.difficulty = Game.pick_word()
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
        self.total_points = 0

    def calculate_points(self) -> int:  # called after any probable change in points
        return len((self.guess_progress).replace("_", " ").replace(" ", "")) * 2

    def end_game(self, log) -> None:  # called at the end of the game to generate report
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
        print(f"You have ended the game with {s.prGreen(log['points'])} points.")
        print(
            f"Here is what we are logging: \n{padding2}\n\t  Name: {log['player']}\n\t  Points: {log['points']}\n\t  Date: {log['date']}\n{padding2}"
        )

    def guess_letter(self, letter: str):
        def verify_guess(guess):
            if not guess.isalpha():
                os.system("cls")
                print(s.prRed(f"{padding}\nPlease enter a letter."))
            elif len(guess) != 1:
                os.system("cls")
                print(s.prRed(f"{padding}\nPlease enter a single letter. "))
            elif guess in self.previous_guesses:
                os.system("cls")
                print(s.prRed(f"{padding}\nYou already guessed that letter. "))
            return True

        if not verify_guess(letter):
            return
        count = 0  # refers to number of times letter appears in word
        if (
            letter.lower() in self.word
        ):  # i did this function while drunk so it's a bit scuffed
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    before = self.guess_progress[: i * 2]
                    after = self.guess_progress[i * 2 + 1 :]
                    self.guess_progress = before + letter.lower() + after
                    count += 1
        if (
            count == 0
        ):  # if letter is not in word, append letter to the incorrect list and increment to number of guesses
            self.guesses += 1
            self.incorrect_list.append(letter)
            os.system("cls")
            print(
                f"{padding}\nIncorrect! You have "
                + str(settings["guesses"] - self.guesses)
                + f" guesses left. "
            )
        elif (
            count > 1
        ):  # if there's more than 1 of the same letter in the word, print the number of times it appears
            os.system("cls")
            print(
                f"{padding}\nCongratulations. There are "
                + str(count)
                + " "
                + letter
                + f"'s. "
            )
        elif (
            count == 1
        ):  # if there's only 1 of the letter in the word, print that there's 1 of the letter
            os.system("cls")
            print(f"{padding}\nCongratulations. There is 1 " + letter + f". ")
        self.previous_guesses.append(
            letter
        )  # add letter to previous guesses regardless if it's correct or wrong

    def pick_word(self):
        def read_words():
            global previous_words  # i really don't want to use global variables but i can't find a way not to
            try:
                with open("word_list.txt", "r") as f:
                    wordlist = ast.literal_eval(f.read())
                    return wordlist
            except:
                print(
                    "Error, wordlist is empty. Please contact an administrator for assistance."
                )
                sys.exit()

        wordlist = read_words()  # returns wordlist as a dictionary
        rand_index = random.randint(
            0, len(wordlist) - 1
        )  # pick a random index from the wordlist
        while (
            rand_index in previous_words
        ):  # if the random index has already been used, pick a new one
            rand_index = random.randint(0, len(wordlist) - 1)
        previous_words.append(rand_index)
        word, word_type, difficulty = (
            wordlist[rand_index]["word"],
            wordlist[rand_index]["type"],
            wordlist[rand_index]["difficulty"],
        )
        return word, word_type, difficulty


def menu() -> int:
    while 1:
        os.system("cls")
        hm_banner()  # ascii art
        print(
            s.prBold(
                """
---------------------------- ~ MENU ~ -----------------------------\n
                        1. Start new game\n
                        2. Print leaderboard\n
                        3. Search player\n
                        4. Exit\n
------------------------------------------------------------------\n"""
            )
        )
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
        print("Word: " + game.guess_progress)
        print(f"Incorrect Guesses: {', '.join(game.incorrect_list)}")
        print(
            f"Correct Guesses: {', '.join(list(set(game.previous_guesses) - set(game.incorrect_list)))}"
        )
        print("Guesses remaining: " + str(settings["guesses"] - game.guesses))
        print_hangman(game.guesses)


def hm_banner():
    print(
        s.prRed(
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
    if choice == 1:  # Name validation
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
    elif choice == 2:  # menu validation
        if not input.isnumeric():
            return False, s.prRed("Please enter a valid option.")
        options = [1, 2, 3, 4]
        for option in options:
            if int(input) == option:
                return True, None
        return False, s.prRed("Please enter a valid option. ")
    elif choice == 3:
        options = ["Y", "N", "y", "n"]
        if input not in options:
            return False, s.prRed("Please enter a valid option. ")
        else:
            if input == "Y" or input == "y":
                return True, None
            elif input == "N" or input == "n":
                print(s.prGreen("Thanks for playing! "))
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
    logs.sort(
        key=lambda x: x["points"], reverse=True
    )  # sort from highest to lowest points
    print(f"{padding}\n LEADERBOARD (Top {num})\n{padding}")
    for i in range(len(logs)):
        # could also i in range num but this is more flexible because it can print less than num if there are less than num logs
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


def main() -> None:
    while 1:  # loops until check is true
        player_name = input("Enter your name: ")
        check, err = validate_input(player_name, 1)
        if check:
            begin(player_name)
            break
        else:
            print(err)


def begin(player_name: str) -> None:
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
        # After every guess, either the word is progressively guessed OR the number of guesses is incremented until the number of guesses is equal to the number of guesses allowed
        hang_man.calculate_points()
        banner(hang_man, session, 3)
        guess = input("Guess: ")
        hang_man.guess_letter(guess)
        print(padding)
    if hang_man.guesses == settings["guesses"]:  # if reached max number of guesses
        print(s.prRed("\nYou have reached the maximum number of guesses. "))
    else:
        print(s.prGreen("\nWell Done! You have guessed the word. "))
    print(f'The {hang_man.type} was "{hang_man.word}"')  # prints regardless of win/loss
    if (
        session < settings["attempts"]
    ):  # if there are still attempts left, loop until end
        session += 1
        log["points"] += hang_man.calculate_points()
        print(f"Your total points are {s.prBold(log['points'])}.")
        begin(player_name)
    else:
        if log["points"] > 15:
            print(padding2)
            print(f"Congratulations! You have {s.prGreen('won')} the game! ")
        else:
            print(padding2)
            print(f"You have {s.prRed('lost')} the game. ")
        log["points"] += hang_man.calculate_points()
        log["player"] = (hang_man.player).capitalize()
        Game.end_game(log)
        replay()


def replay() -> None:
    while 1:
        wanna_replay = input("Play again? (Y/N): ")
        check, err = validate_input(wanna_replay, 3)
        if check:
            while 1:
                choice = menu()
                if choice == 1:
                    global session
                    global previous_words
                    global log
                    session = 1
                    previous_words = []
                    log = {
                        "player": "",
                        "points": 0,
                        "date": date.today().strftime("%d/%m/%y"),
                    }
                    main()
                    break
                elif choice == 2:
                    print_leaderboard(settings["top"])
                elif choice == 3:
                    search_player()
                elif choice == 4:
                    print("Thank you for playing. ")
                    exit()
                input("Press Enter to continue...")
        else:
            print(err)


if __name__ == "__main__":
    try:
        settings = game_settings()
        padding = "-" * 40
        padding2 = "=" * 40
        session = 1
        previous_words = []
        log = {"player": "", "points": 0, "date": date.today().strftime("%d/%m/%y")}
        while 1:
            choice = menu()
            if choice == 1:
                main()
                break
            elif choice == 2:
                print_leaderboard(int(settings["top"]))
            elif choice == 3:
                search_player()
            elif choice == 4:
                print(s.prRed(("\nThank you for playing. ")))
                sys.exit()
            input("Press Enter to continue...")
    except KeyboardInterrupt:
        print(s.prRed(("\nThank you for playing. ")))
        sys.exit()
