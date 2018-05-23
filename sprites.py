'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e Alexandre Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

Jogo feito em 2018

Aproveite!!!
'''

import pygame as pg
from configuracoes import *
vec = pg.math.Vector2
import math
from random import randrange

# Classe dedicada ao spritesheet:
class Spritesheet():
	def __init__(self, arquivo):
		self.spritesheet = pygame.image.load(arquivo).convert()

	# pega uma imagem do spritesheet
	def pegar_imagem(self, x, y, largura, altura):
		image = pygame.Surface ((largura, altura))
		image.blit(self.spritesheet, (0,0), (x, y, largura, altura))
		return image

# Sprite do jogador
class Jogador(pg.sprite.Sprite):
	def __init__(self, jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.vida = 20
		self.veltiro = 0
		self.pulador = 0
		self.contador_invencivel = 0
		self.invencivel = False
		self.pular = False
		self.direita = True
		self.image = pg.image.load('img/megaman.png')
		self.rect = self.image.get_rect()
		self.posi = vec(largura * 1 / 2, altura - 130)
		self.velo = vec(0, 0)
		self.acele = vec(0, grav_jogador)
		self.vel_tiro_reto=vec(20,0)
		self.vel_tiro_parabola=vec(10,-10)
		self.posicao_arma=vec(20,-25)
		self.contador_tiro=0
		self.tiro_reto=False
		self.tiro_parabola=False



		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.caracters.add(self)
		self.jogo.moviveis.add(self)

	# Movimento do personagem com teclas pressionadas
	def update(self):
		# Esquerda
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.velo.x = -velo_jogador
			self.direita=False
			self.posicao_arma.x=-20

		elif keys[pg.K_d]:
			self.velo.x = velo_jogador
			self.direita=True
			self.posicao_arma.x=20
		else:
			self.velo.x = 0

		inverte(self,"img/megaman.png")

		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi
		# Colisão com máscaras
		self.mask = pg.mask.from_surface(self.image)

	# Pulo do personagem
	def pulo(self):
		self.pular = False
		# Colisão


		# Pula apenas se o número de pulos for menor que 2
		if self.pulador < 2:
			self.pular = True

		if self.pular:
			self.velo.y = -pulo_jogador
			self.pulador += 1
			if self.posi.y < 0 + 0:
				self.velo.y = 0

	# Pulo pequeno
	def pulo_parar_meio(self):
		if self.pular:
			if self.velo.y < -5:
				self.velo.y = -5

# Sprite das plataformas
class Plataforma(pg.sprite.Sprite):
	def __init__(self, jogo, x, y, l, a):
		pg.sprite.Sprite.__init__(self)
		self.jogo=jogo
		self.image = pg.Surface((l, a))
		self.image.fill(verd_esc)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)

# Sprite básico dos inimigos
class Inim(pg.sprite.Sprite):
	def __init__(self,jogo,image,dano,vida,posix,posiy,velo,acele):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.img=image
		self.image = pg.image.load(image)
		self.rect = self.image.get_rect()
		self.posi = vec(posix,posiy)
		self.rect.midbottom=self.posi
		self.vida=vida
		self.dano=dano
		self.direita=True
		self.velo = velo
		self.acele = acele
		self.invencivel=False

		# Adição nos grupos
		self.jogo.caracters.add(self)
		self.jogo.todos_sprites.add(self)
		self.jogo.inimigos.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)

	def update(self):
		if self.velo.x>0:
			self.direita=True
		elif self.velo.x<0:
			self.direita=False
		if self.posi.x>-100 and self.posi.x<largura+100:
			self.velo += self.acele
			self.posi += self.velo + 0.5 * self.acele
		self.rect.midbottom = self.posi
		self.mask = pg.mask.from_surface(self.image)
		self.eventos()
		inverte(self,self.img)

	def eventos(self):
		pass

# Sprite do inimigo pedra
class Pedra(Inim):
	def __init__(self, jogo, posix,posiy):
		Inim.__init__(self, jogo ,"img/pedra.png",3,5, posix,posiy,vec(-5,0),vec(0,grav_jogador))

# Sprite básico dos tiros
class Tiro(pg.sprite.Sprite):
	def __init__(self,jogo,image,dano,posicao,velo,acele,velo_personagem,direita,tempo):
		pg.sprite.Sprite.__init__(self)
		self.img=image
		self.jogo=jogo
		self.posi=vec(posicao[:])
		self.image=pg.image.load(image)
		self.rect=self.image.get_rect()
		self.velo=vec(velo)
		self.vel=self.velo.x
		self.acele=acele
		self.dano=dano
		self.direita=direita
		self.tempo=tempo
		self.velo_personagem=vec(velo_personagem)
		self.vel_personagem=self.velo_personagem.x
		self.rect.center=self.posi
		inverte(self,self.img)
		
		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)
		self.jogo.tiros.add(self)

	def update(self):
		if self.direita:
			self.velo.x=self.vel

		else:
			self.velo.x=-self.vel
		self.eventos()
		self.tempo-=1
		if self.tempo==0:
			self.kill()
		self.velo += self.acele
		self.posi += self.velo + self.acele/2 
		self.posi.x += self.velo_personagem.x
		self.rect.center = self.posi
		inverte(self,self.img)

	def eventos(self):
		pass

# tiro reto do personagem
class Tiro_reto(Tiro):

	def __init__(self,jogo,posicao,velo,velo_personagem,direita):
	 	Tiro.__init__(self,jogo,'img/Fireball.png',1,posicao,velo,vec(0,0),velo_personagem,direita,fps)
	 	self.jogo.tiro_personagem.add(self)
	 	self.jogo.tiros.add(self)


# Granada
class Tiro_parabola(Tiro):
	def __init__(self,jogo,posicao,velo,velo_personagem,direita):
		Tiro.__init__(self,jogo,'img/granada.png',5,posicao,velo,vec(0,0.5),velo_personagem,direita,fps)
		self.jogo.tiro_personagem.add(self)
		self.jogo.tiros.add(self)

class Golem(Inim):
	def __init__(self, jogo, posix,posiy):
		Inim.__init__(self, jogo ,"img/golem.png",3,5, posix,posiy,vec(-5,0),vec(0,grav_jogador))

class Robo(Inim):
	def __init__(self,jogo,posix,posiy):
		Inim.__init__(self,jogo,"img/robo.png",3,5,posix,posiy,vec(0,0),vec(0,grav_jogador))
		self.contador=0
		self.veltiro=vec(10,0)
		self.velx=0
		self.posicao_arma=vec(50,-100)
		self.tiro = 0
	def eventos(self):
		if self.direita:
			self.posicao_arma.x=50
		else:
			self.posicao_arma.x=-50
		if self.contador==120:
		 	self.velo.x=0
		 	self.tiro=Tiro(self.jogo,'img/granada.png',5,self.posi+self.posicao_arma,self.veltiro,vec(0,0),self.velo,self.direita,fps)
		 	self.jogo.tiro_inimigo.add(self.tiro)

		elif self.contador==150:
		 	self.velx=-self.velx
		 	self.direita= not self.direita
		 	self.velo.x=self.velx
		 	self.contador=0
		self.contador+=1

class Mineirinho(Inim):
	def __init__(self,jogo,posix,posiy):
		Inim.__init__(self,jogo,"img/miner.png",3,2,posix,posiy,vec(-2,0),vec(0,grav_jogador))
		self.contador=0
		self.ataque=False
		self.posicao_arma=vec(10,-10)
		self.tiro=0
	def eventos(self):
		if self.direita:
			self.posicao_arma.x=10
		else:
			self.posicao_arma.x=-10
		esta_direita=self.posi.x>self.jogo.jogador.posi.x+70
		esta_esquerda=self.posi.x<self.jogo.jogador.posi.x-70

		if (esta_direita and not self.jogo.jogador.direita) or (esta_esquerda and self.jogo.jogador.direita) or self.ataque:
			self.invencivel=False


			if esta_direita:
				self.velo.x=-2
			elif esta_esquerda:
				self.velo.x=2
			else:
				self.velo.x=0
			 	
			self.contador+=1
		else:
			self.invencivel=True
			self.contador=0
			self.velo.x=0

		if self.contador==60:
			self.ataque=True
			self.velo.x=0
			self.tiro=Tiro(self.jogo,'img/granada.png',5,self.posi+self.posicao_arma,vec(5,0),vec(0,0),self.velo,self.direita,fps)
			self.jogo.tiro_inimigo.add(self.tiro)

		if self.contador==120:
			self.ataque=False
			self.contador=0

class Pb(Inim):
	def __init__(self,jogo,posix,posiy):
		Inim.__init__(self,jogo,"img/pubg.png",0,2,posix,posiy,vec(0,0),vec(0,grav_jogador))
		self.contador = 0
		self.contato=False
		self.explode=True
		self.tiro=0
	def eventos(self):
		if abs(self.posi.x-self.jogo.jogador.posi.x)<30:
			self.velo.x=0
			if abs(self.posi.y-self.jogo.jogador.posi.y)<30:
					self.contato=True
		else:
			if self.posi.x>self.jogo.jogador.posi.x:
				self.velo.x=-5
			else:
				self.velo.x=5

		if self.contato:
			self.velo.x=0
		if self.contato:
			self.contador+=1
		if self.contador==60 and self.explode:
			self.tiro=Tiro(self.jogo,'img/explosao.png',10,self.rect.midbottom,vec(0,0),vec(0,0),self.velo,self.direita,fps)
			self.jogo.tiro_inimigo.add(self.tiro)
		if self.contador==80:
			self.kill()

# Classe de animação
class inverte(pg.sprite.Sprite):
	def __init__(self,personagem,image):

		self.caracters=personagem

		self.dir=pg.image.load(image)
		self.esq=pg.transform.flip(self.dir,True,False)

		if self.caracters.direita:
			self.caracters.image=self.dir
		else:
			self.caracters.image=self.esq

class Spike(Inim):
		def __init__(self, jogo, posix,posiy):
			Inim.__init__(self, jogo ,"img/espinho.png",50,40, posix,posiy,vec(0,0),vec(0,0))
			self.invencivel=True

class Chefe(Inim):
		def __init__(self,jogo,posix,posiy):
			Inim.__init__(self,jogo,"img/head.png",3,40,posix,posiy,vec(-2,0),vec(0,0))
			self.contador=0
			self.contador_ataque=0
			self.modo=0
			self.angulo=90
			self.mao_direita=0
			self.ataque=0
			self.n_ataque=0
			
		def eventos(self):
			if self.modo==0:
				if self.contador<=60:
					self.velo=vec(0,3)
				elif self.contador<=300:
					self.invencivel=True
					self.velo=vec(10*math.sin(self.angulo*math.pi/180),10*math.cos(self.angulo*math.pi/180))
					self.angulo+=3
				elif self.contador<=360:
					self.velo=vec(0,-3)
				elif self.contador==361:
					self.velo=vec(0,0)
					self.ataque=randrange(3)
				elif self.contador>=362:
					self.contador_ataque+=1
					
				if self.ataque==0:
					if self.contador_ataque==30:
						self.mao_direita=Inim(self.jogo,"img/right.png",0,50,largura-50,3*altura/4,vec(0,0),vec(0,0))
					elif self.contador_ataque==90 or self.contador_ataque==150 or self.contador_ataque==210:
						Tiro(self.jogo,'img/granada.png',4,self.mao_direita.rect.center,vec(-8,0),vec(0,0),self.velo,self.direita,5*fps)
					elif self.contador_ataque==270:
						self.mao_direita.kill()
						self.contador_ataque=0
					elif self.contador_ataque==300:
						self.n_ataque+=1
						self.ataque=randrange(3)

				elif self.ataque==1:

					if self.contador_ataque==30:
						Inim(self.jogo,"img/left.png",0,50,50,7*altura/8,vec(0,0),vec(0.5,0))
						self.ataque=randrange(3)


						self.n_ataque+=1
				else:
					self.ataque=randrange(3)
					self.n_ataque+=1

				if self.n_ataque==3:
					self.contador=0
					

				self.contador+=1