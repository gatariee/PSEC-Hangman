import ast
from inspect import istraceback
import random
session = 0
previous_words = []
def readWords():
    """
    Returns:
        wordlist(list): [
            {
                'word': value,
                'difficulty': value,
                'type': value,
            },
            {
                ...
            }
        ]
    """
    try:
        with open('wordlist.txt') as f:
            global wordlist
            wordlist = (ast.literal_eval(f.read()))
    except:
        print("Error. Wordlist not found. ")


def guessCheck(word, guess, guess_progress):
    """
    Args:
        word (str): The word that is being guessed
        guess (str): The letter that the user has guessed
        guess_progress (str): The current progress of the game

    Returns:
        check (bool): returns True if guess is correct, False if guess is wrong
        ans (str): returns the result after checking the guess

    Note:
        guess_progress == BEFORE checking
        ans ==  AFTER checking
        logically, guess_progress is the previous iteration of ans
    """
    global previous_guesses
    global incorrect_list
    ans = ""
    check = False
    for letter in word:
        if letter == guess:
            previous_guesses.append(guess)
    for letter in word:
        if letter in previous_guesses:
            ans += letter + " "
            if letter not in guess_progress:
                check = True
        else:
            ans += "_ "
    if not check:
        incorrect_list.append(guess)
    return check, ans

def game():    
    word = pickWord()
    global incorrect_list
    global previous_guesses
    previous_guesses = [] # Globally accessible
    incorrect_list = [] # Globally accessible
    guess_progress = "_ " * len(word) # Initial
    while 1:
        print(f'Current progress: {guess_progress}')
        userGuess = input("Guess: ")
        correct, guess_progress = guessCheck(word=word, guess=userGuess, guess_progress=guess_progress)
        print(guess_progress)
        print(incorrect_list)
        print(previous_guesses)

def pickWord():
    readWords()
    global previous_words
    randIndex = random.randint(0, len(wordlist)-1)
    if(randIndex in previous_words):
        pickWord()
    else:
        word = wordlist[randIndex]['word']
        previous_words.append(randIndex)
    return word

def banner(name):
    global session
    session += 1
    print(f'\nH A N G M A N\nPlayer: {name}\n{session} out of 3')

def begin():
    playerName = input("Please enter your name: ")
    banner(playerName)
    game()

begin()