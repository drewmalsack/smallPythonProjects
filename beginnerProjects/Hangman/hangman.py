import random


word_list = ["Supposedly", "there", "are", "over", "one", "million", "words", "in", "the", "English", "Language",
                 "We", "trimmed", "some", "fat", "to", "take", "away", "really", "odd", "words", "and", "determiners",
                 "Then", "we", "grabbed", "the", "most", "popular", "words", "and", "built", "this", "word",
                 "Just", "keep", "clicking", "generate", "chances", "are", "you", "wont", "find", "repeat"]
lives = 5
letters = []
letters_left = 0


def hang_man():
    global letters_left
    word = find_word()
    letters_left = len(word)
    for i in range(len(word)):
        letters.append("___  ")
    draw()
    while lives > 0 and letters_left > 0:
        guess(word)
        draw()
    if lives == 0:
        print("You lose")
    else:
        print("You Win, the word was "+word.upper())


def find_word():
    x = random.randint(0, 43)
    word = word_list[x]
    return word


def draw():
    for i in range(len(letters)):
        if i == len(letters)-1:
            print(letters[i])
        else:
            print(letters[i], end='')
    print(str(lives) + " lives left.")


def guess(word):
    guess_letter = input("Enter your guess: ")
    check_word(word, guess_letter)


def check_word(word, guess_letter):
    global lives, letters_left
    characters = list(word)
    correct = 0
    for i in range(len(characters)):
        if characters[i].lower == guess_letter.lower:
            letters[i] = guess_letter+" "
            letters_left -= 1
            correct = 1
    if correct == 0:
        print("No "+guess_letter+"'s")
        lives -= 1
    else:
        print("Correct")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hang_man()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
