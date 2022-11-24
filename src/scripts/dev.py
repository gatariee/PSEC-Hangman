import json
import ast


def read_word():
    with open("./words.txt", "r") as f:
        words = f.readlines()
    return words

def read_meaning():
    with open("./meanings.txt", "r") as f:
        meanings = f.readlines()
    return meanings

def build_word(word, meaning):
    word_type = ""
    if(" " in word):
        word_type = "Idioms-Proverbs"
        if(len(word.split()) > 8):
            difficulty = "Complex"
        else:
            difficulty = "Simple"
    else:
        word_type = "Word"
        if(len(word) > 8):
            difficulty = "Complex"
        else:
            difficulty = "Simple"
    obj = {
        "word": word,
        "meaning": meaning,
        "difficulty": difficulty,
        "type": word_type,
        "enabled": 'on'
    }
    new = json.dumps(obj, indent=4)
    return new

if(__name__ == "__main__"):
    words = read_word()
    meanings = read_meaning()
    obj = []
    for i in range(len(words)):
        word = words[i].strip()
        meaning = meanings[i].strip()
        word_str = build_word(word, meaning)
        new = ast.literal_eval(word_str)
        obj.append(new)

formatted_obj = json.dumps(obj, indent=4)

with open('./test.txt', 'r+') as f:
    f.write(formatted_obj)

