import ast
import json
import os
import hashlib
def banner(num):
    if(num == 1):
            print(padding)
            print("You have selected: Word Settings")
            print("\t1: Add a word")
            print("\t2: Remove a word")
            print("\t3: Edit a word")
            print("\t4: View all words")
            print("\t5: *** Reset words ***")
            print("\t6: Back")
def wordSettings():
    def addWord() -> None:
        newWord = {
            'word': input('Enter Word: '),
            'type': input('Enter Type: '),
            'difficulty': input('Enter Difficulty: ')
        }
        try:
            with open('word_list.txt', 'r+') as f:
                if(os.stat("word_list.txt").st_size == 0):
                    obj = []
                    obj.append(newWord)
                else:                                       
                    obj = (ast.literal_eval(f.read()))
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
                    print(padding)
                    for i in range(len(obj)):
                        print(f"{i+1}: {obj[i]['word']}")
                    print(padding)
                    word = input("Enter the word you want to remove ('0' to exit):  ")
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
        except:
            print("Error. Wordlist is empty or not found. ")
            return
    def editWord() -> None:
        try:
            with open('word_list.txt', 'r+') as f:
                obj = (ast.literal_eval(f.read()))
                while(1):
                    print(padding)
                    print(f"List of words: ")
                    for i in range(len(obj)):
                        print(f"{i+1}: {obj[i]['word']}")
                    word = input("Enter the word you want to edit ('0' to exit):  ")
                    for i in range(len(obj)):
                        if(obj[i]['word'] == word):
                            while(1):
                                print(padding)
                                print("\tCurrent word: ", obj[i]['word'])
                                print("\tCurrent type: ", obj[i]['type'])
                                print("\tCurrent difficulty: ", obj[i]['difficulty'])
                                print(padding)
                                print("1: Edit word")
                                print("2: Edit type")
                                print("3: Edit difficulty")
                                print("4: Save and exit")
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
        except:
            print("Error. Wordlist is empty or not found. ")
            return
    def viewWords() -> None:
        try:
            with open('word_list.txt', 'r') as f:
                obj = (ast.literal_eval(f.read()))
                print(f"There are currently {len(obj)} words in the word list.")
                for i in range(len(obj)):
                    print(padding)
                    print("\tWord: ", obj[i]['word'])
                    print("\tType: ", obj[i]['type'])
                    print("\tDifficulty: ", obj[i]['difficulty'])
        except:
            print("Error. Wordlist is empty or not found. ")
            return
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
        return False, "Please enter a valid option."
    if(choice == 1):
        options = [1,2,3,4,5,6]
        if int(input) not in options:
            return False, "Invalid input. Please try again."
        else:
            return True, ""
def menu() -> int:
    while(1):
        userInput = input("""
        --------------- Welcome to the Admin Panel ---------------
                Please choose an option:
                    1: Word Settings
                    2: Game Settings
                    3: View reports
                    4: Exit
        \n>> """)
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
    username = input("Username: ")
    password = input("Password: ")
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
            print("2")
        elif(choice == 3):
            print("3")
        elif(choice == 4):
            print("4")
        elif(choice == 5):
            print("5")
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
if __name__ == "__main__":
    padding = "=" * 50
    main()