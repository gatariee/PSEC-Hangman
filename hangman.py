import ast
import random
class Game:
    def __init__(self, player):
        self.player = player
        self.session = session 
        self.word, self.type, self.difficulty = Game.pickWord()
        self.guesses = 0
        self.previous_guesses = []
        self.incorrect_list = []
        self.guess_progress = "_ " * len(self.word)
    def guessLetter(self, letter):
        def verifyGuess(guess):
            if(not guess.isalpha()):
                print("Please enter a letter.")
            elif(len(guess) != 1):
                print("Please enter a single letter.")
            elif(guess in self.previous_guesses):
                print("You already guessed that letter.")
            else:
                return True
        if(not verifyGuess(letter)):
            return
        else:
            letter = letter.lower()
        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.guess_progress = self.guess_progress[:i*2] + letter + self.guess_progress[i*2+1:]
        else:
            self.guesses += 1
            self.incorrect_list.append(letter)
        self.previous_guesses.append(letter)
    def pickWord():
        def readWords():
            global previous_words
            try:
                with open('wordlist.txt') as f:
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
        if(all(char in allowed_chars for char in playerName)):
            begin(playerName)
            return
        print("Please enter a valid name. ")
def begin(playerName): # Start of game loop
    global session
    HangMan = Game(playerName)
    if(session == 1):
        print("\nWelcome to Hangman, " + HangMan.player + "!")
        print("Your word is " + str(len(HangMan.word)) + " letters long. ")
        print("You have 5 guesses to guess the word. Good Luck!")
        print("Session: " + str(session))
    else:
        print("\nYour word is " + str(len(HangMan.word)) + " letters long. ")
        print("Session: " + str(HangMan.session))
    while(HangMan.guesses < 5) and ((HangMan.guess_progress).replace(" ","") != HangMan.word):
        print("\nWord: " + HangMan.guess_progress)
        print(f"Incorrect Guesses: {', '.join(HangMan.incorrect_list)}")
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
        begin(playerName)
    

if(__name__ == "__main__"):
    main()