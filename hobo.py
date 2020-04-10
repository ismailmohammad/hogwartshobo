import pygame
from pygame.locals import *
import time
import os

pygame.init()
screen_width = 1295
screen_height = 800
fps = 360

finish = False
quit_induced = False
game_over = False

# IMPORTANT: Uncomment one or the other for debug purposes, not a lot of screen switching, debug use w/o FS

# screen=pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
screen=pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Hogwarts Hobo')

clock = pygame.time.Clock()

# Steps of 117 ie. divisible by 9 sprite frames
TRAIN_POSITIONS = [270, 387, 504]
INITIAL_Y = TRAIN_POSITIONS[0]
INITIAL_X = 200
HOBO_SPEED = 13
# reimplement plnae/train speed  later to change things up randomize
TRAIN_SPEED = 5
PLANE_SPEED = 4
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
# Used because the sprites in group are hashed, simplicity sake
hearts = []

# Create trains sprite group
trains = pygame.sprite.Group()

# Create planes sprite group
planes = pygame.sprite.Group()

# Set up them music (Feel free to replace the music peeps)
pygame.mixer.music.load('media/bg_music.mp3') 
pygame.mixer.music.play(-1,0.0)
# Set up Damage sound upon collision
damage_sound_effect = pygame.mixer.Sound('media/not_the_roblox_death_sound.wav')
# Game over music
gameover_sfx = 'media/game_over.mp3'
game_over_img = pygame.image.load('images/game_over.png')


class PaperPlane(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/paperplane.png')
        # resize the image to the desired size as indicated
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if (self.rect.x - self.rect.width+100 > screen_width):
            self.kill()


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
    def __init__(self, startX, startY, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/train.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY
        self.speed = speed

    # Update train position
    def update(self):
        collided = self.collision()
        if collided:
            yum = "lol"
        else:
            # Trains will only move towards the Hobo, hence the increase in x position
            self.rect.x += self.speed
            # Once the train reaches the end of the scene it then loops around
            if (self.rect.x - self.rect.width > screen_width):
                self.rect.x = -self.rect.width

    def collision(self):
        for hobo in user_sprites:
            if (self.rect.colliderect(hobo) and hobo.dead == False):
                hobo.hit()
                return True
            return False
                

class Hobo(pygame.sprite.Sprite):
    dead = False
    health = MAX_HEALTH

    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.hurt_image = pygame.image.load('images/sprite_hurt.png').subsurface((8,5,55,77)).convert_alpha()
        self.images = []
        # Load all the sprite images into the image array
        for index in range(9):
            sprite_frame = pygame.image.load(os.path.join('images','sprite_' + str(index) + '.png')).convert_alpha()
            # simply get a subframe and use that as the sprite (constraining the hitbox of the hobo to closer to body)
            sprite_frame = sprite_frame.subsurface((0,5,55,77))
            self.images.append(sprite_frame)
        # Select the default sprite img
        self.image = self.images[self.frame_index]
        # self.image = self.hurt_image
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    # Update hobo position based on key presses
    def update(self, direction, speed):
        # direction being 1 for up and -1 for down
        if (direction == 1 and self.rect.y > TRAIN_POSITIONS[0]):
            self.animateMovement(speed) # Go down a track
        elif (direction == -1 and self.rect.y < TRAIN_POSITIONS[2]):
            self.animateMovement(speed, False) # Go up a track

    def animateMovement(self, step, up=True):
        self.frame_index = 0
        for frame in self.images:
            self.changeSpriteFrame()
            if up:
                self.rect.y -= step/2
            else:
                self.rect.y += step/2
            render()
            if up:
                self.rect.y -= step - (step/2)
            else:
                self.rect.y += step - (step/2)
            render()

    def changeSpriteFrame(self):
        self.frame_index += 1
        if self.frame_index == len(self.images):
            self.frame_index = 0
        self.image = self.images[self.frame_index]
        

    def hit(self):
        self.health -= 1
        self.image = self.hurt_image
        self.image.set_colorkey(0)
        self.image.set_alpha(100)
        damage_sound_effect.play()
        # Kill/Remove the heart at the end of health indicator based on health intervals
        if (self.health in [0,25,50,75]):
            hearts[len(user_health.sprites()) - 1].kill()
        if self.health == 0:
            self.dead = True
            self.image = self.hurt_image
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
    user_hobo = Hobo(1000,INITIAL_Y)
    user_sprites.add(user_hobo)
    # Populate the user's health indicator
    heart_number = 0
    heart_size = 50
    while heart_number < NUMBER_HEARTS:
        heart = Heart(0 + (heart_number * heart_size), backgroundImage.get_rect().height + 5, heart_size)
        user_health.add(heart)
        hearts.append(heart)
        heart_number += 1
    # Create 3 trains (randomize frequency and speeed later)
    # (xpos, ypos,speed)
    trains.add(Train(50 + 150 * (12 - 1), TRAIN_POSITIONS[0], TRAIN_SPEED))
    trains.add(Train(50 + 150 * (12 - 2 * 5), TRAIN_POSITIONS[1] , TRAIN_SPEED + 1))
    trains.add(Train(50 + 150 * (12 - 3 * 5), TRAIN_POSITIONS[2], TRAIN_SPEED + 2))
    # Create a sample paper plane: to be generated randdomly via Poisson process soon
    # Create 3 one on each track for debug
    for i in range(3):
        plane = PaperPlane(0, TRAIN_POSITIONS[i], PLANE_SPEED + i, 60)
        planes.add(plane)

def render(hoboMoving = False):
    # Render Sequence: fill black -> bg -> user hobo -> trains -> health
    screen.fill(0)
    screen.blit(backgroundImage, (0, 0))
    user_sprites.update(0, 0)
    user_sprites.draw(screen)
    if game_over:
        screen.blit(game_over_img, (screen.get_rect().centerx - (game_over_img.get_rect().width/2), backgroundImage.get_rect().height))
    trains.update()
    # Draw trains
    trains.draw(screen)
    # Update and draw planes
    planes.update()
    planes.draw(screen)
    # Draw the user's health onto the screen
    user_health.draw(screen)
    pygame.display.update()


# Add the sprites into their respective groups then start
addSprites()
# Introduce a slight waiting period to ensure load/switch to fullscreen
pygame.time.delay(100)

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            quit_induced = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                user_sprites.update(1, HOBO_SPEED)
                print("y: " + str(user_hobo.rect.y));
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                user_sprites.update(-1, HOBO_SPEED)
                print("y: " + str(user_hobo.rect.y));
    render()
    clock.tick(fps)
    if (game_over):
        finish = True

# Render Final Frame and wait x seconds before exiting (enough time for sfx to play)
# To quit normally on a ctrl-c in terminal or x if windowed
if not quit_induced:
    render()
    pygame.time.wait(9000)
pygame.quit()
quit()