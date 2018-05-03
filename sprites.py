# Sprites pro joguinho
import pygame as pg
from configuracoes import *
vec = pg.math.Vector2

class Jogador(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.image.load("img/FatYoshi.png")
		self.rect = self.image.get_rect()
		self.rect.center = (largura / 2, altura / 2)
		self.posi = vec(largura / 2, altura / 2)
		self.velo = vec(0, 0)
		self.acele = vec(0, 0)

	# Movimento do personagem
	def update(self):
		self.acele = vec(0, grav_jogador)
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.acele.x = -acele_jogador
		if keys[pg.K_d]:
			self.acele.x = acele_jogador

		# Adiciona fricção à aceleração (útil no gelo)
		self.acele.x += self.velo.x * atrito_jogador
		# Velocidade somada com a aceleração
		self.velo += self.acele
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# limite da tela
		if self.posi.x > largura:
			self.posi.x = 0
		if self.posi.x < 0 :
			self.posi.x = largura

		# Define a posição do centro
		self.rect.midbottom = self.posi

	# Pulo do personagem
	def pulo(self):
		# Pular apenas com plataforma
		self.rect.x += 1
		colisao = pg.sprite.spritecollide(self, self.game.plataforma, False)
		self.rect.x -= 1
		if colisao:
			self.velo.y = -15



class Plataforma(pg.sprite.Sprite):
	def __init__(self, x, y, l, a):
		pg.sprite.Sprite.__init__(self)
		# self.image = pg.image.load("img/chao.png")
		self.image = pg.Surface((l, a))
		self.image.fill(ama_esc)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
