import pygame
from pygame.locals import *
import random 


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 120
PIPE_HEIGHT = 500
PIPE_GAP = 200
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando as imagens
        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                      pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                      pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        
        self.speed = SPEED
        
        #Trocando as imagens
        self.current_image = 0
        
        
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        #4 parametros , 1º,2º canto superior esquerdo , 3º e 4º o tamanho
        self.rect = self.image.get_rect() 
        
        #posicionando o passaro
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2
        
        print(self.rect)  
        
    def update(self):
        
        #Batendo as asas
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
         
        #forçando ele descer 
        self.speed += GRAVITY
         
        #Atualzando altura
        self.rect[1] += self.speed
        
    def bump(self):
        #Subindo
        self.speed = -SPEED
        
class Pipe(pygame.sprite.Sprite):
    
    def __init__(self,inverted,xpos,ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))
        
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        
        if inverted:
            #Cano invertido
            self.image = pygame.transform.flip(self.image, False, True)      
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            #Cano normal
            self.rect[1] = SCREEN_HEIGHT - ysize
            
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect[0] -= GAME_SPEED
class Ground(pygame.sprite.Sprite):
    def __init__(self,xpos):
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()  
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH,GROUND_HEIGHT))  
        
        self.mask = pygame.mask.from_surface(self.image)
        
        #4 parametros , 1º,2º canto superior esquerdo , 3º e 4º o tamanho
        self.rect = self.image.get_rect()    

        self.rect[0] = xpos
        #posicionando o chão na parte de baixo da tela
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
                
    def update(self):
        #Velocidade com que o chão se move
        self.rect[0] -= GAME_SPEED
        
def is_off_screen(sprite):
    #VErifica se o sprite saiu da tela
    return sprite.rect[0] < -(sprite.rect[2])
        
def get_random_pipes(xpos):
    size = random.randint(100,300)
    pipe = Pipe(False,xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return(pipe,pipe_inverted)

pygame.init()

#Defininfo o tamanho da tela
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Carregando o background
BACKGROUND = pygame.image.load('assets/sprites/background-day.png')

#Redimensionando o tamanho do arquivo background
BACKGROUND = pygame.transform.scale(BACKGROUND,(SCREEN_WIDTH,SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    #Deixando o chão continuo
    ground = Ground(SCREEN_WIDTH * i)
    ground_group.add(ground)
    
pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    

clock = pygame.time.Clock()


while True:
    
    #Definindo fps
    clock.tick(20)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
            
    screen.blit(BACKGROUND,(0,0))
    
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        
        new_ground =  Ground(GROUND_WIDTH - 430) 
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
    ground_group.draw(screen)
    pipe_group.draw(screen)
    
    if (pygame.sprite.groupcollide(bird_group,ground_group,False,False, pygame.sprite.collide_mask)) or (pygame.sprite.groupcollide(bird_group,pipe_group,False,False, pygame.sprite.collide_mask)):
       
        #GAME OVER
        break 
    
    pygame.display.update() 