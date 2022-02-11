from cs50 import get_string

text = get_string("Text: ")
textLen = len(text)

numLetters = 0
numWords = 1
numSentences = 0

for letter in range(textLen):
    if text[letter].isalpha():
        numLetters+=1
    elif text[letter].isspace():
        numWords+=1
    elif (text[letter] == '?' or text[letter] == '!' or text[letter] == '.'):
        numSentences+=1

colemanIndex = round((0.0588 * numLetters / numWords * 100) - (0.296 * numSentences / numWords * 100) - 15.8)

if colemanIndex < 1:
    print("Before Grade 1")
elif colemanIndex > 16:
    print("Grade 16+")
else:
    print(f"Grade {colemanIndex}")