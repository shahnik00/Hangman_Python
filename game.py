import pygame
import random
import os
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)
#main_dir = os.path.split(os.path.abspath(__file__))[0]
#data_dir = os.path.join(main_dir, "data")

def main():
    # pygame setup    
    running = True

    # Game background
    background_image = pygame.image.load("./Hangman.jpg")
    Lose_Screen  = pygame.image.load("./Lose Screen.jpg")
    Win = pygame.image.load("./Win.jpg")

    background_image = pygame.transform.scale(background_image,(1280, 720))
    Lose_Screen = pygame.transform.scale(Lose_Screen,(1280, 720))
    Win = pygame.transform.scale(Win,(1280, 720))

    screen.blit(background_image,(0,0))

    # Hangman global trackers 
    chosenWord = sportWords()
    uniqueChar = unqiueCharacters(chosenWord)
    wrongGuessCount = 0
    correctLetters = 0
    usedLetters = []
    writeToScreen("Incorrect guess", 800 , 50, size = 100)
    writeToScreen("Welcome to hangman!", 800 , 300, size = 30)
    writeToScreen("Guess the hidden sports related word to win", 800 , 330, size = 30)
    writeToScreen("Making 6 incorrect guess means you lose", 800 , 360, size = 30)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and wrongGuessCount != 6 and correctLetters != uniqueChar:
                if event.key in range(97,123):
                    guessLetter = chr(event.key)
                    if guessLetter not in usedLetters:
                        usedLetters.append(guessLetter)
                        if check(guessLetter, chosenWord):
                            # Draws the letter in the place where it is in the word
                            correctLetters += 1
                            locations = findLocation(chosenWord, guessLetter)
                            for i in locations:
                                writeToScreen(guessLetter, 75 * i + 400, 590, size = 100)
                        else:
                            # Draws apart of the body for each incorrect guess
                            wrongGuessCount += 1  
                            writeToScreen(guessLetter, 75 * (len(usedLetters) - correctLetters) + 540, 130, size = 100)
                            printBody(wrongGuessCount)

        

        # Puts up the lose or win background
        drawWordLine(chosenWord)
        if wrongGuessCount == 6:
            #draw losing screen
            screen.blit(Lose_Screen,(0,0))

        if correctLetters == uniqueChar:
            #draw win screen
            screen.blit(Win,(0,0))
            
    #################################################################
        # RENDER YOUR GAME HERE
            
    ##############################################################
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


class PlayerMouse(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image, self.rect = load_image(image,scale=.1)#adjust scale to get character sizing right
        self.rect.topleft = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)#adjust arugments for disired starting position
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos

class PlayerWasd(pygame.sprite.Sprite):
    
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        
        self.speed = 15
        self.image, self.rect = load_image(image,scale=.5)#adjust scale to get character sizing right
        self.rect.topleft = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)#adjust arugments for disired starting position
    def update(self):
        keys = pygame.key.get_pressed()
        (x,y) = self.rect.topleft
        if keys[pygame.K_w]:
            y -= self.speed
        if keys[pygame.K_s]:
            y += self.speed
        if keys[pygame.K_a]:
            x -= self.speed
        if keys[pygame.K_d]:
            x += self.speed
        self.rect.topleft = (x,y)


def writeToScreen(msg, x, y, size = 1000):
    font = pygame.font.Font(None, size)
    text = font.render(msg, True, (10, 10, 10))
    textpos = text.get_rect(centerx=x, y=y)
    screen.blit(text, textpos)

def load_image(name,x, y, colorkey=None, scale=1):
    #fullname = os.path.join(data_dir, name)
    image = pygame.image.load(name)
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        rect = image.get_rect()
        rect.topleft = (x, y)
    return image, rect

#################################################################
##                   HANGMAN CODE                              ##
#################################################################

#Gets a random sports related word
def sportWords():
    sport = ["soccer", "basketball","football", "tennis", "baseball",
             "lacrosse", "golf", "volleyball","badminton","hockey"]
    choosenWord = random.choice(sport)
    return choosenWord
    
# Gets the number of unique characters in the choosen word
def unqiueCharacters(chosenWord):
    uniqueChar = []
    for i in chosenWord:
        if i not in uniqueChar:
            uniqueChar.append(i)
    return len(uniqueChar)
#test
# Returns the indexs of where the user guessed correctly at 
def findLocation(chosenWord, userGuess):
    locations = []
    for i, character in enumerate(chosenWord):
        if character == userGuess:
            locations.append(i)
    return locations

# Checks if the users guess character is in the choosen word
def check(userGuess, chosenWord):
    if userGuess.lower() in chosenWord:
        return True
    else:
        return False

# Draws a number of lines representing number of characters in choosen word
def drawWordLine(chosenWord):
    for i in range(0, len(chosenWord)):
        writeToScreen("_", 75 * i + 400, 600, size = 100)
        
# Draws a hangman body part based on number of incorrect guesses
def printBody(wrongGuesses):
    if(wrongGuesses == 1):
        writeToScreen("O", 400,200,150)
    elif(wrongGuesses == 2):
        writeToScreen("|", 400,275,175)
    elif(wrongGuesses == 3):
        writeToScreen("/", 380,300,175)
    elif(wrongGuesses == 4):
        writeToScreen("\\", 420,300,175)
    elif(wrongGuesses == 5):
        writeToScreen("/", 380,375,175)
    elif(wrongGuesses == 6):
        writeToScreen("\\", 420,375,175)

main()