import pygame
import random
import time
import os

MAX_HEALTH = 100.0
WHITE = (255,255,255)
FIRST_TRAIN_YPOS  = 270
TRACK_Y_TARGETS = [FIRST_TRAIN_YPOS, FIRST_TRAIN_YPOS + 112.5, FIRST_TRAIN_YPOS + 225]

pygame.init()
screen_width = 1295
screen_height = 620
fps = 60

finish = False
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hogwarts Hobo')
clock = pygame.time.Clock()


hobos = pygame.sprite.Group()

user_hobos = pygame.sprite.Group()

train = pygame.image.load('images/train.png')


game_sprites = pygame.sprite.Group()
backgroundImage = pygame.image.load('images/background.png')

# Set up them music (Feel free to replace the music peeps)
pygame.mixer.music.load('media/bg_music.mp3') 
pygame.mixer.music.play(-1,0.0)

damage_sound_effect = pygame.mixer.Sound('media/not_the_roblox_death_sound.wav')

# Set font for the Text
font = pygame.font.Font('freesansbold.ttf', 32) 


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
        for hobo in user_hobos:
            if (self.rect.colliderect(hobo) and hobo.dead == False):
                hobo.hurt()

class Hobo(pygame.sprite.Sprite):
    dead = False
    health = MAX_HEALTH

    def __init__(self, xpos, ypos, size):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.size = size
        self.images = []
        # Load all the sprite images into the image array
        for index in range(0,9):
            sprite_frame = pygame.image.load(os.path.join('images','sprite_' + str(index) + '.png'))
            self.images.append(sprite_frame)
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.surface = pygame.Surface((self.rect.width, self.rect.height))

    # Update hobo position based on key presses
    def update(self, direction):
        # direction being 1 for up and -1 for down
        if (direction == 1 and self.rect.y > 270):
            self.animateJump()
            self.rect.y -= 12.5
            # go down
        elif (direction == -1 and self.rect.y < 495):
            self.animateJump()
            self.rect.y += 12.5


    def animateJump(self):
        self.frame_index += 1
        if self.frame_index == len(self.images):
            self.frame_index = 0
        self.image = self.images[self.frame_index]

    def displayName(self):
        text , tr = displayMessage("Not Bob", font, WHITE)
        self.surface.blit(text, tr)

    def updateHealth(self):
        # Set initial color to Green
        self.bar_color = (0,255,0)
        self.health_bar_width = (self.health / MAX_HEALTH) * 50.00
        
    # If hobo is hurt, decrease health as necessary
    def hurt(self):
        self.health -= 1
        self.updateHealth()
        damage_sound_effect.play()
        if self.health == 0:
            self.dead = True
            self.kill()
            print("game over, your hobo died lol")
            pygame.quit()
            quit()
        print("HObo Health: " + str(self.health))


def displayMessage(text, font, color):
    text = font.render(text, True, color)
    text_rectangle = text.get_rect()
    return (text, text_rectangle)
        


# Make the user hobo then init game with it
# (x,y, size)
user_hobo = Hobo(1000,200,50)

# Sets and resets the game screen
def initialize_game(user_hobo):

    for sprite in game_sprites:
        sprite.kill()

    #  change thihs up later to randomize them tings
    train_speed = 1
    # set the width and height of dem trains
    (width, height) = (100, 50)
    # set up hobo on the tracks too
    user_hobo.rect.y = FIRST_TRAIN_YPOS
    # Create 3 trains (randomize frequency and speeed later)
    # (x, y,speed, direction, width, height)
    for i in range(0, 3):
        if (i == 1):
            game_sprites.add(Train(50 + 150 * (12 - i), FIRST_TRAIN_YPOS, train_speed, -1, width, height))
        elif i == 2:
            game_sprites.add(Train(50 + 150 * (12 - i * 5), FIRST_TRAIN_YPOS + 112.5 , train_speed + 2, -1, width, height))
        else:
            game_sprites.add(Train(50 + 150 * (12 - i * 5), FIRST_TRAIN_YPOS + 225, train_speed + 4, -1, width, height))
    # add the user controlled hobo man ting
    user_hobos.add(user_hobo)

initialize_game(user_hobo)

# Display Health Text
ht_surface, ht_rect = displayMessage("Health:", font, WHITE)
ht_rect.y += 5
ht_rect.x += 5


while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                for i in range (9):
                    user_hobo.update(1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                for i in range (9):
                    user_hobo.update(-1)
            

    screen.blit(backgroundImage, (0, 0))

    # draw the user hobo onto the screen
    user_hobos.update(0)
    user_hobos.draw(screen)

    user_hobo.displayName()

    game_sprites.update()
    game_sprites.draw(screen)
    # to be used later to create bare hobos
    # hobos.update()
    # hobos.draw(screen)

    pygame.display.update()
    clock.tick(fps)


pygame.quit()
quit()