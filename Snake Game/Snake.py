import pygame       #importing pygame module     
pygame.init()       #importing pygame module
import random       #random food on screen

from pygame import mixer

#Colors definition(r,g,b)
green = (0, 250, 0)
white = (255, 255, 255)
red = (250, 0, 0)
black = (0, 0, 0)
yellow = (250, 250, 0)

#Creating Game Window
screen_width = 900      #var for width of game screen
screen_height = 600     #var for height of game screen
gameWindow = pygame.display.set_mode((screen_width,screen_height))     #setting the screen size (len,bre)
pygame.display.set_caption("Snake Game")           #setting the title of the game
pygame.display.update()     #to update the gameWindow for every action
gameWindow.fill(green)      #to set the background color of gameWindow
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()     #initializing clock for fps

#Background Images
bgimg = pygame.image.load("bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
wlimg = pygame.image.load("wl.jpeg")
wlimg = pygame.transform.scale(wlimg, (screen_width, screen_height)).convert_alpha()
goimg = pygame.image.load("gmover.jpeg")
goimg = pygame.transform.scale(goimg, (screen_width, screen_height)).convert_alpha()

#Score on Screen
def text_screen(text, color, x, y):
    screen_text  = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

#Make the snake grow
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

#making the Welcome Screen
def welcome():
    exit_game = False
    
    #game background music
    mixer.music.load("bgMusic.mp3")
    mixer.music.play()
    
    while not exit_game:
        gameWindow.blit(wlimg, (0, 0))  #to set the background image of gameWindow
        text_screen("Welcome to Snakes Game!", black, screen_width/12, screen_height/2.9)
        text_screen("Press SpaceBar To Play", black, screen_width/9, screen_height/2.2)
        text_screen("~Snakes by Aditya Bhatt", black, screen_width/100, screen_height/1.1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #game background music restarts for the new game
                    mixer.music.play(-1)
                    game_loop()

        pygame.display.update()
        clock.tick(30)

#Game Loop
def game_loop():
    #game specific variables
    exit_game = False       #var for quitting the game
    game_over = False       #var for game over
    snake_x = 150            #initial position of snake
    snake_y = 155            #initial position of snake
    snake_size = 20
    velocity_x = 0
    velocity_y = 0
    fps = 30

    food_x = random.randint(35,screen_width-35)
    food_y = random.randint(35, screen_height-35)
    score = 0
    init_velocity = 7
    snake_list = []
    snake_length = 1 

    #Creating a game loop
    while(not exit_game):
        if(game_over):
            gameWindow.blit(goimg, (0, 0))  #to set the background color of gameWindow
            text_screen("Press Enter to Continue...", red, screen_width/4, screen_height/1.5)
            text_screen("Your Score : " + str(score), red, screen_width/3, screen_height/6)
            
            for event in pygame.event.get():        #detects every event(cursor, click, button)
                if(event.type == pygame.QUIT):      #close the game using X
                    exit_game = True
            
                if(event.type == pygame.KEYDOWN):   #detects key pressed or not
                    if(event.key == pygame.K_RETURN):#detects right arrow key specifically
                        welcome()
        else:

            for event in pygame.event.get():        #detects every event(cursor, click, button)
                if(event.type == pygame.QUIT):      #close the game using X
                    exit_game = True
                
                if(event.type == pygame.KEYDOWN):   #detects key pressed or not
                    if(event.key == pygame.K_RIGHT):#detects right arrow key specifically
                        #snake_x = snake_x + 10      #moves snake to right
                        velocity_x = init_velocity
                        velocity_y = 0

                    if(event.key == pygame.K_LEFT): #detects left arrow key specifically
                        #snake_x = snake_x - 10      #moves snake to left
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if(event.key == pygame.K_UP):   #detects up arrow key specifically
                        #snake_y = snake_y - 10      #moves snake to up
                        velocity_x = 0
                        velocity_y = -init_velocity

                    if(event.key == pygame.K_DOWN): #detects down arrow key specifically
                        #snake_y = snake_y + 10      #moves snake to down
                        velocity_x = 0
                        velocity_y = init_velocity

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            #Snake eats the food
            if(abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size):
                score = score + 10      #increase score by 10
                
                #food music
                bite_Sound = mixer.Sound("appleBite.mp3")
                bite_Sound.play()
                
                #remake the new food
                food_x = random.randint(35,screen_width-35)
                food_y = random.randint(35, screen_height-35)
                snake_length = snake_length + 5     #increase the snake length by 5

            gameWindow.blit(bgimg, (0, 0))#to set the background color of gameWindow
            text_screen("Score : "+str(score), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            #to reduce the length of the snake after every step
            if(len(snake_list)>snake_length):
                del snake_list[0]

            #game over if snake goes into itself
            if head in snake_list[:-1]:
                game_over = True
                #game over music
                pygame.mixer.music.load("bonk.mp3")
                pygame.mixer.music.play()
            
            #game over if snake goes beyond margin
            if(snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height):
                game_over = True
                #game over music
                pygame.mixer.music.load("bonk.mp3")
                pygame.mixer.music.play()
                
            plot_snake(gameWindow, green, snake_list, snake_size)
    
        pygame.display.update()     #to update the gameWindow for every action
        clock.tick(fps)             #frames per second

    pygame.quit()
    quit()

welcome()
pygame.quit()
quit()
