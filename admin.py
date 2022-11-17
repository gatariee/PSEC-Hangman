import ast
import json
import os
import hashlib
import time as t
from styles import Styles as s
def banner(num):
    if(num == 1):
            os.system('cls')
            print(s.prBold((f"{padding} ~ MENU ~ {padding}\n")))
            print(f"\t\tYou have selected: {s.prBold('Word Settings')}\n\n{s.prBold(padding * 2 + '==========')}\n")
            print(f"\t\t\t{s.prBold('1')}: Add word")
            t.sleep(0.05)
            print(f"\t\t\t{s.prBold('2')}: Remove word")
            t.sleep(0.05)
            print(f"\t\t\t{s.prBold('3')}: Edit word")
            t.sleep(0.05)
            print(f"\t\t\t{s.prBold('4')}: View wordlist")
            t.sleep(0.05)
            print(f"\t\t\t{s.prBold('5')}: {s.prRed('*** Reset Words ***')}")
            t.sleep(0.05)
            print(f"\t\t\t{s.prBold('6')}: Back")
    if(num == 2):

        print(s.prGreen((r""" █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗    ██████╗  █████╗ ███╗   ██╗███████╗██╗     
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║    ██████╔╝███████║██╔██╗ ██║█████╗  ██║     
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║    ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║    ██║     ██║  ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                                      """)))
def wordSettings():
    def addWord() -> None:
        def autoDiff(word):
            if(len(word) <= 4):
                return "easy"
            elif(len(word) <= 7):
                return "medium"
            else:
                return "hard"
        word = input('Enter Word ("0" to exit): ').lower()
        if(word == '0'):
            return
        newWord = {
            'word': word,
            'type': input('Enter Type: ').lower(),
            'difficulty': autoDiff(word)
        }
        try:
            with open('word_list.txt', 'r+') as f:
                if(os.stat("word_list.txt").st_size == 0):
                    obj = []
                    obj.append(newWord)
                else:
                    obj = (ast.literal_eval(f.read()))
                    for i in range(len(obj)):
                        if(obj[i]['word'] == word):
                            print(padding)
                            print('Word already exists!')
                            return
                    obj.append(newWord)
                new = json.dumps(obj, indent=4)
                f.seek(0)
                f.truncate(0)
                f.write(str(new))
                f.close()
                print(f"Successfully added {newWord['word']} to the word list.")
        except:
            print("Error. Wordlist not found. ")
    def removeWord() -> None:
        try:
            with open('word_list.txt', 'r+') as f:
                obj = (ast.literal_eval(f.read()))
                while(1):
                    os.system('cls')
                    print(padding * 2 + '\n')
                    for i in range(len(obj)):
                        print(f"\t\t{s.prBold(i+1)}: {obj[i]['word']}")
                    word = input(f"\n{padding*2}\nEnter the word you want to remove ('0' to exit):  ")
                    for i in range(len(obj)):
                        if(obj[i]['word'].lower() == word.lower()):
                            obj.pop(i)
                            new = json.dumps(obj, indent=4)
                            f.seek(0)
                            f.truncate(0)
                            f.write(str(new))
                            f.close()
                            print(f"Successfully removed {word}.")
                            input("Press Enter to continue...")
                            return
                    if(word == '0'):
                        return
                    else:
                        print("Word not found. Please try again.")
                        input("Press Enter to continue...")
        except:
            print("Error. Wordlist is empty or not found. ")
            return
    def editWord() -> None:
        try:
            with open('word_list.txt', 'r+') as f:
                obj = (ast.literal_eval(f.read()))
                while(1):
                    os.system('cls')
                    print(padding * 2 + '\n')
                    for i in range(len(obj)):
                        print(f"\t\t{s.prBold(i+1)}: {obj[i]['word']}")
                    word = input(f"\n{padding*2}\nEnter the word you want to edit ('0' to exit):  ")
                    check = False
                    index = None
                    if(word.isnumeric()):
                        def checkEdge(word):
                            word = int(word)
                            return(True, word-1) if(word > 0 and word <= len(obj)) else (False, 0)
                        check, index = checkEdge(word)
                    for i in range(len(obj)):
                        if((obj[i]['word'] == word.lower()) or check):
                            while(1):
                                if(index != None):
                                    i = index
                                print(padding*2)
                                print("\n\tCurrent word: ", obj[i]['word'])
                                print("\tCurrent type: ", obj[i]['type'])
                                print("\tCurrent difficulty: ", obj[i]['difficulty'] + '\n')
                                print(padding*2)
                                print(f"\n{s.prBold('1')}: Edit word")
                                print(f"{s.prBold('2')}: Edit type")
                                print(f"{s.prBold('3')}: Edit difficulty")
                                print(f"{s.prBold('4')}: Save and exit")
                                choice = input(">> ")
                                print(padding)
                                if(choice == '1'):
                                    obj[i]['word'] = input("Enter new word: ")
                                elif(choice == '2'):
                                    obj[i]['type'] = input("Enter new type: ")
                                elif(choice == '3'):
                                    obj[i]['difficulty'] = input("Enter new difficulty: ")
                                elif(choice == '4'):
                                    break
                                else:
                                    print("Invalid input. Please try again.")
                                    input("Press Enter to continue...")
                            print(f"These are the new values\n\tWord: {obj[i]['word']}\n\tType: {obj[i]['type']}\n\tDifficulty: {obj[i]['difficulty']}")
                            new = json.dumps(obj, indent=4)
                            f.seek(0)
                            f.truncate(0)
                            f.write(str(new))
                            f.close()
                            return
                    if(word == '0'):
                        return
                    else:
                        print("Word not found. Please try again.")
                        input("Press Enter to continue...")
        except:
            print("Error. Wordlist is empty or not found. ")
            return
    def viewWords() -> None:
        try:
            with open('word_list.txt', 'r') as f:
                obj = (ast.literal_eval(f.read()))
                print(f"There are currently {len(obj)} words in the word list.\n")
                print(padding * 2 + '\n')
                for i in range(len(obj)):
                    print(f"\t\t{s.prBold(i+1)}: {obj[i]['word']}")
                print(f"\n{padding * 2}\n")
        except:
            print("Error. Wordlist is empty or not found. ")
            return
        input("Press Enter to continue...")
    def resetWords() -> None:
        try:
            with open('word_list.txt', 'w') as f:
                f.truncate(0)
                f.close()
                print("Successfully reset word list.")
                return
        except:
            print("Error. Wordlist not found. ")
            return
    def settingsMenu() -> int:
        while(1):
            banner(1)
            choice = input(">> ")
            check, err = validateInput(choice, 1)
            if(check):
                break
            else:
                print(err)
                input("Press Enter to continue...")
        choice = int(choice)
        # validateInput checks if the input is a number, so this shouldn't break anything.. !!
        if(choice == 1):
            addWord()
        elif(choice == 2):
            removeWord()
        elif(choice == 3):
            editWord()
        elif(choice == 4):
            viewWords()
        elif(choice == 5):
            print("Are you sure you want to reset the word list? (y/n)")
            yn = input(">> ")
            if(yn.lower() == 'y'):
                resetWords()
            elif(yn.lower() == 'n'):
                pass
        elif(choice == 6):
            return
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
        settingsMenu()
    settingsMenu()
def validateInput(input, choice) -> bool:
    if(not input.isnumeric()):
        return False, s.prRed("Invalid input. Please try again.")
    if(choice == 1):
        options = [1,2,3,4,5,6]
        if int(input) not in options:
            return False, s.prRed("Invalid input. Please try again.")
        else:
            return True, ""
def menu() -> int:
    while(1):
        os.system('cls')
        print('\n\n\n')
        banner(2)
        print(s.prBold((f"{padding * 1} ~ MENU ~ {padding * 1}\n")))
        t.sleep(0.05)
        print(f"\t\t{s.prBold('1')}: Word Settings")
        t.sleep(0.05)
        print(f"\t\t{s.prBold('2')}: Game Settings")
        t.sleep(0.05)
        print(f"\t\t{s.prBold('3')}: View reports")
        t.sleep(0.05)
        print(f"\t\t{s.prBold('4')}: Exit\n\n{s.prBold(padding * 2 + '==========')}\n")
        t.sleep(0.05)
        userInput = input(">> ")
        check, err = validateInput(userInput, 1)
        if(check):
            return int(userInput)
        else:
            print(err)
            input("Press Enter to continue...")
def checkLogin(username: str, password: str) -> bool:
    try:
        with open('admin.txt', 'r') as f:
            obj = (ast.literal_eval(f.read()))
    except:
        print("Error. admin.txt not found. ")
        return False
    for i in range(len(obj)):
        if(obj[i]['username'] == username):
            if(obj[i]['password']) == hashlib.sha256(password.encode()).hexdigest():
                return True
    return False
def login(attempts: int) -> bool:
    print(s.prBold((f"{padding} ~ LOGIN ~ {padding}")))
    username = input(s.prBold("Username: "))
    password = input(s.prBold("Password: "))
    if(checkLogin(username, password)):
        print("Successfully logged in.")
        return True, attempts
    else:
        if(attempts):
            print(f"Invalid credentials. You have {attempts} attempts left.")
        attempts -= 1
        return False, attempts
def main() -> None:
    attempts = 3
    while(attempts >= 0):
        check, attempts = login(attempts)
        if(check):
            break
    if(attempts < 0):
        print("Too many failed attempts. Exiting...")
        exit()
    while(1):
        choice = menu()
        if(choice == 1):
            wordSettings()
        elif(choice == 2):
            print("WIP")
            input("Press Enter to continue...")
        elif(choice == 3):
            print("WIP")
            input("Press Enter to continue...")
        elif(choice == 4):
            print("Exiting...")
            exit()
        else:
            print(s.prRed(("Invalid input. Please try again.")))
            input("Press Enter to continue...")
if __name__ == "__main__":
    try:
        padding = "=" * 25
        main()
    except KeyboardInterrupt:
        print(s.prRed(("\nExiting...")))
        exit()