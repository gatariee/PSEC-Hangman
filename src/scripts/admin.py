import json
import os
import hashlib
import time as t
import datetime
import sys
from getpass import getpass
from styles import Styles as colours
COLORS = colours()
from banner import admin_banner as banner
class LoginManager:
    """
    A class that manages user login attempts.

    Args:
        attempts (int): The number of attempts allowed.

    """
    def __init__(self, attempts: int) -> None:
        self.attempts = attempts

    def check_login(self, input_username: str, input_password: str) -> bool:
        """
        Checks if the username and password are correct.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            bool: True if the username and password are correct, False otherwise.
        """
        # Read the list of admin users from file
        admins = read_file(file="../data/admin.txt")

        # Hash the password
        password = hashlib.sha256(input_password.encode()).hexdigest()

        # Check if the input username and password match an admin user
        for admin in admins:
            if admin["username"] == input_username and admin["password"] == password:
                return True

        # If no match was found, return False
        return False

    def login(self) -> bool:
        """
        Logs the user in.

        Returns:
            bool: True if the user has successfully logged in, False otherwise.
        """
        while(1):
            # Clear the screen
            os.system("cls")

            # Print the login banner
            print("\n\n")
            banner(6)

            # Ask the user for the username and password
            username = input(COLORS.pr_bold(s="Username: "))
            t.sleep(0.1)
            password = getpass(COLORS.pr_bold(s="Password: "))

            # Check if the login is successful
            if self.check_login(input_username=username, input_password=password):
                return True

            # If the login failed
            if self.attempts:
                # Print a message and reduce the number of attempts
                print(f"Invalid credentials. You have {self.attempts} attempts left.")
                input("Press enter to continue...")
                self.attempts -= 1
            else:
                # Exit
                print("You have exceeded the number of attempts allowed.")
                input("Press enter to continue...")
                return False
# General Functions
def read_file(file: str) -> list | None:
    """
    Reads a file and returns a list of the contents.

    Args:
        file (str): The file to be read.

    Returns:
        list: A list of the contents of the file.

    """
    try:
        # Check if the file is empty
        if os.stat(file).st_size == 0:
            raise FileNotFoundError
        # Read the file and return the contents as a list
        with open(file, "r") as f:
            return json.loads((f.read()))

    except FileNotFoundError:
        # If the file is not found, print an error message and return None
        return ""

def write_file(file: str, data: str) -> None:
    """
    Writes data to a file.

    Args:
        file (str): The file to be written to.
        data (str): The data to be written to the file.
    """
    try:
        with open(file, "w") as f:
            f.seek(0)
            f.truncate(0)
            # Write the data to the file
            f.write(str(data))
            return
    except FileNotFoundError:
        # If the file is not found, print an error message
        print("Error. File not found. ")
        return



def validate_input(userin: int | str, options: list | str) -> tuple[bool, str]:
    """
    Validates user input.

    Args:
        userin (int | str): The user input.
        options (_type_): The options to be validated against.

    Returns:
        tuple[bool, int]: A tuple containing a boolean value and an integer value.
        bool: True if the user input is valid, False otherwise.
        str: The error message input if return false, otherwise an empty string.
    """
    if options == "int":
        if not userin.isnumeric():
            return False, COLORS.pr_red(s="Invalid input. Please try again.")
        return True, ""
    if userin.isnumeric():
        if int(userin) not in options:
            return False, COLORS.pr_red(s="Invalid input. Please try again.")
        return True, ""
    if userin not in options:
        return False, COLORS.pr_red(s="Invalid input. Please try again.")
    return True, ""

################################################################
###                   1. Word Settings                       ###
################################################################
def add_word() -> None:
    """
    Adds a word to the word list.
    """
    def validate_word(word: str, option: int) -> bool:
        numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
        if(option == 1):
            if(word.startswith(" ") or word == ""):
                print("Word cannot start with a space.")
                input("Press enter to continue...")
                os.system('cls')
                return False
            for letter in word:
                if letter in numbers:
                    print("Word cannot contain numbers.")
                    input("Press enter to continue...")
                    os.system('cls')
                    return False
            return True
        if(option == 2):
            if meaning.startswith(" ") or meaning == "":
                print("Meaning cannot start with a space.")
                input("Press enter to continue...")
                os.system('cls')
                return False
            for letter in meaning:
                if letter in numbers:
                    print("Meaning cannot contain numbers.")
                    input("Press enter to continue...")
                    os.system('cls')
                    return False
            return True
    while(1):
        word = input('Enter Word ("0" to exit): ').lower()
        if word == "0":
            return
        if validate_word(word, 1):
            break
    if " " in word:
        word_type = "Idioms-Proverbs"
        if len(word.split()) > 8:
            diff = "Complex"
        else:
            diff = "Simple"
    else:
        word_type = "Word"
        if len(word) > 8:
            diff = "Complex"
        else:
            diff = "Simple"
    while(1):
        meaning = input("Enter Meaning: ").lower()
        if validate_word(meaning, 2):
            break
    new_word = {
        "word": word,
        "meaning": meaning,
        "difficulty": diff,
        "type": word_type,
        "enabled": "on",
    }
    if os.stat("../data/word_list.txt").st_size == 0:
        obj = []
        obj.append(new_word)
    else:
        obj = read_file(file="../data/word_list.txt")
        for item in obj:
            if item["word"] == word:
                print("Word already exists.")
                input("Press enter to continue...")
                return
        obj.append(new_word)
    new = json.dumps(obj, indent=4)
    write_file(file = "../data/word_list.txt", data = new)
    os.system("cls")
    print((f"Successfully added \"{COLORS.pr_bold(new_word['word'])}\" to the word list."))
    print(PADDING * 2)
    print(f"The following attributes have been automatically added to the word: \n")
    print(f"\tDifficulty: {COLORS.pr_bold(new_word['difficulty'])}")
    print(f"\tType: {COLORS.pr_bold(new_word['type'])}\n")
    print(PADDING * 2)
    input("Press Enter to continue...")


def remove_word() -> None:
    """
    Removes a word from the word list.
    """
    obj = read_file(file="../data/word_list.txt")
    while 1:
        check, index = False, 0
        os.system("cls")
        print(PADDING * 4 + "\n")
        for i, item in enumerate(obj):
            print(f"{i + 1}. {item['word']}")
        word = input(
            f"\n{PADDING*4}\nEnter the word you want to remove ('0' to exit):  "
        )
        if word.isnumeric():
            check, index = (
                (True, int(word) - 1) if (0 < int(word) <= len(obj)) else (False, 0)
            )
        for i, item in enumerate(obj):
            if item["word"].lower() == word.lower() or check:
                if index != 0:
                    i = index
                print(f"{obj[i]['word']} has been removed from the word list.")
                input("Press enter to continue...")
                obj.pop(i)
                new = json.dumps(obj, indent=4)
                write_file(file = "../data/word_list.txt", data = new)
                return
        if word == "0":
            return
        print("Word not found. Please try again.")
        input("Press Enter to continue...")


def edit_word() -> None:
    """
    Edits a word in the word list.
    """
    obj = read_file(file="../data/word_list.txt")
    while 1:
        check, index = False, 0
        os.system("cls")
        print(PADDING * 2 + "\n")
        for i, item in enumerate(obj):
            print(f"{i + 1}. {item['word']}")
        word = input(f"\n{PADDING*2}\nEnter the word you want to edit ('0' to exit):  ")
        if word.isnumeric():
            check, index = (
                (True, int(word) - 1) if (0 < int(word) <= len(obj)) else (False, 0)
            )
        for i in range(len(obj)):
            if (obj[i]["word"] == word.lower()) or check:
                while 1:
                    os.system("cls")
                    if index != 0:
                        i = index
                    print(PADDING * 2)
                    print("\n\tCurrent word: ", obj[i]["word"])
                    print("\tCurrent meaning: ", obj[i]["meaning"])
                    print("\tCurrent type: ", obj[i]["type"])
                    print("\tCurrent difficulty: ", obj[i]["difficulty"] + "\n")
                    print(PADDING * 2)
                    print(f"\n{COLORS.pr_bold('1')}: Edit word")
                    print(f"{COLORS.pr_bold('2')}: Edit meaning")
                    print(f"{COLORS.pr_bold('3')}: Edit difficulty")
                    print(f"{COLORS.pr_bold('4')}: Save and exit")
                    choice = input(">> ")
                    print(PADDING)
                    if choice == "1":
                        temp_word = input("Enter new word: ").lower()
                        if(" " in temp_word):
                            obj[i]["type"] = "Idioms-Proverbs"
                            if len(temp_word.split()) > 8:
                                obj[i]["difficulty"] = "Complex"
                            else:
                                obj[i]["difficulty"] = "Simple"
                        else:
                            obj[i]["type"] = "Word"
                            if len(temp_word) > 8:
                                obj[i]["difficulty"] = "Complex"
                            else:
                                obj[i]["difficulty"] = "Simple"
                        obj[i]["word"] = temp_word
                    elif choice == "2":
                        obj[i]["meaning"] = input("Enter new meaning: ")
                    elif choice == "3":
                        obj[i]["difficulty"] = input("Enter new difficulty: ")
                    elif choice == "4":
                        break
                    else:
                        print("Invalid input. Please try again.")
                        input("Press Enter to continue...")
                print(
                    f"These are the new values\n\tWord: {obj[i]['word']}\n\tType: {obj[i]['meaning']}\n\tDifficulty: {obj[i]['difficulty']}"
                )
                new = json.dumps(obj, indent=4)
                write_file(file = "../data/word_list.txt", data = new)
                return
        if word == "0":
            return
        print("Word not found. Please try again.")
        input("Press Enter to continue...")


def view_words() -> None:
    """
    Displays all the words in the word list.
    """
    os.system('cls')
    try:
        if os.stat("../data/word_list.txt").st_size == 0:
            print("Wordist is empty.")
            input("Press Enter to continue...")
            return
        obj = read_file(file="../data/word_list.txt")
        print(f"There are currently {len(obj)} words in the word list.\n")
        print(PADDING * 4 + "\n")
        for i in range(len(obj)):
            if obj[i]["enabled"] == "on":
                print(COLORS.pr_green((f"\t{COLORS.pr_bold(i+1)}: {obj[i]['word']}")))
            else:
                print(COLORS.pr_red((f"\t{COLORS.pr_bold(i+1)}: {obj[i]['word']}")))
        print(f"\n{PADDING * 4}\n")
    except FileNotFoundError:
        print("Error. Please contact an administrator")
        return
    input("Press Enter to continue...")


def reset_words() -> None:
    """
    Resets the word list to empty
    """
    y_n = input("Are you sure you want to reset the word list? (Y/y to confirm)): ")
    if y_n.lower() == "y":
        try:
            with open("../data/word_list.txt", "w") as f:
                f.truncate(0)
                f.close()
                print("Successfully reset word list.")
                input("Press Enter to continue...")
                return
        except FileNotFoundError:
            print("Error. Wordlist not found. ")
            return
    else:
        print("Cancelling...")
        input("Press Enter to continue...")


def status_menu() -> None:
    """
    Displays the status menu.
    """
    while 1:
        os.system("cls")
        # print list of words but only showing enabled and type
        obj = read_file(file="../data/word_list.txt")
        print(PADDING * 4 + "\n")
        enabled_counter = 0
        disabled_counter = 0
        for i in range(len(obj)):
            if obj[i]["enabled"] == "on":
                enabled_counter += 1
                print(COLORS.pr_green((f"\t{COLORS.pr_bold(i+1)}: {obj[i]['word']}")))
            else:
                disabled_counter += 1
                print(COLORS.pr_red((f"\t{COLORS.pr_bold(i+1)}: {obj[i]['word']}")))
        print(f"\n{COLORS.pr_bold('Enabled')}: {enabled_counter}")
        print(f"{COLORS.pr_bold('Disabled')}: {disabled_counter}")
        print(f"\n{PADDING * 4}\n")
        print(f"{COLORS.pr_bold('1')}: Toggle Words")
        t.sleep(0.05)
        print(f"{COLORS.pr_bold('2')}: Toggle Idiom-Proverbs")
        t.sleep(0.05)
        print(f"{COLORS.pr_bold('3')}: Toggle Specific")
        t.sleep(0.05)
        print(f"{COLORS.pr_bold('4')}: Back")
        t.sleep(0.05)
        choice = input(">> ")
        check, err = validate_input(userin = choice, options = [1, 2, 3, 4])
        if check:
            choice = int(choice)
            match choice:
                case 1:
                    toggle_words()
                case 2:
                    toggle_idioms()
                case 3:
                    toggle_specific()
                case 4:
                    return
                case _:
                    print("Invalid input. Please try again.")
                    input("Press Enter to continue...")
        else:
            print(err)
            input("Press Enter to continue...")


def toggle_words() -> None:
    """
    Toggles the status of all words.
    """
    obj = read_file(file="../data/word_list.txt")
    for i in range(len(obj)):
        if obj[i]["type"] == "Word":
            if obj[i]["enabled"] == "on":
                obj[i]["enabled"] = "off"
            else:
                obj[i]["enabled"] = "on"
    new = json.dumps(obj, indent=4)
    write_file(file = "../data/word_list.txt", data = new)


def toggle_idioms() -> None:
    """
    Toggles the status of all idioms and proverbs.
    """
    obj = read_file(file="../data/word_list.txt")
    for i in range(len(obj)):
        if obj[i]["type"] == "Idioms-Proverbs":
            if obj[i]["enabled"] == "on":
                obj[i]["enabled"] = "off"
            else:
                obj[i]["enabled"] = "on"
    new = json.dumps(obj, indent=4)
    write_file(file = "../data/word_list.txt", data = new)


def toggle_specific() -> None:
    """
    Toggles the status of a specific word.
    """
    obj = read_file(file="../data/word_list.txt")
    user_input = input("Enter index of word to toggle: ")
    options = [i for i in range(1, len(obj) + 1)]
    check, err = validate_input(userin = user_input, options = "int")
    if check:
        user_input = int(user_input)
        if user_input in options:
            if obj[user_input - 1]["enabled"] == "on":
                obj[user_input - 1]["enabled"] = "off"
            else:
                obj[user_input - 1]["enabled"] = "on"
            new = json.dumps(obj, indent=4)
            write_file(file = "../data/word_list.txt", data = new)
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
    else:
        print(err)
        input("Press Enter to continue...")
###############################################################
###                   2. Game Settings                      ###
###############################################################
def edit_session() -> None:
    """
    Edit the number of sessions
    """
    settings = read_file(file="../data/game_settings.txt")
    while 1:
        os.system("cls")
        print(
            f"{PADDING}\nCurrent number of sessions: {settings['number of sessions']}\n{PADDING}"
        )
        session = input("Enter new number of sessions: ")
        check, err = validate_input(userin = session, options = "int")
        if check:
            settings["number of sessions"] = int(session)
            new = json.dumps(settings, indent=4)
            write_file(file = "../data/game_settings.txt", data = new)
            print(COLORS.pr_green("Successfully updated number of sessions."))
            input("Press Enter to continue...")
            break
        print(err)
        input("Press Enter to continue...")


def edit_guesses() -> None:
    """
    Edit the number of guesses per session.
    """
    settings = read_file(file="../data/game_settings.txt")
    while 1:
        os.system("cls")
        print(
            f"{PADDING}\nCurrent number of guesses: {settings['number of guesses']}\n{PADDING}"
        )
        guesses = input("Enter new number of guesses: ")
        check, err = validate_input(userin = guesses, options = "int")
        if check:
            settings["number of guesses"] = int(guesses)
            new = json.dumps(settings, indent=4)
            write_file(file = "../data/game_settings.txt", data = new)
            print(COLORS.pr_green("Successfully updated number of guesses."))
            input("Press Enter to continue...")
            break
        print(err)
        input("Press Enter to continue...")


def edit_top() -> None:
    """
    Edit the number of top scores to display.
    """
    settings = read_file(file="../data/game_settings.txt")
    while 1:
        os.system("cls")
        print(
    f"{PADDING}\nCurrent number of top scores: {settings['number of top players']}\n{PADDING}"
        )
        top = input("Enter new number of top scores: ")
        check, err = validate_input(userin = top, options = "int")
        if check:
            settings["number of top players"] = int(top)
            new = json.dumps(settings, indent=4)
            write_file(file = "../data/game_settings.txt", data = new)
            print(COLORS.pr_green("Successfully updated number of top scores."))
            input("Press Enter to continue...")
            break
        print(err)
        input("Press Enter to continue...")


###############################################################
###                   3. View Reports                       ###
###############################################################
def print_top() -> None:
    """
    Prints the top scores.
    """
    os.system("cls")
    logs = read_file(file = "../data/game_logs.txt")
    if(len(logs) == 0):
        print(f"\n{PADDING*3} No logs found. {PADDING*3}\n")
        input("Press Enter to continue...")
        return
    logs.sort(key=lambda x: x["points"], reverse=True)
    print(f"{PADDING*3}")
    print(f"\t{COLORS.pr_bold('Rank')}\t\t{COLORS.pr_bold('Name')}\t\t{COLORS.pr_bold('Points')}")
    print(f"{PADDING*3}")
    for i, log in enumerate(logs, start=1):
        print(f"\t{COLORS.pr_bold(i)}\t\t{log['player']}\t\t{log['points']}")
    print(f"\n{PADDING * 3}\n")
    input("Press Enter to continue...")


def search_logs() -> None:
    """
    Prints the various options to search the logs.
    """
    while 1:
        os.system("cls")
        print(f"{PADDING*2}\n")
        print(f"\t{COLORS.pr_bold('1')}: Search by name")
        print(f"\t{COLORS.pr_bold('2')}: Search by date")
        print(f"\t{COLORS.pr_bold('3')}: Back")
        print(f"\n{PADDING*2}\n")
        choice = input(">> ")
        if choice == "1":
            search_name()
        elif choice == "2":
            search_date()
        elif choice == "3":
            break
        else:
            print(COLORS.pr_red("Invalid input. Please try again."))
            input("Press Enter to continue...")


def search_name() -> None:
    """
    Search the logs by name.
    """
    logs = read_file(file = "../data/game_logs.txt")
    name = input("Enter name: ")
    for log in logs:
        if log["player"].lower() == name.lower():
            print(f"{PADDING*2}\n")
            print(f"\t{COLORS.pr_bold('Name')}: {log['player']}")
            print(f"\t{COLORS.pr_bold('Points')}: {log['points']}")
            print(f"\t{COLORS.pr_bold('Date')}: {log['date']}")
            print(f"\n{PADDING*2}\n")
            input("Press Enter to continue...")
            return
    print("Player not found.")
    input("Press Enter to continue...")


def search_date() -> None:
    """
    Search the logs by date.
    """
    start_date = input("Enter start date (dd/mm/yy): ")
    end_date = input("Enter end date (dd/mm/yy): ")
    if start_date > end_date:
        print("Start date can not be larger than end date.")
        input("Press Enter to continue...")
        return
    if (start_date == end_date) or (start_date == "" and end_date == ""):
        print("Invalid date range.")
        input("Press Enter to continue...")
        return
    try:
        list_of_players = []
        os.system("cls")
        start_date_ugly = datetime.datetime.strptime(start_date, "%d/%m/%y")
        end_date_ugly = datetime.datetime.strptime(end_date, "%d/%m/%y")
        logs = read_file(file = "../data/game_logs.txt")
        if logs is None:
            return
        for player in logs:
            date = datetime.datetime.strptime(player["date"], "%d/%m/%y")
            if start_date_ugly <= date <= end_date_ugly:
                list_of_players.append(player)
        if len(list_of_players) == 0:
            print("No results found.")
        else:
            print(
                f"\nShowing {len(list_of_players)} results between {start_date} and {end_date}..."
            )
            print(f"{PADDING*3}")
            print(
                f"\t{COLORS.pr_bold('Name')}\t\t{COLORS.pr_bold('Points')}\t\t{COLORS.pr_bold('Date')}\n"
            )
            for player in list_of_players:
                print(
                    f"\t{player['player']}\t\t{player['points']}\t\t{player['date']}\n"
                )
            print(f"{PADDING*3}")
        input("Press Enter to continue...")
    except ValueError:
        print("Error. Invalid date format. ")
        input("Press Enter to continue...")


def remove_log() -> None:
    """
    Remove a log from the logs.
    """
    logs = read_file(file = "../data/game_logs.txt")
    while 1:
        os.system('cls')
        print(f"\n{PADDING*2}")
        print("List of Players:")
        print(f"{PADDING*2}\n")
        for i, log in enumerate(logs, start=1):
            print(f"\t{COLORS.pr_bold(i)}: {log['player']}")
        print(f"\n{PADDING*2}\n")
        name = input("Enter player number to remove (0) to exit: ")
        if name == "0":
            break
        check, err = validate_input(userin = name, options = "int")
        if check:
            name = int(name)
            if name > len(logs):
                print(COLORS.pr_red("Please enter a number within range. "))
                input("Press Enter to continue...")
            else:
                print(COLORS.pr_green(f"Successfully removed {logs[name-1]['player']}"))
                del logs[name - 1]
                new = json.dumps(logs, indent=4)
                write_file(file = "../data/game_logs.txt", data = new)
                input("Press Enter to continue...")
                break
        else:
            print(err)
            input("Press Enter to continue...")
            os.system('cls')


###############################################################
###                   4. Admin Settings                     ###
###############################################################
def add_admin() -> None:
    """
    Add an admin to the admin list.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    ##
    numbers = "1234567890"
    sp_chars = "!@#$%"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    num_string = f"Contains at least one number {COLORS.pr_red('✘')}"
    sp_string = f"Contains at least one special character {COLORS.pr_red('✘')}"
    len_string = f"Contains between 4 and 20 characters {COLORS.pr_red('✘')}"
    upper_string = f"Contains at least one uppercase letter {COLORS.pr_red('✘')}"
    lower_string = f"Contains at least one lowercase letter {COLORS.pr_red('✘')}"
    check_lowercase = False
    check_uppercase = False
    check_sp = False
    check_len = False
    checknum = False
    ##
    if 4 < len(password) < 20:
        check_len = True
        len_string = f"Contains between 4 and 20 characters {COLORS.pr_green('✔')}"
    for i in password:
        if i in numbers:
            checknum = True
            num_string = f"Contains at least one number {COLORS.pr_green('✔')}"
        if i in sp_chars:
            check_sp = True
            sp_string = f"Contains at least one special character {COLORS.pr_green('✔')}"
        if i in uppercase:
            check_uppercase = True
            upper_string = f"Contains at least one uppercase letter {COLORS.pr_green('✔')}"
        if i in lowercase:
            check_lowercase = True
            lower_string = f"Contains at least one lowercase letter {COLORS.pr_green('✔')}"
    if not (
        checknum and check_sp and check_len and check_uppercase and check_lowercase
    ):
        os.system("cls")
        print("Password does not meet requirements.")
        print(PADDING * 3)
        print(
            len_string
            + "\n"
            + num_string
            + "\n"
            + sp_string
            + "\n"
            + upper_string
            + "\n"
            + lower_string
        )
        print(PADDING * 3)
        input("Press Enter to continue...")
        return

    if username == "" or password == "":
        print("Error. Username or password cannot be empty.")
        input("Press Enter to continue...")
        return
    admins = read_file(file = "../data/admin.txt")
    for admin in admins:
        if admin["username"] == username:
            print("Error. Username already exists.")
            input("Press Enter to continue...")
            return
    password = hashlib.sha256(password.encode()).hexdigest()
    admins.append({"username": username, "password": password})
    new = json.dumps(admins, indent=4)
    write_file(file = "../data/admin.txt", data = new)
    os.system("cls")
    print(COLORS.pr_green(f"Successfully added '{username}' as admin."))
    input("Press Enter to continue...")


def remove_admin() -> None:
    """
    Remove an admin from the admin list.
    """
    username = input("Enter username: ")
    admins = read_file(file = "../data/admin.txt")
    for admin in admins:
        if admin["username"] == username:
            admins.remove(admin)
            new = json.dumps(admins, indent=4)
            write_file(file = "../data/admin.txt", data = new)
            os.system("cls")
            print(COLORS.pr_green(f"Successfully removed '{username}' as admin."))
            input("Press Enter to continue...")
            return
    print("Error. Username not found.")
    input("Press Enter to continue...")


def view_admins() -> None:
    """
    View all admins.
    """
    admins = read_file(file = "../data/admin.txt")
    if len(admins) == 0:
        print("No admins found.")
        input("Press Enter to continue...")
    else:
        os.system("cls")
        print(f"\nShowing {len(admins)} admins...")
        print(f"{PADDING*4}")
        print(f"\t{COLORS.pr_bold('Username')}\t\t{COLORS.pr_bold('Password (hashed)')}\n")
        for admin in admins:
            print(f"\t{admin['username']}\t\t{admin['password']}\n")
        print(f"{PADDING*4}")
        input("Press Enter to continue...")


###############################################################
###                          MENU                           ###
###############################################################
def menu() -> int:
    """
    Display the main menu.

    Returns:
        int: The option selected by the user.
    """
    while 1:
        os.system("cls")
        print("\n\n\n")
        banner(2)
        print(COLORS.pr_bold((f"{PADDING * 1} ~ MENU ~ {PADDING * 1}\n")))
        t.sleep(0.05)
        print(f"\t\t{COLORS.pr_bold('1')}: Word Settings")
        t.sleep(0.05)
        print(f"\t\t{COLORS.pr_bold('2')}: Game Settings")
        t.sleep(0.05)
        print(f"\t\t{COLORS.pr_bold('3')}: View Reports")
        t.sleep(0.05)
        print(f"\t\t{COLORS.pr_bold('4')}: Admin Settings")
        print(
            f"\t\t{COLORS.pr_bold('5')}: Exit\n\n{COLORS.pr_bold(PADDING * 2 + '==========')}\n"
        )
        t.sleep(0.05)
        user_input = input(">> ")
        check, err = validate_input(userin = user_input, options = [1, 2, 3, 4, 5])
        if check:
            return int(user_input)
        print(err)
        input("Press Enter to continue...")


def word_menu() -> None:
    """
    Display the word menu.
    """
    while 1:
        banner(1)
        choice = input(">> ")
        check, err = validate_input(userin = choice, options = [1, 2, 3, 4, 5, 6, 7])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            match choice:
                case 1:
                    add_word()
                case 2:
                    remove_word()
                case 3:
                    edit_word()
                case 4:
                    view_words()
                case 5:
                    reset_words()
                case 6:
                    status_menu()
                case 7:
                    return
                case _:
                    print("Invalid input. Please try again.")
                    input("Press Enter to continue...")


def game_menu() -> None:
    """
    Display the game menu.
    """
    while 1:
        banner(3)
        choice = input(">> ")
        check, err = validate_input(userin = choice, options = [1, 2, 3, 4])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            match choice:
                case 1:
                    edit_session()
                case 2:
                    edit_guesses()
                case 3:
                    edit_top()
                case 4:
                    return
                case _:
                    print("Invalid input. Please try again.")
                    input("Press Enter to continue...")


def reports_menu() -> None:
    """
    Display the reports menu.
    """
    while 1:
        banner(4)
        choice = input(">> ")
        check, err = validate_input(userin = choice, options = [1, 2, 3, 4])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            match choice:
                case 1:
                    print_top()
                case 2:
                    search_logs()
                case 3:
                    remove_log()
                case 4:
                    return
                case _:
                    print("Invalid input. Please try again.")
                    input("Press Enter to continue...")


def admin_menu() -> None:
    """
    Display the admin menu.
    """
    while 1:
        banner(5)
        choice = input(">> ")
        check, err = validate_input(userin = choice, options = [1, 2, 3, 4])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            match choice:
                case 1:
                    add_admin()
                case 2:
                    remove_admin()
                case 3:
                    view_admins()
                case 4:
                    return
                case _:
                    print("Invalid input. Please try again.")
                    input("Press Enter to continue...")


###############################################################
###                          MAIN                           ###
###############################################################
def main() -> None:
    """
    This begins the program
    """
    # Change directory to the directory of the script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # start the login, if attempts are exceeded, exit
    login_session = LoginManager(attempts = 3)
    if not login_session.login():
        print(COLORS.pr_red(("\nExiting...")))
        sys.exit()
    while 1:
        choice = menu()
        match choice:
            case 1:
                word_menu()
            case 2:
                game_menu()
            case 3:
                reports_menu()
            case 4:
                admin_menu()
            case 5:
                print("Exiting...")
                sys.exit()
            case _:
                print(COLORS.pr_red(("Invalid input. Please try again.")))
                input("Press Enter to continue...")


if __name__ == "__main__":
    os.system("cls")
    try:
        PADDING = "=" * 25
        main()
    except KeyboardInterrupt:
        print(COLORS.pr_red(("\nExiting...")))
        sys.exit()





































































































