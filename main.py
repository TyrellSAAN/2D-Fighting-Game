import pygame
from pygame import mixer
import spritesheet
from player import Player

mixer.init() #Music mixer
pygame.init()

#Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#creates the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Game')
#helps with time and controlling frame rate
clock = pygame.time.Clock()
FPS = 60

#Text Font
test_font = pygame.font.Font('font/vinque rg.otf', 50)
countdown_font = pygame.font.Font('font/vinque rg.otf', 50)
score_font = pygame.font.Font('font/vinque rg.otf', 30)
winner_font = pygame.font.Font('font/vinque rg.otf', 40)

#Draw Text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#Victory Logo once player wins
victory_img = pygame.image.load('graphics/victory_logo.jpg')

#Images, params is width and height
background = pygame.image.load('graphics/Background/Battleground3/Bright/Battleground3.png').convert_alpha()
text_surface = test_font.render('Test Game', False, 'White')
player_idle_sheet_image = pygame.image.load('graphics/Player/_Idle.png').convert_alpha() #takes into account the transparent background
player_idle_sprite_sheet = spritesheet.SpriteSheet(player_idle_sheet_image)
player_running_sheet_image = pygame.image.load('graphics/Player/_Run.png').convert_alpha()
player_running_sprite_sheet = spritesheet.SpriteSheet(player_running_sheet_image)



#loading spritesheets
knight_sprite_sheet = pygame.image.load('graphics/Player/knight_spritesheet.png').convert_alpha()
samurai_sprite_sheet = pygame.image.load('graphics/Player2/samurai_spritesheet.png').convert_alpha()
#Player variables
KNIGHT_SIZE = [120, 80] #Frame size of the knight
KNIGHT_SCALE = 4 #Scaling the knight
KNIGHT_OFFSET = [45, 35] #Due to where the image is placed on the hitbox rectangle, we need the knight to be set back into place
KNIGHT_FLIP_OFFSET = [55, 35] #Sets Knight back into place if it is flipped
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET, KNIGHT_FLIP_OFFSET]

SAMURAI_SIZE = [200, 200] #Frame size of the knight
SAMURAI_SCALE = 3.5 #Scaling the knight
SAMURAI_OFFSET = [88, 70] #Due to where the image is placed on the hitbox rectangle, we need the knight to be set back into place
SAMURAI_FLIP_OFFSET = [88, 70] #Sets Knight back into place if it is flipped
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET, SAMURAI_FLIP_OFFSET]


#Number of Steps for each animation
KNIGHT_ANIMATION_STEPS = [10, 10, 3, 3, 4, 6, 1, 10] #Steps for Idle, Run, Jump, Fall, Attack1, Attack2, Hit, Death
SAMURAI_ANIMATION_STEPS = [8, 8, 2, 2, 6, 6, 4, 6]

#Music and Sounds
pygame.mixer.music.load("audio/music/Jin_Theme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 2000) #-1 is infinite loops, 0.0 is where it starts, 2000 for the fadein
sword_sound = pygame.mixer.Sound("audio/sound effects/sword_slash.wav")
sword_sound.set_volume(0.75)


#Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

#Game Variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #Scores between the players
round_over = False
ROUND_OVER_COOLDOWN = 3000

"""
player_animation_list = [] #Holds all the frames for the player
player_animation_steps = 10 #The steps/frame for each sprite sheet
#player_animation_steps = [10, 10] #Frames for each sprite sheet, ie idle 10 frames and running 10 frames
player_action = 0
last_update = pygame.time.get_ticks() #the time
animation_cooldown = 100 #in milliseconds
frame = 0
"""


def draw_health_bar(health, x, y):
    ratio = health / 100 #So health starts off at 100 and goes down as will the health bar
    pygame.draw.rect(screen, WHITE, (x-3, y-3, 206, 36))
    pygame.draw.rect(screen, BLACK, (x, y, 200, 30))
    pygame.draw.rect(screen, ORANGE, (x, y, 200 * ratio, 30))
"""
#puts the frames in the animation list
for x in range(player_animation_steps):
    player_animation_list.append(player_running_sprite_sheet.get_image(x, 120, 80, 2, BLACK))
"""
""" 
step_counter = 0
#puts the frames in the animation list if the sprite sheet has every animation in a single sprite sheet ie idle, run
for animation in player_animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(player_idle_sprite_sheet.get_image(step_counter, 120, 80, 2, BLACK))
        step_counter += 1
    player_animation_list.append(temp_img_list)


#Puts sets of animations in an animation list
def animations_in_list(animation_list, sprite_sheet, animation_steps, width, height):
    temp_img_list = []
    for x in range(animation_steps):
        temp_img_list.append(sprite_sheet.get_image(x, width, height, 4, BLACK))
    animation_list.append(temp_img_list)


animations_in_list(player_animation_list, player_idle_sprite_sheet, player_animation_steps, 120, 80)
animations_in_list(player_animation_list, player_running_sprite_sheet, player_animation_steps, 120, 80)
#print(player_animation_list)
"""

#Creating Instance of Player
player1 = Player(1, 200, 310, False, KNIGHT_DATA, knight_sprite_sheet, KNIGHT_ANIMATION_STEPS, sword_sound)
player2 = Player(2, 530, 310, True, SAMURAI_DATA, samurai_sprite_sheet, SAMURAI_ANIMATION_STEPS, sword_sound)



#Transform the background to fill the screen
DEFAULT_BACKGROUND_SIZE = (800, 600)
background = pygame.transform.scale(background, DEFAULT_BACKGROUND_SIZE)

run = True
#Game Loop
while run:
    #refreshes the screen, just a black background color
    #screen.fill((0,0,0))

    # Draws background puts one surface to another surface
    screen.blit(background, (0, 0))
    #screen.blit(text_surface, (220, 50))



    #Update Player Animation
    player1.update()
    player2.update()

    #Draw Players
    player1.draw(screen)
    player2.draw(screen)

    #Draw Player Stats
    draw_health_bar(player1.health, 20, 20)
    draw_health_bar(player2.health, 580, 20)
    draw_text("P1 Wins: " + str(score[0]), score_font, YELLOW, 20, 550)
    draw_text("P2 Wins: " + str(score[1]), score_font, YELLOW, 625, 550)

    if intro_count <= 0:
        # Move Player
        player1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player2, round_over)
        player2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player1, round_over)
    else:
        #Display the countdown timer
        draw_text(str(intro_count), countdown_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

        #updates the start counter every one second
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    #End Game if a player wins
    if round_over == False:
        if player1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif player2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #VICTORY SIGN
        if player1.alive == False:
            draw_text("Player 2 Wins", winner_font, YELLOW, 275, 200)
        if player2.alive == False:
            draw_text("Player 1 Wins", winner_font, YELLOW, 275, 200)
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN: #If 3 seconds have passed
            round_over = False
            intro_count = 3
            player1 = Player(1, 200, 310, False, KNIGHT_DATA, knight_sprite_sheet, KNIGHT_ANIMATION_STEPS, sword_sound)
            player2 = Player(2, 530, 310, True, SAMURAI_DATA, samurai_sprite_sheet, SAMURAI_ANIMATION_STEPS, sword_sound)

    """ OLD CODE
        # update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:  # if animation_cooldown time have passed between the last update and the current time then update the frame
        frame += 1
        last_update = current_time  # resets the cooldown
        if frame >= len(player_animation_list[player_action]):
            frame = 0  # resets frame back to 0

    # Show frame image
    # screen.blit(frame_0, (0, 0))
    # screen.blit(player_sheet_image,(0, 0))
    screen.blit(player_animation_list[player_action][frame], (-40, 150))
    """



    # event loop, iterate through all the events that pygame picks up, can check for a specific event, checks for all possible player input
    for event in pygame.event.get():
        #closes game window, X on window

        if event.type == pygame.QUIT:
            run = False
        """
        if event.type == pygame.KEYDOWN: #if a key is pressed down
            if event.key == pygame.K_RIGHT:
                player_action = 1

        else:
            player_action = 0
        """



    #updates the display for the all the changes that happens
    pygame.display.update()

    # should not run faster than 60 times per second
    clock.tick(FPS)

pygame.quit()