#modules
import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
import pymysql
from pygame.locals import * # Basic pygame imports
from pygame_menu.examples import create_example_window
import pygame_menu

surface = create_example_window('game menu', (1430, 700))

# Load welcome image
background_image = pygame_menu.BaseImage(
    image_path='C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\message2.jpg')

# Main menu theme
main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
main_menu_theme.background_color=(252,252,252)
main_menu_theme.set_background_color_opacity(0.5)
main_menu_theme.title_background_color=(0,124,0)

#main menu
menu = pygame_menu.Menu(
    height=430,
    theme=main_menu_theme,
    title='Menu',
    width=350
    )

#set welcome image
theme_bg_image = main_menu_theme.copy()
theme_bg_image.background_color = pygame_menu.BaseImage(
        image_path='C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\message2.jpg')

# FAQs theme
faq_theme = pygame_menu.themes.THEME_ORANGE.copy()
faq_theme.title_background_color=(0,124,0)
faq_theme.widget_margin = (0, 0)
faq_theme.background_color=(252,252,252)
faq_theme.set_background_color_opacity(0.8)

#FAQs menu
faq_menu =pygame_menu.Menu(
    height=700,
    theme=faq_theme,
    title='FAQs',
    width=1430
    )

#login theme
login_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
login_menu_theme.title_background_color=(0,124,0)
login_menu_theme.widget_font_size = 30
login_menu_theme.widget_padding = (10,10)
login_menu_theme.background_color=(252,252,252)
login_menu_theme.set_background_color_opacity(0.7)

#login menu 
login_menu = pygame_menu.Menu(
    height=400,
    theme=login_menu_theme,
    title='Details',
    width=350
    )


# faq questions
faqs = [f'1. How user can play Flying Fish game?', 
         f'Ans: After clicking play button press the spacebar to allow your fish to fly and to start the game. stay in the middle of screen until the first set of pipes appers. Measure your tap heights to go between the two pipes',
         f'2. When game is over?',
         f'Ans: When fish is hit the pipes, ceiling or ground line then fish is die and game is over.',
         f'3. Where player can see their score?',
         f'Ans: player can see their score at top of center of game screen during playing game.',
         f'4. How many player can play this game at a time?',
         f'Ans: Flying Fish is one player game. At a time only one player can play the game.',
         f'5. What to do if game is over?',
         f'Ans: If you want to play again then click on  play button and play game otherwise click on quit button.',
         f'6. Can you pause in Flying Fish game?',
         f'Ans: you can not pause this game.', 
         f'7. When game will become hard?',
         f'Ans: After collecting 30 scores game will hard then after collecting 50 score game will more hard.',
         f'8. What is the highest score in Flying Fish game?',
         f'Ans: Flying Fish game is endless. Unlike complex,multilevel-games',
         f'9. Why user should play our game?',
         f'Ans: Flying Fish is an arcade-style game. In this game player passed fish between pipes.so,player concentration is develop.',
         f'10. In future what changes we will do in our game?',
         f'Ans: We update our game by given background choice and different fish choice and also give different pipes with background choice']

for m in faqs:
    faq_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    faq_menu.add.vertical_margin(20)

#create db
mydb=pymysql.connect(
host="localhost",
user="root",
password="",
database="fish"
)
mycursor=mydb.cursor()
#mycursor.execute("create database fish")
#mycursor.execute("create table game(player varchar(50))")

# set the game icon 
icon = pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\main_fish.png')
pygame.display.set_icon(icon)


# Global Variables for the game
FPS = 50
SCREENWIDTH = 1365
SCREENHEIGHT = 720
SCREEN = pygame.display.set_mode((400,400),pygame.RESIZABLE)
GROUNDY = SCREENHEIGHT * 10.0
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\main_fish.png'
BACKGROUND = 'C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\Natural_bg2.jpg'
PIPE = 'C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\pipe.png'

def check_name_test(value: str) -> None:
    """
    This function tests the text input widget.

    :param valuD: The widget value
    """
    print(f'User namD: {value}')
    
# player details
login_menu.add.text_input(
    'Player Name: ',
    default='sky',
    onreturn=check_name_test,
    )

#store data
def data_fun() -> None:
    print('Player data:')
    data = login_menu.get_input_data()
    for k in data:
        print(f'Player Name\t->\t{data[k]}')
        
        record="INSERT INTO  game (player) VALUES (%s)"
        val=[({data[k]})]
        mycursor.executemany(record,val)
        mydb.commit()
        
# store data button        
login_menu.add.button('Store data',
                      data_fun,
                      button_id='store',
                      font_size=25,
                      background_color=(0,124,0),
                      font_color=(252,252,252)
                      )

def main_background() -> None:
    background_image.draw(surface)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/2)
    playery = int(SCREENWIDTH/5)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+50, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+50+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    #List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"score is {score}")

                GAME_SOUNDS['point'].play()
                

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2 # score show in center

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.10))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#Main menu screen
menu.add.button('Login',login_menu)
menu.add.button('Play',mainGame)
menu.add.button('FAQs',faq_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 1
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flying Fish')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\0.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\1.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\2.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\3.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\4.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\5.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\6.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\7.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\8.png').convert_alpha(),
        pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\i01_message2.jpg').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('C:\\Users\\jenvi\\project\\gallery\\gallery\\sprites\\base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:\\Users\\jenvi\\project\\gallery\\gallery\\audio\\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:\\Users\\jenvi\\project\\gallery\\gallery\\audio\\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:\\Users\\jenvi\\project\\gallery\\gallery\\audio\\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:\\Users\\jenvi\\project\\gallery\\gallery\\audio\\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:\\Users\\jenvi\\project\\gallery\\gallery\\audio\\wing.wav')
    

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        
        menu.mainloop(surface,main_background)
        #welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame()

        
