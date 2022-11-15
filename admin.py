import ast
import json
import os
from hangman import *
def addWord():
    newWord = {
        'word': input('word: '),
        'type': input('type: '),
        'difficulty': input('difficulty: ')
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
            return
    except:
        print("Error. Wordlist not found. ")
        return
while(1):
    addWord()