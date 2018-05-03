'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

2018

Aproveite!!!
'''
# Importações
import pygame
import sys
from pygame.locals import*
import random

# Variáveis
fps = 90
width = 1000
height = 600

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
dark_yellow = (25, 100, 37)
red = (255, 0, 0)

# Inicialização do básico do sistema
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mario só que é o Yoshi")
clock = pygame.time.Clock()

# Objetos
class Objeto(pygame.sprite.Sprite):
	def __init__(self, imagem, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagem)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Personagem
class Character(pygame.sprite.Sprite):
	def __init__(self, imagem, x, y, vel_mov, vel_jump):
		pygame.sprite.Sprite.__init__(self)
		self.attack = 0
		self.hp = 5
		self.mp = 5
		self.vl = vel_mov
		self.image = pygame.image.load(imagem)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.v_jump = vel_jump

	def moveleft(self):
		self.rect.x -= self.vl

	def moveright(self):
		self.rect.x += self.vl
		
	def jump(self):
		return jump

# Colisão
class Colision(Character):
	def __init__(self,ob1,ob2):
		Character.__init__(self)
		Objeto.__init__(self)
		self.rect1 = ob1.rect
		self.rect2 = ob2.rect

# Sprites
todos_sprites = pygame.sprite.Group()

# Chão
chao = Objeto("chao.png",0,530)
object_group = pygame.sprite.Group()
object_group.add(chao)
todos_sprites.add(chao)


# Personagem
personagem = Character("yoshi.png",40,480,2,5)
charac_group = pygame.sprite.Group()
charac_group.add(personagem)
todos_sprites.add(personagem)

fundo = pygame.image.load("fundo.png").convert()

# Looping principal
rodando=True
while rodando:
	clock.tick(fps)
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False

	if keys[pygame.K_a]:
		personagem.moveleft()
	elif keys[pygame.K_d]:
		personagem.moveright()
	elif keys[pygame.K_w]:
		personagem.jump()
	
	todos_sprites.update()
	tela.blit(fundo,(0,0))
	todos_sprites.draw(tela)
	pygame.display.flip()

pygame.quit()
