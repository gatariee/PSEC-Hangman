import ast
import json
import os
import hashlib
import time as t
from styles import Styles as s
def banner(num):
    if num == 1:
        os.system("cls")
        print(s.pr_bold((f"{padding} ~ MENU ~ {padding}\n")))
        print(
            f"\t\tYou have selected: {s.pr_bold('Word Settings')}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f"\t\t\t{s.pr_bold('1')}: Add word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('2')}: Remove word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('3')}: Edit word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('4')}: View wordlist")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('5')}: {s.pr_red('*** Reset Words ***')}")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('6')}: Back")
    elif num == 2:

        print(
            s.pr_green(
                (
                    r""" █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗    ██████╗  █████╗ ███╗   ██╗███████╗██╗     
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║    ██████╔╝███████║██╔██╗ ██║█████╗  ██║     
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║    ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║    ██║     ██║  ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                                      """
                )
            )
        )
    elif num == 3:
        try:
            with open("game_settings.txt", "r") as f:
                obj = ast.literal_eval(f.read())
        except FileNotFoundError:
            print("Error. Settings not found. ")
        os.system("cls")
        print(s.pr_bold((f"\n\n\n{padding} ~ MENU ~ {padding}\n")))
        print(f"\tYou have selected: {s.pr_bold('Game Settings')}\n")
        t.sleep(0.05)
        print(f"\t\tNumber of sessions: {s.pr_bold(obj['number of attempts'])}")
        t.sleep(0.05)
        print(
            f"\t\tNumber of guesses per session: {s.pr_bold(obj['number of guesses'])}"
        )
        t.sleep(0.05)
        print(
            f"\t\tNumber of top players on leaderboard: {s.pr_bold(obj['number of top players'])}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f" {s.pr_bold('1')}: Edit number of sessions")
        t.sleep(0.05)
        print(f" {s.pr_bold('2')}: Edit number of attempts/guesses")
        t.sleep(0.05)
        print(f" {s.pr_bold('3')}: Edit number of top players")
        t.sleep(0.05)
        print(f" {s.pr_bold('4')}: Back\n")
    elif num == 4:
        os.system("cls")
        print(s.pr_bold((f"{padding} ~ MENU ~ {padding}\n")))
        print(
            f"\tYou have selected: {s.pr_bold('View Reports')}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f"\t\t{s.pr_bold('1')}: Print Leaderboard")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('2')}: Report Settings")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('3')}: Back")
#######
def add_word() -> None:
    word = input('Enter Word ("0" to exit): ').lower()
    if word == "0":
        return
    if len(word) <= 4:
        diff = "easy"
    elif len(word) <= 7:
        diff = "medium"
    else:
        diff = "hard"
    new_word = {"word": word, "type": input("Enter Type: ").lower(), "difficulty": diff}
    with open("word_list.txt", "r+") as f:
        if os.stat("word_list.txt").st_size == 0:
            obj = []
            obj.append(new_word)
        else:
            obj = ast.literal_eval(f.read())
            for i in range(len(obj)):
                if obj[i]["word"] == word:
                    print(padding)
                    print("Word already exists!")
                    return
            obj.append(new_word)
        new = json.dumps(obj, indent=4)
        f.seek(0)
        f.truncate(0)
        f.write(str(new))
        f.close()
        print(f"Successfully added {new_word['word']} to the word list.")
        input("Press Enter to continue...")
def remove_word() -> None:
    with open("word_list.txt", "r+") as f:
        obj = ast.literal_eval(f.read())
        while 1:
            check, index = False, 0
            os.system("cls")
            print(padding * 2 + "\n")
            for i in range(len(obj)):
                print(f"\t\t{s.pr_bold(i+1)}: {obj[i]['word']}")
            word = input(
                f"\n{padding*2}\nEnter the word you want to remove ('0' to exit):  "
            )
            if word.isnumeric():
                check, index = (True, int(word) - 1) if (0 < int(word) <= len(obj)) else (False, 0)
            for i, word in enumerate(obj):
                if word["word"].lower() == word.lower() or check:
                    if index != 0:
                        i = index
                    print(f"{obj[i]['word']} has been removed from the word list.")
                    input("Press enter to continue...")
                    obj.pop(i)
                    new = json.dumps(obj, indent=4)
                    f.seek(0)
                    f.truncate(0)
                    f.write(str(new))
                    f.close()
                    return
            if word == "0":
                return
            else:
                print("Word not found. Please try again.")
                input("Press Enter to continue...")
def edit_word() -> None:
    try:
        with open("word_list.txt", "r+") as f:
            obj = ast.literal_eval(f.read())
            f.close()
    except FileNotFoundError:
        print("Error. Wordlist not found. ")
        return
    while 1:
        check, index = False, 0
        os.system("cls")
        print(padding * 2 + "\n")
        for i in range(len(obj)):
            print(f"\t\t{s.pr_bold(i+1)}: {obj[i]['word']}")
        word = input(
            f"\n{padding*2}\nEnter the word you want to remove ('0' to exit):  "
        )
        if word.isnumeric():
            check, index = (True, int(word) - 1) if (0 < int(word) <= len(obj)) else (False, 0)
        for i in range(len(obj)):
            if (obj[i]["word"] == word.lower()) or check:
                while 1:
                    if index != 0:
                        i = index
                    print(padding * 2)
                    print("\n\tCurrent word: ", obj[i]["word"])
                    print("\tCurrent type: ", obj[i]["type"])
                    print("\tCurrent difficulty: ", obj[i]["difficulty"] + "\n")
                    print(padding * 2)
                    print(f"\n{s.pr_bold('1')}: Edit word")
                    print(f"{s.pr_bold('2')}: Edit type")
                    print(f"{s.pr_bold('3')}: Edit difficulty")
                    print(f"{s.pr_bold('4')}: Save and exit")
                    choice = input(">> ")
                    print(padding)
                    if choice == "1":
                        obj[i]["word"] = input("Enter new word: ")
                    elif choice == "2":
                        obj[i]["type"] = input("Enter new type: ")
                    elif choice == "3":
                        obj[i]["difficulty"] = input("Enter new difficulty: ")
                    elif choice == "4":
                        break
                    else:
                        print("Invalid input. Please try again.")
                        input("Press Enter to continue...")
                print(f"These are the new values\n\tWord: {obj[i]['word']}\n\tType: {obj[i]['type']}\n\tDifficulty: {obj[i]['difficulty']}")
                new = json.dumps(obj, indent=4)
                with open("word_list.txt", "w") as f:
                    f.seek(0)
                    f.truncate(0)
                    f.write(str(new))
                    f.close()
                return
        if word == "0":
            return
        else:
            print("Word not found. Please try again.")
            input("Press Enter to continue...")
def view_words() -> None:
    try:
        with open("word_list.txt", "r") as f:
            obj = ast.literal_eval(f.read())
            print(f"There are currently {len(obj)} words in the word list.\n")
            print(padding * 2 + "\n")
            for i in range(len(obj)):
                print(f"\t\t{s.pr_bold(i+1)}: {obj[i]['word']}")
            print(f"\n{padding * 2}\n")
    except FileNotFoundError:
        print("Error. Wordlist is empty or not found. ")
        return
    input("Press Enter to continue...")
def reset_words() -> None:
    try:
        with open("word_list.txt", "w") as f:
            f.truncate(0)
            f.close()
            print("Successfully reset word list.")
            return
    except FileNotFoundError:
        print("Error. Wordlist not found. ")
        return
#######
def read_settings() -> dict:
    try:
        with open("game_settings.txt", "r") as f:
            obj = ast.literal_eval(f.read())
            return obj
    except FileNotFoundError:
        print("Error. Settings not found. ")
def write_settings(obj) -> None:
    try:
        with open("game_settings.txt", "w") as f:
            new = json.dumps(obj, indent=4)
            f.seek(0)
            f.truncate(0)
            f.write(str(new))
            f.close()
            return
    except FileNotFoundError:
        print("Error. Settings not found. ")
        return
def edit_session() -> None:
    settings = read_settings()
    while 1:
        os.system("cls")
        print(
            f"{padding}\nCurrent number of sessions: {settings['number of attempts']}\n{padding}"
        )
        session = input("Enter new number of sessions: ")
        check, err = validate_input(session, "int")
        if check:
            settings["number of attempts"] = int(session)
            write_settings(settings)
            print(s.pr_green("Successfully updated number of sessions."))
            input("Press Enter to continue...")
            break
        else:
            print(err)
            input("Press Enter to continue...")
def edit_guesses() -> None:
    settings = read_settings()
    while 1:
        os.system("cls")
        print(
            f"{padding}\nCurrent number of guesses: {settings['number of guesses']}\n{padding}"
        )
        guesses = input("Enter new number of guesses: ")
        check, err = validate_input(guesses, "int")
        if check:
            settings["number of guesses"] = int(guesses)
            write_settings(settings)
            print(s.pr_green("Successfully updated number of guesses."))
            input("Press Enter to continue...")
            break
        else:
            print(err)
            input("Press Enter to continue...")
def edit_top() -> None:
    settings = read_settings()
    while 1:
        os.system("cls")
        print(
            f"{padding}\nCurrent number of top scores: {settings['number of top players']}\n{padding}"
        )
        top = input("Enter new number of top scores: ")
        check, err = validate_input(top, "int")
        if check:
            settings["number of top "] = int(top)
            write_settings(settings)
            print(s.pr_green("Successfully updated number of top scores."))
            input("Press Enter to continue...")
            break
        else:
            print(err)
            input("Press Enter to continue...")
#######
def view_leaderboard():
    def print_top() -> None:
        logs = read_logs()
        if len(logs) == 0:
            print("No logs found.")
            input("Press Enter to continue...")
        else:
            logs.sort(key=lambda x: x["score"], reverse=True)
            print(f"{padding}\n{padding}\n")
            for i in range(len(logs)):
                print(f"\t\t{s.pr_bold(i+1)}: {logs[i]['player']} - {logs[i]['points']}")
            print(f"\n{padding * 2}\n")
            input("Press Enter to continue...")
    def read_logs() -> dict:
        try:
            with open("game_logs.txt", "r") as f:
                obj = ast.literal_eval(f.read())
                return obj
        except FileNotFoundError:
            print("Error. Leaderboard not found. ")
    def settings_menu():
        while 1:
            banner(4)
            choice = input(">> ")
            check, err = validate_input(choice, [1, 2, 3])
            if check:
                break
            else:
                print(err)
                input("Press Enter to continue...")
        choice = int(choice)
        if choice == 1:
            print_top()
            input("Press Enter to continue...")
        elif choice == 2:
            print("")
        elif choice == 3:
            return
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
    settings_menu()
def validate_input(userin, options):
    if options == "int":
        if not userin.isnumeric():
            return False, s.pr_red("Invalid input. Please try again.")
        else:
            return True, ""
    else:
        if not userin.isnumeric():
            return False, s.pr_red("Invalid input. Please try again.")
        if int(userin) not in options:
            return False, s.pr_red("Invalid input. Please try again.")
        else:
            return True, ""
def menu() -> int:
    while 1:
        os.system("cls")
        print("\n\n\n")
        banner(2)
        print(s.pr_bold((f"{padding * 1} ~ MENU ~ {padding * 1}\n")))
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('1')}: Word Settings")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('2')}: Game Settings")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('3')}: View reports")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('4')}: Exit\n\n{s.pr_bold(padding * 2 + '==========')}\n")
        t.sleep(0.05)
        user_input = input(">> ")
        check, err = validate_input(user_input, [1, 2, 3, 4])
        if check:
            return int(user_input)
        else:
            print(err)
            input("Press Enter to continue...")
def check_login(username: str, password: str) -> bool:
    try:
        with open("./admin.txt", "r") as f:
            obj = ast.literal_eval(f.read())
    except Exception as e:
        print(e)
        return False
    for i in range(len(obj)):
        if obj[i]["username"] == username:
            if (obj[i]["password"]) == hashlib.sha256(password.encode()).hexdigest():
                return True
    return False
def login(attempts: int):
    print(s.pr_bold((f"{padding} ~ LOGIN ~ {padding}")))
    username = input(s.pr_bold("Username: "))
    password = input(s.pr_bold("Password: "))
    if check_login(username, password):
        print("Successfully logged in.")
        return True, attempts
    else:
        if attempts:
            print(f"Invalid credentials. You have {attempts} attempts left.")
        attempts -= 1
        return False, attempts
def game_menu():
    while 1:
        banner(3)
        choice = input(">> ")
        check, err = validate_input(choice, [1, 2, 3, 4])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            if choice == 1:
                edit_session()
            elif choice == 2:
                edit_guesses()
            elif choice == 3:
                edit_top()
            elif choice == 4:
                return
            else:
                print("Invalid input. Please try again.")
                input("Press Enter to continue...")
def word_menu():
    while 1:
        banner(1)
        choice = input(">> ")
        check, err = validate_input(choice, [1, 2, 3, 4, 5, 6])
        if not check:
            print(err)
            input("Press Enter to continue...")
        else:
            choice = int(choice)
            if choice == 1:
                add_word()
            elif choice == 2:
                remove_word()
            elif choice == 3:
                edit_word()
            elif choice == 4:
                view_words()
            elif choice == 5:
                reset_words()
            elif choice == 6:
                return
            else:
                print("Invalid input. Please try again.")
                input("Press Enter to continue...")
def main() -> None:
    attempts = 3
    while attempts >= 0:
        check, attempts = login(attempts)
        if check:
            break
    if attempts < 0:
        print("Too many failed attempts. Exiting...")
        exit()
    while 1:
        choice = menu()
        if choice == 1:
            word_menu()
        elif choice == 2:
            game_menu()
        elif choice == 3:
            view_leaderboard()
        elif choice == 4:
            print("Exiting...")
            exit()
        else:
            print(s.pr_red(("Invalid input. Please try again.")))
            input("Press Enter to continue...")
if __name__ == "__main__":
    try:
        padding = "=" * 25
        main()
    except KeyboardInterrupt:
        print(s.pr_red(("\nExiting...")))
        exit()