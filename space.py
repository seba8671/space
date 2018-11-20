# Save this file as something meaningful!
# Unless you want your game to be callled skeleton...

import pygame
from pygame.math import Vector2
import random
import time

# Setup
pygame.init()

WHITE = (255, 255, 255)
RED =   (255,   0,   0)
BLACK = (  0,   0,   0)

# Screen
size = [400, 600]
screen = pygame.display.set_mode(size)

# Objects and variables
done = False
clock = pygame.time.Clock()
x_speed = 0
y_speed = 0
small_font = pygame.font.SysFont("Arial", 12)
hit_count = 0
spawnrate = 8
level_count = 0
life_count = 3

# Make Ship a subclass of Sprite.
# This means that all the operations that the Sprite class has will be
# something that the Ship class can do.
# We say "Ship inherits from Sprite"
class Ship(pygame.sprite.Sprite):
    # All classes must have an __init__ method.
    # All data that a class uses must be initialised in the __init__ method.
    # Each data element is called a field.
    def __init__(self):
        # First make sure the base class is initialised.
        pygame.sprite.Sprite.__init__(self)

        # This ship will have a speed as internal data as a Vector2, which
        # set to (0,0) initially.
        self.speed = Vector2(0, 0)

        # Spirtes should have an image field. In this caes we load the image
        # from a file on disk and scale it so it is suitable for our screen.
        self.image = pygame.image.load('UFO.jpg')
        self.image = pygame.transform.scale(self.image, (46, 78))

        # pygame uses the rect field of a Spirte to draw the Sprite, but also
        # to calculate collisions so we have to initialise it.
        # We take the rect from the image field and then we change the x and y
        # fields of the rect in order to place the Ship on the right spot on the
        # screen.
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 500

        # The update method of the Sprite class doesn't do anything. The purpose of
        # it is to provide a hook for you to provide a way to update your class in
        # a way that fits with the basic features of pygame.
        # In this caes we just move the rect with the coordinates of the speed vector.
    def update(self):
        if self.speed.x < 0:
            if self.rect.left > 0:
                self.rect.x += self.speed.x
                self.rect.y += self.speed.y
        elif self.speed.x > 0:
            if self.rect.right < size[0]:
                self.rect.x += self.speed.x
                self.rect.y += self.speed.y

class Comet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        randomangle = random.uniform(-0.10,0.10)
        randomspeed_y = random.randint(3,6)
        self.speed = Vector2(randomangle,randomspeed_y)
        randomcometsize = random.randint(10, 30)
        self.image = pygame.image.load('comet.jpg')
        self.image = pygame.transform.scale(self.image, (randomcometsize, randomcometsize))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        if self.rect.y > size[1]+1:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x_bullet = player_ship.speed.x / 3
        self.speed = Vector2(x_bullet,-5)
        self.image = pygame.image.load('lazer.png')
        self.image = pygame.transform.scale(self.image, (12, 19))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        if self.rect.y < -19:
            self.kill()


# Create Objects
# All the objects to be on the screen when the game starts.
player_ship = Ship()


# Handle sprites
# Create as many Sprite groups as you need to make things easy to manage.
# all_sprites contains all the objects we'll ever create. All objects must be
# added to the all_sprites Group for things to work.
all_sprites = pygame.sprite.Group()
all_sprites.add(player_ship)
all_bullets = pygame.sprite.Group()
all_comets = pygame.sprite.Group()


# -------- Main Program Loop -----------
# we use the global variable done to control when to end the game.
while not done:
    # --- Event Processing
    # Get all events from keyboard and/or mouse.
    for event in pygame.event.get():
        # if you click the x in the window top the game will end
        if event.type == pygame.QUIT:
            done = True

        # if you press a key and it is either A or D change the speed of
        # the x_speed variable.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                    x_speed = -5
            elif event.key == pygame.K_d:
                    x_speed = 5
            elif event.key == pygame.K_SPACE:
                bullet = Bullet()
                bullet.rect.x = player_ship.rect.centerx
                bullet.rect.y = 500
                all_sprites.add(bullet)
                all_bullets.add(bullet)


        # When the A or D  key is released change the x_speed to 0.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                if x_speed < 0:
                    x_speed = 0
            elif event.key == pygame.K_d:
                if x_speed > 0:
                    x_speed = 0



    # --- Game Logic
    # Update variables
    player_ship.speed.x = x_speed
    all_sprites.update()

    if random.randint(1,spawnrate)==1:
        comet = Comet()
        randompos_x = random.randint(5, size[0]-5)
        comet.rect.x = randompos_x
        comet.rect.y = 0
        all_sprites.add(comet)
        all_comets.add(comet)


    # Collisions
    # Read the documentation of groupcollide very carefully and figure out
    # how the arguments woraak.
    hit_list = pygame.sprite.groupcollide(all_comets, all_bullets, True, True)
    hit_count += len(hit_list)
    level_count += len(hit_list)

    if level_count >= 75:
        spawnrate -= 1
        spawnrate = max(spawnrate, 2)
        level_count -= 75
    elif level_count >= 75:
        if collision:
            level_count += spawnrate

    collision = pygame.sprite.spritecollideany(player_ship, all_comets)
    if collision != None:
        life_count -= 1
        for comet in all_comets:
            comet.kill()
        if life_count <= 0:
            done = True


    # --- Draw
    # When using Sprite groups it is super easy to update the screen:
    # 1. Clear the screen.
    # 2. Call the draw method of the all_sprites Group using the screen as the
    #    only argument.
    screen.fill(WHITE)
    all_sprites.draw(screen)

    life_text = small_font.render("lifes: " + str(life_count), 1, RED)
    screen.blit(life_text, (10, 25))

    hit_text = small_font.render("score: " + str(hit_count), 1, BLACK)
    screen.blit(hit_text, (10, 10))

    # Update screen
    # pygame will draw the screen in the background and only when it is time
    # to update it will it be shown on the screen.
    clock.tick(30)  # update the screen 30 times every second.
    pygame.display.flip()


# When we break out of the gmae loop there is nothing to do but..
# Close the window and quit.
pygame.quit()
