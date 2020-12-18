"""
Vapor Bird v.1.0
Daniel González

"""

import pygame, random
from pygame.locals import *

#valors independents
SCREEN_WIDTH = 393
SCREEN_HEIGHT = 700
SPEED = 10
GRAVITY = 1
GAME_SPEED = 5

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 100

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('../assets/Images/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('../assets/Images/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('../assets/Images/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('../assets/Images/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY

        #actualitzacio d'altura
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('../assets/Images/tuberia.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('../assets/Images/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

#fucntion to randomize the position of the pipes
def get_random_pipes(xpos):
    size = random.randint(100, 400)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

#function to pause the game
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused=False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(5)
        #gameDisplay.fill(white)
        #message_to_screen("Paused", balck, -100, size="large")

#Inicio el joc
pygame.init()
#nom finestra
pygame.display.set_caption("VaporBird")
#Inicio la musica de fons
pygame.mixer.init()
pygame.mixer.music.load("../assets/Sounds/backgroundmusic.mp3")
pygame.mixer.music.play(-1, 0.0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('../assets/Images/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

MENU_BACKGROUND = pygame.image.load('../assets/Images/menu-vaporbird.png')
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

rungame=True

#començament del joc - menu -
while True:
    #incluim un bucle dins d'un altre, de manera que el menu sera el de fora i al captar un event entrarem al joc.
    clock.tick(30)
    screen.blit(MENU_BACKGROUND,(0, 0))
    pygame.display.update() 

    for event in pygame.event.get():
        if event.type == QUIT:
            #run = False
            pygame.quit()
            exit()
            pygame.display.quit()
        
        elif event.type == KEYDOWN:
            
            if event.key == K_SPACE:
                
                #Un cop es prem l'espai s'incia el joc
                while rungame:
                    clock.tick(30)
                    
                    #atrapar els keyboard-events
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            #run = False
                            pygame.quit()
                            exit()
                            pygame.display.quit()
                        elif event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                bird.bump()
                            elif event.key == K_p:
                                pause()

                    screen.blit(BACKGROUND, (0, 0))

                    if is_off_screen(ground_group.sprites()[0]):
                        ground_group.remove(ground_group.sprites()[0])

                        new_ground = Ground(GROUND_WIDTH - 20)
                        ground_group.add(new_ground)

                    if is_off_screen(pipe_group.sprites()[0]):
                        pipe_group.remove(pipe_group.sprites()[0])
                        pipe_group.remove(pipe_group.sprites()[0])

                        pipes = get_random_pipes(SCREEN_WIDTH * 2)

                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                    bird_group.update()
                    ground_group.update()
                    pipe_group.update()

                    bird_group.draw(screen)
                    pipe_group.draw(screen)
                    ground_group.draw(screen)

                    pygame.display.update()
                    #pause()
                    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                        # Game over
                        print("game over")
                        break
