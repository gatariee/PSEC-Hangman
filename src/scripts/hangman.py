import ast
import random
import json
import os
import sys
import time as t
from datetime import date
from styles import Styles as s
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
    session : int
        The number of the session
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
        Args:
            player (str): Input name of player
        """
        self.player = player
        self.session = session
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
        This function is called everything a guess is made and calculates the points earned.

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


def end_game(log: dict) -> None:
    with open("../data/game_logs.txt", "r+") as f:
        if os.stat("../data/game_logs.txt").st_size == 0:
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


def pick_word() -> tuple:
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
        global previous_words
        try:
            with open("../data/word_list.txt", "r") as f:
                wordlist = ast.literal_eval(f.read())
                return wordlist
        except:
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
                f"\n---------------------------- ~ MENU ~ -----------------------------\n"
            )
        )
        t.sleep(0.05)
        print(s.pr_bold(f"                        1. Start new game\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        2. Print leaderboard\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        3. Search player\n"))
        t.sleep(0.05)
        print(s.pr_bold(f"                        4. Exit\n"))
        user_input = input(">> ")
        check, err = validate_input(user_input=user_input, choice=2)
        if check:
            return int(user_input)
        input(f"{err}\nPress Enter to continue...")


def banner(game: object, session: int, choice: int) -> None:
    """
    This function prints the banner of the game.

    Args:
        game (object): This is the game object
        session (int): This is the session number
        choice (int): This is the choice of the player
    """
    if choice == 1:
        os.system("cls")
        print("Your word is " + str(len(game.word)) + " letters long. ")
    elif choice == 3:
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
            print(f"Word: " + game.guess_progress)
        print(
            f"Incorrect Guesses ({len(game.incorrect_list)}): {', '.join(game.incorrect_list)}"
        )
        print(
            f"Correct Guesses: {', '.join(list(set(game.previous_guesses) - set(game.incorrect_list)))}"
        )
        print("Guesses remaining: " + str(settings["guesses"] - game.guesses))
        print_hangman(guess_num=game.guesses)


def hm_banner():
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


def validate_input(user_input, choice: int) -> tuple:
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
            if os.stat("../data/game_logs.txt").st_size != 0:
                with open("../data/game_logs.txt", "r") as f:
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
    elif choice == 4:
        options = ['1','2','3']
        if user_input not in options:
            return False, s.pr_red("Please enter a valid option. ")
        else:
            return True, None



def find_vowels(word: str):
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
def solve_vowels(game, vowels):
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
    print(f"{padding}\n LEADERBOARD (Top {num})\n{padding}")
    for i in range(len(logs)):
        print(f"{i+1}. {logs[i]['player']} - {logs[i]['points']} points")
        if i == num - 1:
            break
    print(f"{padding}\n")


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
    for log in logs:
        if log["player"].lower() == name.lower():
            print(f"{padding}\n{log['player']} - {log['points']} points\n{padding}")
            return
    print(f"{padding}\nPlayer not found. \n{padding}")


def game_settings() -> object:
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
    """
    This is the main function
    """
    while 1:  # loops until check is true
        player_name = input("Enter your name: ")
        check, err = validate_input(user_input=player_name, choice=1)
        if check:
            begin(player_name=player_name)
            break
        else:
            print(err)


def begin(player_name: str) -> None:
    """
    this function begins the game

    Args:
        player_name (str): this is the player's name
    """
    global session
    global lifeline_vowel
    global lifeline_meaning
    hang_man = Game(player_name)
    if session == 1:
        banner(game=hang_man, session=session, choice=1)
    while (hang_man.guesses < settings["guesses"]) and (
        (hang_man.guess_progress).replace(" ", "") != hang_man.word
    ):
        hang_man.calculate_points()
        banner(game=hang_man, session=session, choice=3)
        guess = input("Guess ('0' to activate lifeline): ")
        if(guess == "0"):
            os.system('cls')
            print(f"{padding}\nLifelines: \n1. Show Vowels\n2. Show Meaning\n3. Quit\n{padding}")
            while(1):
                lifeline = input("Enter lifeline: ")
                check, err = validate_input(user_input=lifeline, choice=4)
                if check:
                    break
                else:
                    print(err)
            if int(lifeline) == 1:
                if lifeline_vowel == True:
                    os.system('cls')
                    print(s.pr_red("You have already used this lifeline. "))
                    continue
                os.system('cls')
                vowels = find_vowels(hang_man.word)
                if(len(vowels) == 0):
                    print(s.pr_red("No vowels found. "))
                else:
                    vowel_obj = {
                        "a" : 0,
                        "e" : 0,
                        "i" : 0,
                        "o" : 0,
                        "u" : 0
                    }
                    for vowel in vowels:
                        vowel_obj[vowel] += 1
                    print(f"{padding}\nVowels: ")
                    for vowel in vowel_obj:
                        if vowel_obj[vowel] != 0:
                            print(f"{vowel} - {vowel_obj[vowel]}")
                    input("Press enter to continue. ")
                    solve_vowels(hang_man, vowels)
                    lifeline_vowel = True
                    os.system('cls')
            elif int(lifeline) == 2:
                print('2')
                input("Press enter to continue. ")
            elif int(lifeline) == 3:
                print('3')
                input("Press enter to continue. ")
        else:
            hang_man.guess_letter(letter=guess)
        print(padding)
    if hang_man.guesses == settings["guesses"]:
        print(s.pr_red("\nYou have reached the maximum number of guesses. "))
    else:
        print(s.pr_green("\nWell Done! You have guessed the word. "))
    if hang_man.space == False:
        print(
            f"After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. \nThe word was \"{hang_man.word}\".\nIts meaning is: '{hang_man.meaning}'"
        )
    else:
        formatted_word = (hang_man.word).replace("_", " ")
        print(
            f"After {len(hang_man.incorrect_list)} incorrect guesses and {len(hang_man.previous_guesses)-len(hang_man.incorrect_list)} correct guesses. \nThe word was \"{formatted_word}\".\nIts meaning is: '{hang_man.meaning}'"
        )
    if session < settings["attempts"]:
        session += 1
        log["points"] += hang_man.calculate_points()
        print(f"Your total points are {s.pr_bold(s = log['points'])}.\n")
        print(f"{padding}\n")
        input("Press enter to continue. ")
        os.system("cls")
        begin(player_name)
    else:
        if log["points"] > 15:
            print(padding2)
            print(f"Congratulations! You have {s.pr_green(s = 'won')} the game! ")
        else:
            print(padding2)
            print(f"You have {s.pr_red(s = 'lost')} the game. ")
        log["points"] += hang_man.calculate_points()
        log["player"] = (hang_man.player).capitalize()
        end_game(log=log)


if __name__ == "__main__":
    settings = game_settings()
    padding = "-" * 40
    padding2 = "=" * 40
    try:
        while 1:
            choice = menu()
            match choice:
                case 1:
                    lifeline_vowel = False
                    lifeline_meaning = False
                    session = 1
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
                    exit()
            input("Press Enter to continue...")
    except KeyboardInterrupt:
        print(s.pr_red(("\nThank you for playing. ")))
        sys.exit()

    # Program Flow:

    # 1. User runs the program -> if(__name__ == "__main__"): main()
    # 2. User is prompted to login -> login() is called by main() which returns a boolean value and the number of attempts left
    # ^^ If login() returns True, the user is logged in and menu() is called, else the user is prompted to try again
    # 3. User is presented with the main menu -> menu() is called by main() which returns an integer value
    # 4. User is presented with the sub-menu for the option they chose
    # -> 1. word_menu(), 2. game_menu(), or 3. reports_menu()
    # 5. banner(x) is called by the sub-menu function to display the sub-menu

    """"
        Word Settings:                                  word_menu()
            1. Add word calls                               add_word()
            2. Remove word calls                            remove_word()
            3. Edit word calls                              edit_word()
            4. View words calls                             view_words()
            5. Reset words calls                            reset_words()
            6. Exit returns from word_menu() to             menu()
    
        Game Settings:                                  game_menu()
            1. Edit session calls                           edit_session()
            2. Edit guesses calls                           edit_guesses()
            3. Edit top calls                               edit_top()
            4. Exit returns from game_menu() to             menu()

        View reports:                                   reports_menu()
            1. Print top calls                              print_top()
            2. Search logs calls                            search_logs()
                2.1 Search by name calls                        search_by_name()
                2.2 Search by date calls                        search_by_date()
                2.3 Exit returns from search_logs() to          reports_menu()
            3. Exit returns from reports_menu() to          menu()

    """
