import math
import random
import os
#hides the pygame message in terminal 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer

#start up pygame
pygame.init()

#window size set up
screen = pygame.display.set_mode((800, 600))


buttons = pygame.image.load(
    "selected-buttons.png").convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
pause_button = buttons.subsurface(rect).copy()

#fetch background Image
background = pygame.image.load('background.png')

#sound effects
mixer.music.load("background_song.wav")
#loop music indefinitely
mixer.music.play(-1)

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#fonts
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 40, bold=True)

#game name on tab
pygame.display.set_caption("Corona Invader")

#player settings and coordinates
player_img = pygame.image.load('vp.png')
playerX = 375
playerY = 490
playerX_change = 0       

#enemy settings
enemy_img = []
enemyX = []
enemyY = []
global enemyX_change 
global enemyY_change
enemyX_change = []
enemyY_change = []
enemies_num = 2

for i in range(enemies_num):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(45, 140))
    enemyX_change.append(2)
    enemyY_change.append(10)

#bullet settings and state
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 475
bulletX_change = 0
bulletY_change = 4
#set state to ready 
bullet_state = "ready"

#points score and font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 35)

textX = 10
testY = 10

#Start Game text
start_font = pygame.font.Font('freesansbold.ttf', 30)

#gameover
end_font = pygame.font.Font('freesansbold.ttf', 64)

#display points on top left screen
def show_points(x, y):
    score = font.render("Points : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

#display start game page when you start
def start_game():
    start_game = start_font.render("Score 20 points to complete Level", True, (0, 0, 0))
    screen.blit(start_game, (300, 10))

#display game over page when you lose
def game_over_message():
    over_text = end_font.render("You Loose", True, (0, 0, 0))
    screen.blit(over_text, (210, 270))

#render player object
def player(x, y):
    screen.blit(player_img, (x, y))

#render enemy object
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

#render bullet object
def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#collision math
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 26:
        return True
    else:
        return False

#draw_level_cleared
def draw_level_cleared():
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    if score_value == 5:
        rect = pygame.Rect(100, 0, 600, 500)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))

    for i in range(enemies_num):
        enemy_img.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(45, 140))
        enemyX_change.append(0)
        enemyY_change.append(0)
            
        


#Loop the game
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    start_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #deciding movements: left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #release bullet sound effect if ready
                    bulletSound = mixer.Sound("shoot.wav")
                    bulletSound.play()
                    bulletX = playerX
                    shoot_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movements
    for i in range(enemies_num):

        #decides when game is over
        if enemyY[i] > 440:
            for j in range(enemies_num):
                enemyY[j] = 2000
            game_over_message()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        #collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #play explosion.wav when hit
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movements depending on state
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    draw_level_cleared()


    #return functions
    player(playerX, playerY)
    show_points(textX, testY)
    #update portions of screen
    pygame.display.update()
