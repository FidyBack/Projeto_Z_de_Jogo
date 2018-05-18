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
		self.posicao_arma = vec(0, -25)

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
			self.dir = self.rect.midleft[:]
			self.direita = False
			self.posicao_arma.x = -20
		# Direita
		elif keys[pg.K_d]:
			self.velo.x = velo_jogador
			self.dir = self.rect.midright[:]
			self.direita = True
			self.posicao_arma.x = 20
		# Parado
		else:
			self.velo.x = 0

		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi
		# Colisão com máscaras
		self.mask = pg.mask.from_surface(self.image)

		inverte(self,"img/megaman.png")


	# Pulo do personagem
	def pulo(self):
		self.pular = False
		# Colisão
		colisao = pg.sprite.spritecollide(self, self.jogo.plataforma, False)

		# Zera o pulador se tem colisão
		if colisao:
		 	self.pulador = 0

		# Pula apenas se o número de pulos for menor que 2
		if self.pulador < 46545:
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
	def __init__(self, jogo, image, dano, vida, posix, posiy, velx):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = pg.image.load(image)
		self.rect = self.image.get_rect()
		self.posi = vec(posix, posiy)
		self.vida = vida
		self.dano = dano
		self.velo = vec(velx, 0)
		self.acele = vec(0, grav_inimigo)

		# Adição nos grupos
		self.jogo.caracters.add(self)
		self.jogo.todos_sprites.add(self)
		self.jogo.inimigos.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)

	def update(self):
		self.eventos()
		if self.posi.x > - 100 and self.posi.x < largura + 100:
			self.velo += self.acele
			self.posi += self.velo + 0.5 * self.acele
		self.rect.midbottom = self.posi
		self.mask = pg.mask.from_surface(self.image)

	def eventos(self):
		pass

# Sprite do inimigo pedra
class Pedra(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo, "img/golem.png", 5, 10, posix, posiy, -6)

# Sprite básico dos tiros
class Tiro(pg.sprite.Sprite):
	def __init__(self, jogo, posicao, image, dano, velx, vely, acelex, aceley):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = posicao[:]
		self.image = pg.image.load(image)
		self.rect = self.image.get_rect()
		self.velo = vec(velx, vely)
		self.acele = vec(acelex, aceley)
		self.dano = dano

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)
		self.jogo.tiros.add(self)

	def update(self):
		self.velo += self.acele
		self.posi += self.velo + self.acele / 2
		self.rect.center = self.posi
		# Colisão com máscaras
		self.mask = pg.mask.from_surface(self.image)

# tiro reto do personagem
class Tiro_reto(Tiro):
	def __init__(self, jogo, posicao, velx):
		Tiro.__init__(self, jogo, posicao, 'img/Fireball.png', 2, velx, 0, 0, 0)
		self.jogo.tiro_personagem.add(self)

# Granada do personagem
class Tiro_parabola(Tiro):
	def __init__(self, jogo, posicao, velx):
		Tiro.__init__(self, jogo, posicao, 'img/granada.png', 5, velx, -10, 0, 0.5)
		self.jogo.tiro_personagem.add(self)

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
