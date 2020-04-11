import pygame
from pygame.locals import *
import time
import os
import random

pygame.init()
screen_width = 1295
screen_height = 800
fps = 120

finish = False
quit_induced = False
game_over = False
game_start = False
automated = False

var_prompt = raw_input("Do you want to input certain variables? Type y or Y to continue: \n")
if (var_prompt == "y" or var_prompt == "Y"):
    # Tracks at this time will not be user selectable (however can be easily expanded to render more
    # tracks and simply expand the TRAIN positions to M tracks and loop and increment each by the frame
    # step in this case 117 pixels
    hobo_num = raw_input("How many hobos at the exit? (whole numbers only 0 to x)")
    try:
        hobo_num = int(hobo_num)
    except:
        print("Error: Please enter Whole numbers 0 and greater only.")

# IMPORTANT: Uncomment one or the other for debug purposes, not a lot of screen switching, debug use w/o FS

# screen=pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
screen=pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Hogwarts Hobo')

clock = pygame.time.Clock()

# Steps of 117 ie. divisible by 9 sprite frames
TRAIN_POSITIONS = [270, 387, 504]
HOBO_Y = TRAIN_POSITIONS[0]
HOBO_X = 1100
HOBO_SPEED = 13
# reimplement plnae/train speed  later to change things up randomize
TRAIN_SPEED = 2
PLANE_SPEED = 1
MAX_HEALTH = 100
NUMBER_HEARTS = 4
# Number of opponents/other hobos
NUMBER_HOBOS = 3
# Reassign hobo number if input was valid
if type(hobo_num) == int:
    NUMBER_HOBOS = hobo_num

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Set up splash screen
splash_screen = pygame.image.load('images/splash.png').convert_alpha()
# Set up background image - 1295 x 620 px
background_image = pygame.image.load('images/background.png').convert_alpha()

# Create Sprite group for the user's char
user_sprites = pygame.sprite.Group()
# Create global variable user_hobo to be initialized later
user_hobo = 0
# Create a group to hold the user's health indicator
user_health = pygame.sprite.Group()
# Used because the sprites in group are hashed, simplicity sake
hearts = []

# Group to contain other hobos
other_hobos = pygame.sprite.Group()

# Create trains sprite group
trains = pygame.sprite.Group()

# Create planes sprite group
planes = pygame.sprite.Group()

# Create messages sprite
messages = pygame.sprite.Group()
# Used to keep track of messages in order as they present themselves since the Group is hashed instead
message_list = []

# Set up them music (Feel free to replace the music peeps)
pygame.mixer.music.load('media/bg_music.mp3') 
pygame.mixer.music.play(-1,0.0)
# Set up Damage sound upon collision
damage_sound_effect = pygame.mixer.Sound('media/not_the_roblox_death_sound.wav')
# Game over music
gameover_sfx = 'media/game_over.mp3'
game_over_img = pygame.image.load('images/game_over.png').convert_alpha()

class Message(pygame.sprite.Sprite):
    def __init__(self, y_pos, time, text, x_pos = "center"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/scroll.png').convert_alpha()
        self.rect = self.image.get_rect()
        if x_pos == "center":
            self.rect.x = screen.get_rect().centerx - (self.rect.width/1.9)
        else:
            self.rect.x = x_pos
        self.rect.y = y_pos
        self.display_time = time
        self.start = pygame.time.get_ticks()
        self.text = text

    def update(self):
        # Only display if time hasn't passed
        if not (pygame.time.get_ticks() - self.start) >= self.display_time:
            self.renderText()

    def renderText(self):
        screen.blit(self.image, self.rect)
        font_size = 68
        font = pygame.font.Font('fonts/mystic.ttf', font_size) # default pygame font
        render_surface = font.render(self.text, True, BLACK)
        render_rect = render_surface.get_rect()
        render_rect.center = self.rect.center
        screen.blit(render_surface, render_rect)



class PaperPlane(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, speed, size, train):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/paperplane.png').convert_alpha()
        # resize the image to the desired size as indicated
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed
        self.train = train

    def update(self):
        self.rect.x += self.speed
        # Once the planereaches the Hobo.
        if (self.rect.x == HOBO_X):
            # Display the message
            messages.add(Message(0, 600, "Train on " + str(self.train)))
            # Kill the sprite, the plane is discarded. Though no one should litter.
            # The paper is recycled.
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/heart.png').convert_alpha()
        # resize the image to the desired size as indicated
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


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
            # CHANGE TO KILL ONCE RANDOMIZED GENERATION COMPLETED.
            if (self.rect.x - self.rect.width > screen_width):
                self.rect.x = -self.rect.width

    def collision(self):
        for hobo in user_sprites:
            if (self.rect.colliderect(hobo) and hobo.dead == False and not hobo.switching):
                hobo.hit()
                return True
        for other_hobo in other_hobos:
            if (self.rect.colliderect(other_hobo) and other_hobo.dead == False and not other_hobo.switching):
                other_hobo.hit()
                return True
        return False
                

class Hobo(pygame.sprite.Sprite):
    dead = False
    health = MAX_HEALTH

    def __init__(self, x_pos, y_pos, sprite_type = "user"):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.sprite_type = sprite_type
        if sprite_type == "other":
            self.hurt_image = pygame.image.load('images/oh_hurt.png').subsurface((8,5,55,77)).convert_alpha()
        else:
            self.hurt_image = pygame.image.load('images/sprite_hurt.png').subsurface((8,5,55,77)).convert_alpha()
        self.images = []
        # Load all the sprite images into the image array
        if sprite_type == "other":
            img_type = "oh_"
        else:
            img_type = "sprite_"
        for index in range(9):
            sprite_frame = pygame.image.load(os.path.join('images',img_type + str(index) + '.png')).convert_alpha()
            # simply get a subframe and use that as the sprite (constraining the hitbox of the hobo to closer to body)
            sprite_frame = sprite_frame.subsurface((0,5,55,77))
            self.images.append(sprite_frame)
        # Select the default sprite img
        self.image = self.images[self.frame_index]
        # self.image = self.hurt_image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.collided = False
        self.switching = False

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

    """
    Gets the current track index of the Hobo, used to determine which tracks
    can be switched to, regardless of if they are occupied or not
    """
    def getCurrentTrack(self):
        try:
            position = TRAIN_POSITIONS.index(self.rect.y)
        except:
            position = None
        return position

    def chooseTrack(self):
        # Switch Tracks if collided/hit
        # Get current track
        current_track = self.getCurrentTrack()
        if current_track == None:
            return current_track
        # Instead of making it random track, change it soon to be one that's not thought to be
        # occupied
        random_track = random.choice(TRAIN_POSITIONS)
        # If the chosen track is the same choose another track
        while random_track == TRAIN_POSITIONS[current_track]:
            random_track = random.choice(TRAIN_POSITIONS)
        return random_track

    def switchTrack(self):
        current = self.getCurrentTrack()
        if current == None and not self.dead:
            return None
        else:
            current = TRAIN_POSITIONS[current]
        destination = self.chooseTrack()
        self.switching = True
        if destination < current:
            while self.rect.y != destination:
                self.update(1, HOBO_SPEED)
        else:
            while self.rect.y != destination:
                self.update(-1, HOBO_SPEED)
        self.switching = False


    def hit(self):
        self.health -= 25
        self.collided = True
        self.image = self.hurt_image
        self.image.set_colorkey(0)
        self.image.set_alpha(100)
        damage_sound_effect.play()
        if automated:
            pygame.event.pump()
            self.switchTrack()
        # Kill/Remove the heart at the end of health indicator based on health intervals
        if (self.health in [0,25,50,75] and self.sprite_type != "other"):
            hearts[len(user_health.sprites()) - 1].kill()
        if self.health <= 0:
            self.dead = True
            self.image = self.hurt_image
            self.kill()
        print("HObo Health: " + str(self.health))

def addSprites():
    # Create the user's hobo and add it to the Sprite group of user controlled sprites
    global user_hobo
    user_hobo = Hobo(HOBO_X,HOBO_Y)
    user_sprites.add(user_hobo)
    # Populate the user's health indicator
    heart_number = 0
    heart_size = 50
    while heart_number < NUMBER_HEARTS:
        heart = Heart(0 + (heart_number * heart_size), background_image.get_rect().height + 5, heart_size)
        user_health.add(heart)
        hearts.append(heart)
        heart_number += 1
    # Create 3 trains (randomize frequency and speeed later)
    # (x_pos, y_pos,speed)
    trains.add(Train(50 + 150 * (12 - 1), TRAIN_POSITIONS[0], TRAIN_SPEED))
    trains.add(Train(50 + 150 * (12 - 2 * 5), TRAIN_POSITIONS[1] , TRAIN_SPEED + 1))
    trains.add(Train(50 + 150 * (12 - 3 * 5), TRAIN_POSITIONS[2], TRAIN_SPEED + 2))
    # Create a sample paper plane: to be generated randdomly via Poisson process soon
    # Create 3 one on each track for debug
    # (x_pos, y_pos (track), speed, size, tracknum)
    planes.add(PaperPlane(0, TRAIN_POSITIONS[0], PLANE_SPEED + (1 * 0.5), 60, 1))
    planes.add(PaperPlane(0, TRAIN_POSITIONS[1], PLANE_SPEED + (2 * 0.5), 60, 2))
    planes.add(PaperPlane(0, TRAIN_POSITIONS[2], PLANE_SPEED + (3 * 0.5), 60, 3))

def addOtherHobos(number_hobos):
    for hobo in range(number_hobos):
        pc_hobo = Hobo(HOBO_X, (HOBO_Y + (117 * random.choice([1,2])) ), "other")
        other_hobos.add(pc_hobo)
  

def render(hobo_moving = False):
    # Render Sequence: fill black -> bg -> user hobo -> trains -> health
    screen.fill(0)
    screen.blit(background_image, (0, 0))
    user_sprites.update(0, 0)
    user_sprites.draw(screen)
    other_hobos.update(0, 0)
    other_hobos.draw(screen)
    if game_over:
        screen.blit(game_over_img, (screen.get_rect().centerx - (game_over_img.get_rect().width/2), background_image.get_rect().height))
    if not hobo_moving and (not game_over):
        trains.update()
    # Draw trains
    trains.draw(screen)
    # Update and draw planes
    planes.update()
    planes.draw(screen)
    # Update and draw any messages
    messages.update()
    # Draw the user's health onto the screen
    user_health.draw(screen)
    pygame.display.update()


# Add the sprites into their respective groups then start
addSprites()

# Show Splash screen
while not game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == ord('q'):
                pygame.quit()
                quit()
            if event.key == pygame.K_m or event.key == ord('m'):
                game_start = True
            if event.key == pygame.K_a or event.key == ord('a'):
                addOtherHobos(NUMBER_HOBOS)
                game_start = True
                automated = True
        screen.fill(0)
        screen.blit(splash_screen, (0, 0))
        pygame.display.update()
        clock.tick(fps)
    
# Start Game
while not finish and game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            quit_induced = True
        if event.type == pygame.KEYDOWN:
            # Press Q to quit
            if event.key == pygame.K_q or event.key == ord('q'):
                pygame.quit()
                quit()
            if not automated:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    user_sprites.update(1, HOBO_SPEED)
                    print("y: " + str(user_hobo.rect.y));
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    user_sprites.update(-1, HOBO_SPEED)
                    print("y: " + str(user_hobo.rect.y));
    global game_over
    if (len(user_sprites) == 0 and len(other_hobos) == 0):
        game_over = True
        print("game over, all hobo died lol")
    render()
    clock.tick(fps)
    if (game_over):
        break

# Render Final Frame and wait x seconds before exiting (enough time for sfx to play)
# To quit normally on a ctrl-c in terminal or x if windowed
if not quit_induced:
    render()
    # Play game over sfx
    pygame.mixer.music.load(gameover_sfx) 
    pygame.mixer.music.play()
    pygame.time.wait(9000)
pygame.quit()
quit()