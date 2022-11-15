import ast
import random
from datetime import date
import json
import os
import sys
class Game:
    def __init__(self, player: str) -> None: 
        self.player = player
        self.session = session 
        self.word, self.type, self.difficulty = Game.pickWord()
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
        self.totalPoints = 0
    def calculatePoints(self) -> int:
        return len((self.guess_progress).replace("_", " ").replace(" ", "")) * 2
    def endGame(log: object) -> None:
        def generateReport() -> None:
            with open('./game_logs.txt', 'r+') as f:
                if(os.stat("./game_logs.txt").st_size == 0):
                    obj = []
                    obj.append(log)
                else:
                    obj = (ast.literal_eval(f.read()))
                    obj.append(log)
                new = json.dumps(obj, indent=4)
                f.seek(0)
                f.truncate(0)
                f.write(str(new))
                f.close()
                return
        print(f"{padding}\nGame Over. You have ended the game with {log['points']} points.") 
        print(f"Here is what we are logging: \n{padding}\nName: {log['player']}\nPoints: {log['points']}\nDate: {log['date']}\n{padding}")
        generateReport()
    def guessLetter(self, letter: str) -> bool: 
        def verifyGuess(guess):
            if(not guess.isalpha()):
                print(f"{padding}\nPlease enter a letter.\n{padding}")
            elif(len(guess) != 1):
                print(f"{padding}\nPlease enter a single letter. \n{padding}")
            elif(guess in self.previous_guesses):
                print(f"{padding}\nYou already guessed that letter. \n{padding}")
            else:
                return True
        if(not verifyGuess(letter)):
            return
        else:
            letter = letter.lower()
        count = 0
        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    before = self.guess_progress[:i*2]
                    after = self.guess_progress[i*2+1:]
                    self.guess_progress = before + letter + after
                    count+=1
        else:
            self.guesses += 1
            self.incorrect_list.append(letter)
            print(f"{padding}\nIncorrect! You have " + str(settings['guesses']-self.guesses) + f" guesses left. \n{padding}")
        self.previous_guesses.append(letter)
        if(count > 1):
            print(f"{padding}\nCongratulations. There are " + str(count) + " " + letter + f"'s. \n{padding}")
        elif(count == 1):
            print(f"{padding}\nCongratulations. There is 1 " + letter + f". \n{padding}")
    def pickWord() -> dict:
        def readWords():
            global previous_words
            try:
                with open('word_list.txt') as f:
                    wordlist = (ast.literal_eval(f.read()))
                    return wordlist  
            except:
                print("Error. Wordlist not found. ")
        wordlist = readWords()
        randIndex = random.randint(0, len(wordlist)-1)
        while(randIndex in previous_words):
            randIndex = random.randint(0, len(wordlist)-1)
        previous_words.append(randIndex)
        word, type, difficulty = wordlist[randIndex]['word'], wordlist[randIndex]['type'], wordlist[randIndex]['difficulty']
        return word, type, difficulty
def menu() -> int:
    # loop until check is true
    while(1):
        userInput = input("""
        ************ Welcome to HangMan **************
                1: Start new game
                2: Print leaderboard
                3: Search player
                4: Exit
        \n>> """)
        check, err = validateInput(userInput, 2)
        if(check):
            return int(userInput)
        else:
            print(err)
            input("Press Enter to continue...")
def banner(game: object, session: int, choice: int) -> None:
    if(choice == 1):
        print("\nWelcome to Hangman, " + game.player + "!")
        print("Your word is " + str(len(game.word)) + " letters long. ")
    elif(choice == 2):
        print("Session: " + str(session) + " / " + str(settings['attempts']) + f"\n{padding}")
    elif(choice == 3):
        print("\nWord: " + game.guess_progress)
        print(f"Incorrect Guesses: {', '.join(game.incorrect_list)}")
        print(f"Correct Guesses: {', '.join(list(set(game.previous_guesses) - set(game.incorrect_list)))}")
        print("Guesses remaining: " + str(settings['guesses'] - game.guesses))
def validateInput(input, choice: int) -> bool:
    if(choice == 1): # Name validation
        alphabets_lower = list(map(chr, range(97, 123)))
        alphabets_upper = list(map(chr, range(65, 91)))
        special_chars = ['-','/']
        allowed_chars = alphabets_upper + alphabets_lower + special_chars
        if(not all(char in allowed_chars for char in input)):
            return False, "Please enter a valid name. "
        else: 
            if(os.stat("./game_logs.txt").st_size != 0):
                with open("./game_logs.txt", 'r') as f:
                    gameLogs = (ast.literal_eval(f.read()))
                    for value in gameLogs:
                        if(value['player'] == input):
                            return False, "This name is already taken. "
            return True, None
    elif(choice == 2): # menu validation
        if(not input.isnumeric()):
            return False, "Please enter a valid option."
        options = [1,2,3,4]
        for option in options:
            if(int(input) == option):
                return True, None
        return False, "Please enter a valid option. "
def printLeaderboard(num) -> None:
    def readLogs():
        try:
            with open('game_logs.txt', 'r') as f:
                logs = (ast.literal_eval(f.read()))
                return logs
        except:
            print("Error. Game logs not found. ")
    logs = readLogs()
    logs.sort(key=lambda x: x['points'], reverse=True) # sort from highest to lowest points
    print(f"{padding}\n LEADERBOARD (Top {num})\n{padding}")
    for i in range(len(logs)): 
        # could also i in range num but this is more flexible because it can print less than num if there are less than num logs
        print(f"{i+1}. {logs[i]['player']} - {logs[i]['points']} points")
        if(i == num-1):
            break
    print(f"{padding}\n") 
def gameSettings() -> object:
    try:
        with open('./game_settings.txt') as f:
            game_settings = (ast.literal_eval(f.read()))
            # For better readability
            game_settings['attempts'] = game_settings['number of attempts']
            game_settings['guesses'] = game_settings['number of guesses']
            game_settings['words'] = game_settings['number of words']
            game_settings['top'] = game_settings['number of top players']
            # Completely unnecessary but good for my sanity
            del game_settings['number of attempts'], game_settings['number of words'], game_settings['number of top players']
            return game_settings
    except:
        print("Error. game_settings.txt not found. ")
def main() -> None: 
    while(1): # loops until check is true
        playerName = input("Enter your name: ")
        check, err = validateInput(playerName, 1)
        if(check):
            begin(playerName)
            break
        else:
            print(err)
def begin(playerName: str) -> None: 
    global session
    HangMan = Game(playerName) 
    if(session == 1):
        banner(HangMan, session, 1)
        banner(HangMan, session, 2)
    else:
        banner(HangMan, session, 2)
    while(HangMan.guesses < settings['guesses']) and ((HangMan.guess_progress).replace(" ","") != HangMan.word):
        # After every guess, either the word is progressively guessed OR the number of guesses is incremented until the number of guesses is equal to the number of guesses allowed
        HangMan.calculatePoints()
        banner(HangMan, session, 3)
        guess = input("Guess: ")
        HangMan.guessLetter(guess)
    if(HangMan.guesses == settings['guesses']): # if reached max number of guesses
        print("\nYou have reached the maximum number of guesses. ")
    else:
        print("\nCongratulations. ")
    print(f"The {HangMan.type} is \"{HangMan.word}\"") # prints regardless of win/loss
    if(session < settings['attempts']): # if there are still attempts left, loop until end
        session+=1
        log['points'] += HangMan.calculatePoints()
        print(f"Your total points are {log['points']}.")
        begin(playerName)
    else:
        if(log['points'] > 15):
            print("Congratulations! You have won the game! ")
        else:
            print("You have lost the game. ")
        log['points'] += HangMan.calculatePoints()
        log['player'] = HangMan.player
        Game.endGame(log)

if(__name__ == "__main__"):
    settings = gameSettings()
    padding = '-' * 40
    session = 1
    previous_words = []
    log = {
        'player': '',
        'points': 0, 
        'date': date.today().strftime("%d/%m/%y")
    }
    while(1):
        choice = menu() 
        if(choice == 1):
            main()
            break
        elif(choice == 2):
            printLeaderboard(int(settings['top']))
        elif(choice == 3):
            print('search player on lb')
        elif(choice == 4):
            sys.exit()
        input("Press Enter to continue...")
