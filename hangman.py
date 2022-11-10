import ast
import random
from datetime import date
import json
import os
class Game:
    def __init__(self, player):
        """_summary_:
            Initializes the game object
        Args:
            player (_type_): str
                _description_: The name of the player
        """
        self.player = player
        self.session = session 
        self.word, self.type, self.difficulty = Game.pickWord()
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
        self.totalPoints = 0
    def calculatePoints(self):
        """_summary_: 
            Removes all underscores and whitespace from guess_progress and multiplies the length of the result by 2.
            The length of the result is the number of CORRECT guesses
        Returns:
            _type_: int
            _description_: The number of points accumulated from the session
        """
        return len((self.guess_progress).replace("_", " ").replace(" ", "")) * 2
    def endGame(log):
        """_summary_: 
            This function is called at the end of the game before logging and destruction of game object.
            It prints the final score of the player and gives the player an option to print the leaderboard
        Args:
            log (_type_): object
                _description_: 
                The log object contains 3 keys. 'player', 'score', and 'date'
        """
        def generateReport():
            """_summary_: 
                This function is called to permanently save the log object to game_logs.txt for administrative purposes
            """
            with open('game_logs.txt', 'r+') as f:
                if(os.stat("game_logs.txt").st_size == 0):
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
        print(f"------------------------------------------\nGame Over. You have ended the game with {log['points']} points.") 
        print(f"Here is what we are logging: \n------------------------------------------\nName: {log['player']}\nPoints: {log['points']}\nDate: {log['date']}\n------------------------------------------")
        generateReport()
    def guessLetter(self, letter):
        def verifyGuess(guess):
            if(not guess.isalpha()):
                print("------------------------------------------\nPlease enter a letter.\n------------------------------------------")
            elif(len(guess) != 1):
                print("------------------------------------------\nPlease enter a single letter. \n------------------------------------------")
            elif(guess in self.previous_guesses):
                print("------------------------------------------\nYou already guessed that letter. \n------------------------------------------")
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
                    self.guess_progress = self.guess_progress[:i*2] + letter + self.guess_progress[i*2+1:]
                    count+=1
        else:
            self.guesses += 1
            self.incorrect_list.append(letter)
            print("------------------------------------------\nIncorrect! You have " + str(5-self.guesses) + " guesses left. \n------------------------------------------")
        self.previous_guesses.append(letter)
        if(count > 1):
            print("------------------------------------------\nCongratulations. There are " + str(count) + " " + letter + "'s. \n------------------------------------------")
        elif(count == 1):
            print("------------------------------------------\nCongratulations. There is 1 " + letter + ". \n------------------------------------------")
    def pickWord():
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
        word = wordlist[randIndex]['word']
        type = wordlist[randIndex]['type']
        difficulty = wordlist[randIndex]['difficulty']
        previous_words.append(randIndex)
        return word, type, difficulty

def main(): # Start of program
    global previous_words
    global session
    session = 1
    previous_words = []
    while(1):
        alphabets_lower = list(map(chr, range(97, 123)))
        alphabets_upper = list(map(chr, range(65, 91)))
        special_chars = ['-','/']
        allowed_chars = alphabets_upper + alphabets_lower + special_chars
        playerName = input("Enter your name: ")
        if(not all(char in allowed_chars for char in playerName)):
            print("Please enter a valid name. ")
            continue
        else: 
            count = 0
            if(os.stat("game_logs.txt").st_size != 0):
                with open("game_logs.txt", 'r') as f:
                    gameLogs = (ast.literal_eval(f.read()))
                    for value in gameLogs:
                        if(value['player'] == playerName):
                            break
                        else:
                            count+=1
                if(count == len(gameLogs)):
                    begin(playerName)
                    return
            else:
                begin(playerName)
                return
            print("Name is taken. Please try again.")
def begin(playerName): # Start of game loop
    global session
    HangMan = Game(playerName)
    log['player'] = HangMan.player
    if(session == 1):
        print("\nWelcome to Hangman, " + HangMan.player + "!")
        print("Your word is " + str(len(HangMan.word)) + " letters long. ")
        print("You have 5 guesses to guess the word. Good Luck!")
        print("Session: " + str(session) + "\n------------------------------------------")
    else:
        print("\nYour word is " + str(len(HangMan.word)) + " letters long. ")
        print("Session: " + str(HangMan.session) + "\n------------------------------------------")
    while(HangMan.guesses < 5) and ((HangMan.guess_progress).replace(" ","") != HangMan.word):
        HangMan.calculatePoints()
        print("\nWord: " + HangMan.guess_progress)
        print(f"Incorrect Guesses: {', '.join(HangMan.incorrect_list)}")
        print(f"Correct Guesses: {', '.join(list(set(HangMan.previous_guesses) - set(HangMan.incorrect_list)))}")
        print("Guesses remaining: " + str(5 - HangMan.guesses))
        guess = input("Guess: ")
        HangMan.guessLetter(guess)
    
    if(HangMan.guesses == 5):
        print("\nYou lose.")
    else:
        print("\nCongratulations. You win!")
    print(f"The {HangMan.type} is \"{HangMan.word}\", the difficulty was {HangMan.difficulty}.")
    if(session < 3):
        session+=1
        log['points'] += HangMan.calculatePoints()
        print(f"Your total points are {log['points']}.")
        begin(playerName)
    else:
        log['points'] += HangMan.calculatePoints()
        Game.endGame(log=log)


    

if(__name__ == "__main__"):
    log = {'player': '','points': 0, 'date': date.today().strftime("%d/%m/%y")}
    main()