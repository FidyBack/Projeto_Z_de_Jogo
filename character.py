'''character'''
#objeto da classe ataque precisa de uma velocidade específica dos objetos de classe objeto
#pulo depende de estar em contato com o chao
#pulo usando a parede pode depencder de usar a parede
import pygame
import sys
from pygame.locals import*
from random import randrange

class Objeto(pygame.sprite.Sprite):
	def __init__(self,imagem,px,py):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(imagem)
		self.rect=self.image.get_rect()
		self.rect.x=px
		self.rect.y=py

class Character(pygame.sprite.Sprite):
	def __init__(self,imagem,px,py,vel_mov,vel_jump):
		pygame.sprite.Sprite.__init__(self)
		self.attack=0
		self.hp=5
		self.mp=5
		self.vl=vel_mov
		self.image=pygame.image.load(imagem)
		self.rect=self.image.get_rect()
		self.rect.x=px
		self.rect.y=py
		self.v_jump=vel_jump
	def moveleft(self):
		self.rect.x-=self.vl

	def moveright(self):
		self.rect.x+=self.vl

	def moveup(self):
		self.rect.y-=self.vl
	def movedown(self):
		self.rect.y+=self.vl		
	def jump(self):
		return jump

class Colision(Character):
	def __init__(self,ob1,ob2):
		Character.__init__(self)
		Objeto.__init__(self)
		self.rect1=ob1.rect
		self.rect2=ob2.rect



chao=Objeto("chao.png",0,530)
object_group = pygame.sprite.Group()
object_group.add(chao)

personagem=Character("yoshi.png",40,480,1,5)
charac_group = pygame.sprite.Group()
charac_group.add(personagem)
print(personagem)
'''print(Colision(personagem,chao))'''
screen=width,height=1000,600
tela=pygame.display.set_mode(screen)
chao = pygame.image.load("chao.png").convert()
fundo = pygame.image.load("fundo.png").convert()
'''col=Colision(personagem,chao)
print(col)'''
pygame.key.set_repeat(2, 2)
rodando=True
while rodando:

	for event in pygame.event.get():
		if event.type == QUIT:
			rodando=False
	
		if event.type==KEYDOWN:
			if event.key==pygame.K_a:
				personagem.moveleft()
			elif event.key==pygame.K_d:
				personagem.moveright()
			elif event.key==pygame.K_w:
				personagem.moveup()
			elif event.key==pygame.K_s:
				personagem.movedown() 
	tela.blit(fundo,(0,0))
	object_group.draw(tela)
	charac_group.draw(tela)
	pygame.display.flip()
