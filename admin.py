import ast
import json
newWord = {
    'word': input('word: '),
    'type': input('type: '),
    'difficulty': input('difficulty: ')
}
with open('wordlist.txt', 'r+') as f:
    try: 
        obj = (ast.literal_eval(f.read()))
        obj.append(newWord)
    except:
        obj = newWord
    new = json.dumps(obj, sort_keys=True, indent=4)
    f.seek(0)
    f.truncate(0)
    f.write(str(new))
    f.close()
print(type(obj))