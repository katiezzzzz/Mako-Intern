from random_word import RandomWords

life = 7
counter = 10
r = RandomWords()

r = 'pixel'
counter = len(r)
RealList = [i for i in r]
GuessList = [0] * counter
GuessTrack = []

while counter > 0:
    guess = str(input('Guess a Letter:'))
    RealList = [i for i in r]
    counter2 = 0
    if guess in RealList and guess not in GuessTrack:
        GuessTrack.append(guess)
        while guess in RealList:
            position = RealList.index(guess) + counter2
            GuessList[position] = RealList[RealList.index(guess)]
            RealList.remove(guess)
            print('You guessed correctly! ' + str(counter) + ' letters remaining')
            print(GuessList)
            counter = counter - 1
            counter2 += 1
    else:
        print('Wrong Guess :( ' + str(life) + ' lives remaining')
        life -= 1
        if life == 0:
            print('Out of lives')
            break
if counter == 0:
    print('Congratulations! You have found the word')

