class Word:
    def __init__(self, word, difficulty):
        self.word = word
        self.difficulty = difficulty
    def show(self):
        print(f'The current word is {self.word} and the difficulty is {self.difficulty}')
def banner(player: str, session: int, incorrect: int, incorrect_list: list) -> str:
    print(
        f'\n\n\nH A N G M A N\nPlayer: {player}\n{session} of 3\nIncorrect letters: {incorrect_list} ({incorrect})\n')
        
wordlist = [
    {'word': 'kangaroo', 'difficulty': 'hard'}
]

def game(player: str, session: int) -> int:
    counter = 0
    word = wordlist[0]['word']
    guess_list = []
    incorrect_list = []
    guess_progress = "_ " * len(word)
    banner(player, session, counter, incorrect_list)
    while '_' in guess_progress and counter < 5:
        print(guess_progress)
        guess = input("Guess: ")
        guess_progress, guess_list, check, incorrect_list = guessCheck(word=word, guess=guess, previous_guesses=guess_list, previous_result=guess_progress, incorrect=incorrect_list)
        if (not check):
            counter += 1
        banner(player, session, counter, incorrect_list)
    return (len(guess_progress.replace(" ", "").replace('_', '')))


def guessCheck(word: str, guess: str, previous_guesses: str, previous_result: str, incorrect: list) -> str:
    str = ''
    check = False
    for letter in word:
        if (letter == guess):
            previous_guesses.append(guess)
    for letter in word:
        if letter in previous_guesses:
            str += letter+" "
            if letter not in previous_result:
                check = True
        else:
            str += "_ "
    if (not check):
        incorrect.append(guess)
    return (str, previous_guesses, check, incorrect)


class Player:
    def __init__(self, name, points):
        self.name = name
        self.points = points


def main():
    player_list = []
    player = Player(input("Please enter your name: "), 0)
    for i in range(3):
        player.points += game(player=player.name, session=i+1) * 2
    player_list.append(vars(player))
    print(player_list)

main()
