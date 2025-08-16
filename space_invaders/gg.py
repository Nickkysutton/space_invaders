import math
import random
from pygame.locals import *
import pygame
from pygame import mixer
import time
# Intialize the pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

mixer.music.load('background.wav')
#mixer.music.play(-1)

pygame.display.set_caption("Blast through space")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)


textX = 10
testY = 10

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# create enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#powerups
def powerup(score_value):
    """Increase the number of shots when score is a multiple of 5."""
    global num_of_shots
    if score_value % 5 == 0 and score_value != 0:
        num_of_shots += 1
        powerupSound = mixer.Sound("videogame-power-up-sound-effect-01-no-copyright-352863.mp3")
        powerupSound.play()
        print(f"Power-up activated! Number of shots increased to {num_of_shots}")
# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
num_of_shots = 1

life = 3

# draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# collision detection, find distance between (x1,y1) and (x2,y2)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def set_background():
    global background
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))


def move_bullet():
    global bulletX, bulletY, bullet_state
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


def game_input():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change,score_value
    # Enemy Movement
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]


        enemy(enemyX[i], enemyY[i], i)


def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value, life
    for i in range(num_of_enemies):
        # Collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:

            if bullet_state == "fire":
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
            else:
                life -= 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

# Game Loop
running = True
while running:
    powerup(score_value)
    set_background()
    game_input()
    enemy_movement()
    collision()
    move_bullet()
    if life <=0 :
        score = font.render("GAME OVER ", True, (255, 0, 0))
        screen.blit(score, (200, 300))
        #time delay
        time.sleep(5)
        running = False

    player(playerX, playerY)
    score = font.render("life : " + str(life), True, (255, 255, 255))
    screen.blit(score, (400, 10))

    show_score(textX, testY)
    pygame.display.update()

