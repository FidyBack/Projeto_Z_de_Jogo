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

# Sprite do jogador
class Jogador(pg.sprite.Sprite):
	def __init__(self, jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.vida = 20
		self.pular = False
		self.image = pg.image.load("img/FatYoshi.png")
		self.rect = self.image.get_rect()
		self.posi = vec(largura * 1 / 2, altura - 50)
		self.velo = vec(0, 0)
		self.acele = vec(0, grav_jogador)
		self.pulador = 0
		self.invencivel=False
		self.contador_invencivel=0
		self.dir='parado'

	# Movimento do personagem com teclas pressionadas
	def update(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.velo.x = -velo_jogador
			self.dir = 'esquerda'
		elif keys[pg.K_d]:
			self.velo.x = velo_jogador
			self.dir = 'direita'
		elif keys[pg.K_w]:
			self.dir = 'cima'
		elif keys[pg.K_s]:
			self.dir='baixo'
		else:
			self.velo.x = 0

		print(self.dir)

		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Posição de acordo com a velocidade
		self.posi += self.velo
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi


	# Pulo do personagem
	def pulo(self):
		self.pular = False
		# Pular apenas com plataforma
		self.rect.y += 1
		colisao = pg.sprite.spritecollide(self, self.jogo.plataforma, False)
		self.rect.y -= 1

		# Zera o pulador se tem colisão
		if colisao:
		 	self.pular = True
		 	self.pulador = 0

		# Pula apenas se o número de pulos for menor que 2
		if self.pulador < 2:
			self.pular = True

		if self.pular:
			self.velo.y = -pulo_jogador
			self.pulador += 1


		# Colisão com máscaras
		self.mask = pg.mask.from_surface(self.image)


	def pulo_parar_meio(self):
		if self.pular:
			if self.velo.y < -5:
				self.velo.y = -5

class Plataforma(pg.sprite.Sprite):
	def __init__(self, jogo, x, y, l,a):
		pg.sprite.Sprite.__init__(self)
		# self.image = pg.image.load("img/chao.png")
		self.jogo=jogo
		self.image = pg.Surface((l, a))
		self.image.fill(ama_esc)
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)

class Inimigo(pg.sprite.Sprite):
	def __init__(self, jogo, posix, posiy):
		
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.vida = 5
		self.dano = 3
		self.image = pg.image.load("img/golem.png")
		self.rect = self.image.get_rect()
		self.posi = vec(posix, posiy)
		self.velo = vec(-5, 0)
		self.acele = vec(0, grav_jogador)
		self.jogo.todos_sprites.add(self)
		self.jogo.inimigos.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)


	def update(self):
		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro
		self.rect.midbottom = self.posi

		# Colisão com máscara
		#self.mask = pg.mask.from_surface(self.image)

class Tiro_reto(pg.sprite.Sprite):

	def __init__(self,jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = self.jogo.jogador.posi[:] + vec(10, -30)
		self.image = pg.image.load('img/Fireball.png')
		self.rect = self.image.get_rect()
		self.velo = vec(10, 0)
		self.dano=2
		self.jogo.todos_sprites.add(self)
		self.jogo.tiros.add(self)
		
	def update(self):
		self.posi += self.velo
		self.rect.center = self.posi

class Tiro_parabola(pg.sprite.Sprite):
	def __init__(self,jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = self.jogo.jogador.posi[:] + vec(10, -30)
		self.image = pg.image.load('img/granada.png')
		self.dano=1
		self.rect = self.image.get_rect()
		self.velo = vec(10, -10)
		self.acele = vec(0, grav_jogador)
		self.jogo.todos_sprites.add(self)
		self.jogo.tiros.add(self)

	def update(self):
		self.velo.y += self.acele.y
		self.posi += self.velo + self.acele//2
		self.rect.center = self.posi