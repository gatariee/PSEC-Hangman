"""
Main Program

StudentID:      p2205513
Name:           Zavier Lee Wey
Class:          DISM/FT/1B/05
Assessment:     CA1-1

Script name:
    hangman.py

Purpose:
    This script is a hangman game that allows the user to play hangman 

Usage syntax:
    python hangman.py

Input file:
    ./data/word_list.txt

Output file:
    ./data/game_logs.txt

Python version:
    Python 3.10.8

Reference:
https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python
https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file-using-python
https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

Library/Module:
- these modules are installed by default in python 3.10.8
    os
    sys
    time
    random
    datetime
    ast
    json

Known Issues:
    - tbd

"""
import ast
import random
import json
import os
import sys
import time as t
from datetime import date
from styles import Styles as s

# change working directory to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:
    """
    A class to represent a Player and their game status.
    All game variables are stored in this class

    ...
    Attributes
    ----------
    player : str
        The name of the player
    SESSION : int
        The number of the SESSION
    word : str
        The word to be guessed
    meaning : str
        The meaning of the word
    difficulty : str
        The difficulty of the word
    space : bool
        Whether the word contains a space
    index_of_space : int
        The index of the space in the word
    guesses : int
        The number of guesses made
    previous_guesses : list
        The list of previous guesses
    incorrect_list : list
        The list of incorrect guesses
    guess_progress : str
        The current progress of the word
    total_points : int
        The total points earned

    Methods
    -------
    calculate_points()
        Calculates the points earned
    guess_letter(letter: str)
        Guesses a letter
    """

    def __init__(self, player: str) -> None:
        """
        At the start of every SESSION, the attributes of the game class are re-initialized

        Args:
            player (str): Input name of player
        """
        self.player = player
        (
            self.word,
            self.meaning,
            self.difficulty,
            self.space,
            self.index_of_space,
        ) = pick_word()
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
        self.total_points = 0

    def calculate_points(self) -> int:
        """
        This method is called everything a guess is made and calculates the points earned.

        Returns:
            int: The points earned
        """
        # (the number of letters in the word, removing underscores) * (2 points per correct guess)
        # e.g (_est = 3 letters, 2 points per correct guess = 6 points)
        return len((self.guess_progress).replace("_", " ").replace(" ", "")) * 2

    def guess_letter(self, letter: str) -> None:
        """
        The main part of the game where the player guesses a letter.

        Args:
            letter (str): The letter guessed
        """
        lowercase_alphabets = "abcdefghijklmnopqrstuvwxyz"
        uppercase_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        punctuation = "'!?,"
        allowed_chars = lowercase_alphabets + uppercase_alphabets + punctuation
        # Validation
        if len(letter) != 1:
            os.system("cls")
            print(PADDING)
            print(s.pr_red("Please enter a single letter."))
            return
        if letter not in allowed_chars:
            os.system("cls")
            print(PADDING)
            print(s.pr_red("Please enter a valid character."))
            return
        if letter in self.previous_guesses:
            os.system("cls")
            print(PADDING)
            print(s.pr_red("You have already guessed that letter."))
            return

        count = 0
        if letter.lower() in self.word:  # if letter is in the word
            for i, char in enumerate(self.word):
                if char == letter.lower():
                    count += 1
                    self.guess_progress = (
                        self.guess_progress[: i * 2]
                        + letter.lower()
                        + self.guess_progress[i * 2 + 1 :]
                    )
        if (
            count == 0
        ):  # if count has not been incremented, the letter is not in the word
            self.guesses += 1
            self.incorrect_list.append(letter)
            os.system("cls")
            print(
                f"{PADDING}\nIncorrect! You have "
                + str(settings["guesses"] - self.guesses)
                + " guesses left. "
            )
        elif count > 1:
            os.system("cls")
            print(
                f"{PADDING}\nCongratulations. There are "
                + str(count)
                + " "
                + letter
                + "'s. "
            )
        elif count == 1:
            os.system("cls")
            print(f"{PADDING}\nCongratulations. There is 1 " + letter + ". ")
        self.previous_guesses.append(letter)


def end_game(log_file: dict) -> None:
    """
    This function is called when the game ends.

    Args:
        log_file (dict): The log file
    """
    with open("../data/game_logs.txt", "r+") as f:
        if os.stat("../data/game_logs.txt").st_size == 0:
            obj = []
            obj.append(log_file)
        else:
            obj = ast.literal_eval(f.read())
            obj.append(log_file)
        new = json.dumps(obj, indent=4)
        f.seek(0)
        f.truncate(0)
        f.write(str(new))
    print(f"You have ended the game with {s.pr_green(log['points'])} points.")
    print(
        f"Here is what we are logging: \n{PADDING2}\n\t  Name: {log['player']}\n\t  Points: {log['points']}\n\t  Date: {log['date']}\n{PADDING2}"
    )


def pick_word() -> tuple[str, str, str, bool, int]:
    """
    This function picks a random word from the word list.

    Returns:
        word (str): The word to be guessed
        word_meaning (str): The meaning of the word
        difficulty (str): The difficulty of the word
        space (bool): Whether the word contains a space
        index_of_space (int): The index of the space in the word

    """

    def read_words() -> list:
        """_summary_

        Returns:
            list: This is a list of words
        """
        try:
            with open("../data/word_list.txt", "r") as f:
                wordlist = ast.literal_eval(f.read())
                return wordlist
        except FileNotFoundError:
            print(
                "Error, wordlist is empty. Please contact an administrator for assistance."
            )
            sys.exit()

    wordlist = read_words()
    rand_index = random.randint(0, len(wordlist) - 1)
    while (
        rand_index in previous_words or wordlist[rand_index]["enabled"] != "on"
    ):  # checklist: 1.3
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
            word = word[: letter[0]] + "_" + word[letter[0] + 1 :]
            index_of_space.append(letter[0])
            space = True
    return word, word_meaning, difficulty, space, index_of_space


def menu() -> int:
    """
    This function is the main menu of the game.

    Returns:
        user_input (int): The option chosen
    """
    while 1:
        os.system("cls")
        print("\n\n")
        t.sleep(0.1)
        hm_banner()  # ascii art
        t.sleep(0.05)
        print(
            s.pr_bold(
                "\n---------------------------- ~ MENU ~ -----------------------------\n"
            )
        )
        t.sleep(0.05)
        print(s.pr_bold("                        1. Start new game\n"))
        t.sleep(0.05)
        print(s.pr_bold("                        2. Print leaderboard\n"))
        t.sleep(0.05)
        print(s.pr_bold("                        3. Search player\n"))
        t.sleep(0.05)
        print(s.pr_bold("                        4. Exit\n"))
        user_input = input(">> ")
        check, err = validate_input(user_input=user_input, user_choice=2)
        if check:
            return int(user_input)
        input(f"{err}\nPress Enter to continue...")


def banner(game: object, session: int, user_choice: int) -> None:
    """
    This function prints the banner of the game.

    Args:
        game (object): This is the game object
        session (int): This is the session number
        choice (int): This is the choice of the player
    """
    if user_choice == 1:
        os.system("cls")
        print("Your word is " + str(len(game.word)) + " letters long. ")
    elif user_choice == 3:
        print("Session: " + str(session) + " / " + str(settings["attempts"]))
        if len(game.index_of_space) > 0:
            # replace the underscores with spaces
            new_guess_progress = game.guess_progress
            for i in game.index_of_space:
                new_guess_progress = (
                    new_guess_progress[: i * 2] + " " + new_guess_progress[i * 2 + 1 :]
                )
            print(f"Word: {new_guess_progress}")
        else:
            print("Word: " + game.guess_progress)
        print(
            f"Incorrect Guesses ({len(game.incorrect_list)}): {', '.join(game.incorrect_list)}"
        )
        print(
            f"Correct Guesses: {', '.join(list(set(game.previous_guesses) - set(game.incorrect_list)))}"
        )
        print("Guesses remaining: " + str(settings["guesses"] - game.guesses))
        print_hangman(guess_num=game.guesses)


def hm_banner() -> None:
    """
    This function prints the banner of the game.
    """
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


def print_hangman(guess_num: int) -> None:
    """
    This function prints the hangman ascii art.

    Arguments:
        guess_num {int}: This is the number of guesses the player has made

    """
    match guess_num:
        case 0:
            print(
                r"""            +---+
                |   |
                    |
                    |
                    |
                    |
                ========="""
            )
        case 1:
            print(
                r"""            +---+
                |   |
                O   |
                |   |
                    |
                    |
                ========="""
            )
        case 2:
            print(
                r"""            +---+
                |   |
                O   |
            /|   |
                    |
                    |
                ========="""
            )
        case 3:
            print(
                r"""            +---+
                |   |
                O   |
            /|\  |
                    |
                    |
                ========="""
            )
        case 4:
            print(
                r"""            +---+
                |   |
                O   |
            /|\  |
            /    |
                    |
                ========="""
            )
        case 5:
            print(
                r"""            +---+
                |   |
                O   |
            /|\  |
            / \  |
                    |
                ========="""
            )


def validate_input(user_input: str | int, user_choice: int) -> tuple[bool, str]:
    # checklist: 1.2 (validate all inputs)
    """
    _summary_

    Args:
        user_input (str/int): this is the user input, could be a string or an integer. name or option
        choice (int): this is the choice of validation. 1 for name, 2 for option, 3 for Y/N

    Returns:
        tuple(bool,str):
            bool: True if the input is valid, False if the input is invalid
            str: the error message if the input is invalid
    """
    if user_choice == 1:
        alphabets_lower = list(map(chr, range(97, 123)))
        alphabets_upper = list(map(chr, range(65, 91)))
        special_chars = ["-", "/", "!"]
        allowed_chars = alphabets_upper + alphabets_lower + special_chars
        if (
            not all(char in allowed_chars for char in user_input)
            or len(user_input) == 0
        ):
            return False, "Please enter a valid name. "
        if os.stat("../data/game_logs.txt").st_size != 0:
            with open("../data/game_logs.txt", "r") as f:
                game_log = ast.literal_eval(f.read())
                for value in game_log:
                    if value["player"].lower() == user_input.lower():
                        return False, "This name is already taken. "
        return True, None
    if user_choice == 2:
        if not user_input.isnumeric():
            return False, s.pr_red("Please enter a valid option.")
        options = [1, 2, 3, 4]
        for option in options:
            if int(user_input) == option:
                return True, None
        return False, s.pr_red("Please enter a valid option. ")
    if user_choice == 3:
        options = ["1", "2", "3"]
        if user_input not in options:
            return False, s.pr_red("Please enter a valid option. ")
        return True, None


def find_vowels(word: str) -> list:
    """
    This function finds the vowels in the word and returns a list of vowels.

    Arguments:
        word {str}: This is the word the player has to guess.

    Returns:
        list: This is a list of vowels in the word.
    """
    vowels = ["a", "e", "i", "o", "u"]
    vowel_list = []
    for char in word:
        if char in vowels:
            vowel_list.append(char)
    return vowel_list


def solve_vowels(game: object, vowels: list) -> None:
    """
    This function solves the vowels in the word.

    Args:
        game (object): This is the game object.
        vowels (vowels): This is a list of vowels in the word.
    """
    vowels_unique = []
    for vowel in vowels:
        if vowel not in vowels_unique:
            vowels_unique.append(vowel)
    for i in range(len(game.word)):
        for vowel in vowels_unique:
            if game.word[i] == vowel:
                before = game.guess_progress[: i * 2]
                after = game.guess_progress[i * 2 + 1 :]
                game.guess_progress = before + vowel + after
                game.previous_guesses.append(vowel)


def print_leaderboard(num: int) -> None:
    """
    _summary_

    Args:
        num (_type_): this is the number of players to be displayed in the leaderboard
    """

    def read_logs() -> dict:
        """
        This function reads the game logs and returns a dictionary of the logs

        Returns:
            logs (dict): this is the game log
        """
        try:
            with open("../data/game_logs.txt", "r") as f:
                logs = ast.literal_eval(f.read())
                return logs
        except FileNotFoundError:
            print("Error. Game logs not found. ")

    logs = read_logs()
    logs.sort(key=lambda x: x["points"], reverse=True)
    print(f"{PADDING}\n LEADERBOARD (Top {num})\n{PADDING}")
    for i, value in enumerate(logs):
        if i == num:
            break
        print(f"{i+1}. {value['player']} - {value['points']}")
    print(f"{PADDING}\n")


def search_player() -> None:
    """
    This function searches for a player in the game logs
    """

    def read_logs() -> dict:
        """
        This function reads the game logs and returns a dictionary of the logs

        Returns:
            logs (dict): this is the game log
        """
        try:
            with open("../data/game_logs.txt", "r") as f:
                logs = ast.literal_eval(f.read())
                return logs
        except FileNotFoundError:
            print("Error. Game logs not found. ")

    logs = read_logs()
    name = input("Enter player name: ")
    # checklist: 1. prompt for player name
    for item in logs:
        if item["player"].lower() == name.lower():
            print(f"{PADDING}\n{item['player']} - {['points']} points\n{PADDING}")
            return
    print(f"{PADDING}\nPlayer not found. \n{PADDING}")


def init_game_settings() -> object:
    """
    This function returns the game settings

    Returns:
        game_settings (object): the game settings
    """
    try:
        with open("../data/game_settings.txt") as f:
            game_settings = ast.literal_eval(f.read())
            game_settings["attempts"] = game_settings["number of attempts"]
            game_settings["guesses"] = game_settings["number of guesses"]
            game_settings["top"] = game_settings["number of top players"]
            # Completely unnecessary but good for my sanity
            del (
                game_settings["number of attempts"],
                game_settings["number of top players"],
                game_settings["number of guesses"],
            )
            return game_settings
    except FileNotFoundError:
        print("Error. game_settings.txt not found. ")
        return None


def main() -> None:
    """
    This is the main function
    """
    while 1:  # loops until check is true
        player_name = input("Enter your name: ")
        check, err = validate_input(user_input=player_name, user_choice=1)
        if check:
            begin(player_name=player_name)
            break
        print(err)


def begin(player_name: str) -> None:
    """
    this function begins the game

    Args:
        player_name (str): this is the player's name
    """
    global SESSION, lifeline_vowel, lifeline_meaning
    hang_man = Game(player_name)
    if SESSION == 1:
        banner(game=hang_man, session=SESSION, user_choice=1)
    while (hang_man.guesses < settings["guesses"]) and (
        (hang_man.guess_progress).replace(" ", "") != hang_man.word
    ):
        hang_man.calculate_points()
        banner(game=hang_man, session=SESSION, user_choice=3)
        guess = input("Guess ('0' to activate lifeline): ")
        if guess == "0":
            os.system("cls")
            temp_vowels = s.pr_green("Show Vowels")
            temp_meaning = s.pr_green("Show Meaning")
            if lifeline_vowel:
                temp_vowels = s.pr_red("Show Vowels")
            if lifeline_meaning:
                temp_meaning = s.pr_red("Show Meaning")
            print(
                f"{PADDING}\nLifelines: \n1. {temp_vowels}\n2. {temp_meaning}\n3. Back\n{PADDING}"
            )
            while 1:
                lifeline = input("Enter lifeline: ")
                check, err = validate_input(user_input=lifeline, user_choice=3)
                if check:
                    break
                print(err)
            if int(lifeline) == 1:
                if lifeline_vowel is True:
                    os.system("cls")
                    print(s.pr_red("You have already used this lifeline. "))
                    continue
                os.system("cls")
                vowels = find_vowels(hang_man.word)
                if len(vowels) == 0:
                    print(s.pr_red("No vowels found. "))
                else:
                    vowel_obj = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
                    for vowel in vowels:
                        vowel_obj[vowel] += 1
                    print(PADDING)
                    print(s.pr_green("\nVowels found! \n"))
                    # rewrite the following statements with .items()
                    for key, value in vowel_obj.items():
                        if value > 0:
                            print(f"{key} - {value}")
                    print(f"{PADDING}\n")
                    input("Press enter to continue. ")
                    solve_vowels(hang_man, vowels)
                    lifeline_vowel = True
                    os.system("cls")
            elif int(lifeline) == 2:
                if lifeline_meaning is True:
                    os.system("cls")
                    print(s.pr_red("You have already used this lifeline. "))
                    continue
                lifeline_meaning = True
                # print the meaning of the word
                os.system("cls")
                print(f"\n\n{PADDING}\n")
                print(f'The meaning of the word is: \n"{hang_man.meaning}"\n')
            elif int(lifeline) == 3:
                os.system("cls")
                continue
        else:
            hang_man.guess_letter(letter=guess)
        print(PADDING)
    if hang_man.guesses == settings["guesses"]:
        print(s.pr_red("\nYou have reached the maximum number of guesses. "))
    else:
        print(s.pr_green("\nWell Done! You have guessed the word. "))
    if hang_man.space is False:
        print(
            f"After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. \nThe word was \"{hang_man.word}\".\nIts meaning is: '{hang_man.meaning}'"
        )
    else:
        formatted_word = (hang_man.word).replace("_", " ")
        print(
            f"After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. \nThe word was \"{formatted_word}\".\nIts meaning is: '{hang_man.meaning}'"
        )
    if SESSION < settings["attempts"]:
        SESSION += 1
        log["points"] += hang_man.calculate_points()
        print(f"Your total points are {s.pr_bold(s = log['points'])}.\n")
        print(f"{PADDING}\n")
        input("Press enter to continue. ")
        os.system("cls")
        begin(player_name)
    else:
        if log["points"] > 15:
            print(PADDING2)
            print(f"Congratulations! You have {s.pr_green(s = 'won')} the game! ")
        else:
            print(PADDING2)
            print(f"You have {s.pr_red(s = 'lost')} the game. ")
        log["points"] += hang_man.calculate_points()
        log["player"] = (hang_man.player).capitalize()
        end_game(log_file=log)


if __name__ == "__main__":
    settings = init_game_settings()
    PADDING = "-" * 40
    PADDING2 = "=" * 40
    try:
        while 1:
            choice = menu()
            match choice:
                case 1:
                    lifeline_vowel = False
                    lifeline_meaning = False
                    SESSION = 1
                    previous_words = []
                    log = {
                        "player": "",
                        "points": 0,
                        "date": date.today().strftime("%d/%m/%y"),
                    }
                    main()
                case 2:
                    print_leaderboard(num=int(settings["top"]))
                case 3:
                    search_player()
                case 4:
                    sys.exit()
            input("Press Enter to continue...")
    except KeyboardInterrupt:
        print(s.pr_red(("\nThank you for playing. ")))
        sys.exit()
