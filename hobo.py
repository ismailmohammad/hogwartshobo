import pygame
import random
import time

pygame.init()
screen_width = 1200
screen_height = 600
fps = 30

finish = False
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hogwarts Hobo')
clock = pygame.time.Clock()


hobos = pygame.sprite.Group()
hobo = pygame.image.load('images/sprite_0.png')
user_hobos = pygame.sprite.Group()

train = pygame.image.load('images/train.png')


game_sprites = pygame.sprite.Group()
backgroundImage = pygame.image.load('images/background.png')

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

    # Checks car collision with frogs
    def collision(self):
        for hobo in user_hobos:
            if (self.rect.colliderect(hobo) and hobo.dead == False):
                hobo.hurt()

class Hobo(pygame.sprite.Sprite):
    dead = False
    health = 100

    def __init__(self, xpos, ypos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.size = size
        self.image = hobo

    # Update hobo position based on key presses
    def update(self, direction):
        # direction being 1 for up and -1 for down
        if (direction == 1):
            self.rect.y -= 112.5
            # go down
        elif (direction == -1):
            self.rect.y += 112.5
            
                

    # If hobo is hurt, decrease health as necessary
    def hurt(self):
        # self.image = frogDead
        # self.dead = True
        self.health -= 5
        if self.health == 0:
            self.dead = True
            self.kill()
            print("game over, your hobo died lol")
            pygame.quit()
            quit()
        print("HObo Health: " + str(self.health))

# Make the user hobo then init game with it
# (x,y, size)
user_hobo = Hobo(1000,200,100)

# Sets and resets the game screen
def initialize_game(user_hobo):

    for sprite in game_sprites:
        sprite.kill()

    #  change thihs up later to randomize them tings
    train_speed = 3
    # set the width and height of dem trains
    (width, height) = (100, 50)
    first_train_y  = 270
    # set up hobo on the tracks too
    user_hobo.rect.y = first_train_y
    # Create 3 trains (randomize frequency and speeed later)
    # (x, y,speed, direction, width, height)
    for i in range(0, 3):
        if (i == 1):
            game_sprites.add(Train(50 + 150 * (12 - i), first_train_y, train_speed, -1, width, height))
        elif i == 2:
            game_sprites.add(Train(50 + 150 * (12 - i * 5), first_train_y + 112.5 , train_speed + 2, -1, width, height))
        else:
            game_sprites.add(Train(50 + 150 * (12 - i * 5), first_train_y + 225, train_speed + 4, -1, width, height))
    # add the user controlled hobo man ting
    user_hobos.add(user_hobo)

initialize_game(user_hobo)

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                user_hobo.update(1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                user_hobo.update(-1)
            

    screen.blit(backgroundImage, (0, 0))

    # draw the user hobo onto the screen
    user_hobos.update(0)
    user_hobos.draw(screen)

    game_sprites.update()
    game_sprites.draw(screen)
    # to be used later to create bare hobos
    # hobos.update()
    # hobos.draw(screen)

    pygame.display.update()
    clock.tick(fps)


pygame.quit()
quit()