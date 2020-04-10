import pygame
from pygame.locals import *
import time
import os

pygame.init()
screen_width = 1295
screen_height = 800
fps = 30

finish = False
game_over = False
screen=pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
# screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hogwarts Hobo')
clock = pygame.time.Clock()

# Steps of 117 ie. divisible by 9 sprite frames
TRAIN_POSITIONS = [270, 387, 504]
INITIAL_Y = TRAIN_POSITIONS[0]
INITIAL_X = 200
HOBO_SPEED = 13
# reimplement later to change things up
TRAIN_SPEED = 5
MAX_HEALTH = 100
NUMBER_HEARTS = 4

# Set up background image - 1295 x 620 px
backgroundImage = pygame.image.load('images/background.png')

# Create Sprite group for the user's char
user_sprites = pygame.sprite.Group()
# Create global variable user_hobo to be initialized later
user_hobo = 0
# Create a group to hold the user's health indicator
user_health = pygame.sprite.Group()

# Load the train image and create sprite 
train = pygame.image.load('images/train.png')
trains = pygame.sprite.Group()

# Set up them music (Feel free to replace the music peeps)
pygame.mixer.music.load('media/bg_music.mp3') 
pygame.mixer.music.play(-1,0.0)
# Set up Damage sound upon collision
damage_sound_effect = pygame.mixer.Sound('media/not_the_roblox_death_sound.wav')
# Game over music
gameover_sfx = 'media/game_over.mp3'
game_over_img = pygame.image.load('images/game_over.png')


class Heart(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/heart.png')
        # resize the image to the desired size as indicated
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos


class Train(pygame.sprite.Sprite):
    def __init__(self, startX, startY, speed, direction, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY
        self.img = train
        self.speed = speed
        self.direction = direction  # -1 - left, 1 - right
        self.width = width  
        self.height = height
        self.image = train

    # Update train position
    def update(self):
        if (self.direction == -1):
            self.rect.x += self.speed
        elif (self.direction == 1):
            self.rect.x -= self.speed

        if (self.direction == -1 and self.rect.x - 75 > screen_width):
            self.rect.x = -75
        elif (self.direction == 1 and self.rect.x + 75 < 0):
            self.rect.x = screen_width + 75
        self.collision()

    def collision(self):
        for hobo in user_sprites:
            if (self.rect.colliderect(hobo) and hobo.dead == False):
                hobo.hurt()

class Hobo(pygame.sprite.Sprite):
    dead = False
    health = MAX_HEALTH

    def __init__(self, xpos, ypos, size):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.size = size
        self.hurt_image = pygame.image.load('images/sprite_hurt.png').convert_alpha()
        self.images = []
        # Load all the sprite images into the image array
        for index in range(9):
            sprite_frame = pygame.image.load(os.path.join('images','sprite_' + str(index) + '.png')).convert_alpha()
            sprite_frame.set_colorkey(0)
            sprite_frame.set_alpha(0)
            self.images.append(sprite_frame)
        # Select the default sprite img
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    # Update hobo position based on key presses
    def update(self, direction, speed):
        # direction being 1 for up and -1 for down
        if (direction == 1 and self.rect.y > TRAIN_POSITIONS[0]):
            self.frame_index = 0
            for frame in self.images:
                self.changeSpriteFrame()
                self.rect.y -= 6
                render()
                self.rect.y -= 7
                render(True)
            # go down
        elif (direction == -1 and self.rect.y < TRAIN_POSITIONS[2]):
            self.frame_index = 0
            moved = 0
            for frame in self.images:
                self.changeSpriteFrame()
                self.rect.y += 6
                moved += 6
                render()
                self.rect.y += 7
                moved += 7
                render(True)
            print("moved down: " + str(moved))
                

    def changeSpriteFrame(self):
        self.frame_index += 1
        if self.frame_index == len(self.images):
            self.frame_index = 0
        self.image = self.images[self.frame_index]
        

    def updateHealth(self):
        # Set initial color to Green
        self.bar_color = (0,255,0)
        self.health_bar_width = (self.health / MAX_HEALTH) * 50.00

    def hurt(self):
        self.health -= 1
        # self.updateHealth()
        damage_sound_effect.play()
        if (self.health in [0,25,50,75]):
            for heart in user_health:
                heart.kill()
                
        if self.health == 0:
            self.dead = True
            self.kill()
            global game_over 
            game_over = True
            print("game over, your hobo died lol")
            # Play game over sfx
            pygame.mixer.music.load(gameover_sfx) 
            pygame.mixer.music.play()

        print("HObo Health: " + str(self.health))

def addSprites():
    # Create the user's hobo and add it to the Sprite group of user controlled sprites
    global user_hobo
    user_hobo = Hobo(1000,INITIAL_Y,50)
    user_sprites.add(user_hobo)
    # Populate the user's health indicator
    heart_number = 0
    heart_size = 50
    while heart_number < 4:
        user_health.add(Heart(0 + (heart_number * heart_size), backgroundImage.get_rect().height + 5, heart_size))
        heart_number += 1
    # set the width and height of the trains
    (width, height) = (100, 50)
    # Create 3 trains (randomize frequency and speeed later)
    # (x, y,speed, direction, width, height)
    trains.add(Train(50 + 150 * (12 - 1), TRAIN_POSITIONS[0], TRAIN_SPEED, -1, width, height))
    trains.add(Train(50 + 150 * (12 - 2 * 5), TRAIN_POSITIONS[1] , TRAIN_SPEED + 1, -1, width, height))
    trains.add(Train(50 + 150 * (12 - 3 * 5), TRAIN_POSITIONS[2], TRAIN_SPEED + 2, -1, width, height))

def render(hoboMoving = False):
    # bg -> hobo -> trains
    screen.blit(backgroundImage, (0, 0))
    # pygame.draw.rect(screen, colors[color_index], (x, y, 70, 70))
    user_sprites.update(0, 0)
    user_sprites.draw(screen)
    # Draw the user's health onto the screen
    user_health.draw(screen)
    if (not hoboMoving) and (not game_over):
        trains.update()
    if game_over:
        screen.blit(game_over_img, (screen.get_rect().centerx - (game_over_img.get_rect().width/2), backgroundImage.get_rect().height))
    trains.draw(screen)
    # pygame.draw.rect(screen, (0,0,0,25), (user_hobo.rect.x, user_hobo.rect.y, user_hobo.rect.height, user_hobo.rect.width))
    pygame.display.update()

    # screen.fill((0,0,0))


# Add the sprites into their respective groups then start
addSprites()

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                user_sprites.update(1, 12.5)
                print("y: " + str(user_hobo.rect.y));
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                user_sprites.update(-1, 12.5)
                print("y: " + str(user_hobo.rect.y));
    render()
    
    clock.tick(fps)

    if (game_over):
        finish = True
# Render Final Frame and wait x seconds before exiting
render()
time.sleep(10)
pygame.quit()
quit()