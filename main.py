import pygame
import random

pygame.init()
winHeight = 580
winWidth = 800
win=pygame.display.set_mode((winWidth,winHeight))
black = (0,0, 0)
white = (255,255,255)

btn_font = pygame.font.SysFont("arial", 12)
guess_font = pygame.font.SysFont("monospace", 20)
lost_font = pygame.font.SysFont('arial', 30)
pygame.display.set_caption("Hangman - Python Test Kodland - Pedro")
drawings = [pygame.image.load('0.png'), 
pygame.image.load('1.png'), pygame.image.load('2.png'), 
pygame.image.load('3.png'), pygame.image.load('4.png'), 
pygame.image.load('5.png'), pygame.image.load('6.png')]
limbs = 0
word = ''
buttons = []
guessed = []

def pressedButton(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

def chosenWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]

def gameCreation():
    global guessed
    global drawings
    global limbs
    win.fill(white)
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, black, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, black)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))
    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, black)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1,(winWidth/2 - length/2, 400))
    pic = drawings[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            




def end(winner=False):
    global limbs
    lostTxt = 'You Lost! Press any key to play again...'
    winTxt = 'You Win! Press any key to play again...'
    gameCreation()
    pygame.time.delay(1000)
    win.fill(white)
    if winner == True:
        label = lost_font.render(winTxt, 1, black)
    else:
        label = lost_font.render(lostTxt, 1, black)
    wordTxt = lost_font.render(word.upper(), 1, black)
    wordWas = lost_font.render('Phrase: ', 1, black)
    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    resetGame()


def resetGame():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True
    limbs = 0
    guessed = []
    word = chosenWord()
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([white, x, y, 20, True, 65 + i])
word = chosenWord()
inPlay = True
while inPlay:
    gameCreation()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = pressedButton(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)
pygame.quit()

