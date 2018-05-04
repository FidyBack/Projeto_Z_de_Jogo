'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq

Jogo feito em 2018

Aproveite!!!
'''

# Importações
import pygame as pg
import random
from configuracoes import *
from sprites import *

class Jogo:
	# Inicia o básico do sistema
	def __init__(self):
		pg.init()
		pg.mixer.init()
		pg.display.set_caption(titulo)
		self.tela = pg.display.set_mode((largura, altura))
		self.relogio = pg.time.Clock()
		self.rodando = True

	# Novo Jogo
	def novo(self):
		# Sprites
		self.todos_sprites = pg.sprite.Group()
		# Jogador adicionado
		self.jogador = Jogador(self)
		self.todos_sprites.add(self.jogador)
		# Plataformas adicionadas
		self.plataforma = pg.sprite.Group()
		for plat in lista_plataformas:
			p = Plataforma(*plat)
			self.todos_sprites.add(p)
			self.plataforma.add(p)
		# Rodar
		self.rodar()

	# Inicia o looping
	def rodar(self):
		self.jogando = True
		while self.jogando:
			self.relogio.tick(fps)
			self.eventos()
			self.update()
			self.desenho()

	#  Atualiza o looping
	def update(self):
		self.todos_sprites.update()
		# Colisão com o plataforma (QUeda apenas)
		if self.jogador.velo.y > 0:
			impacto = pg.sprite.spritecollide(self.jogador, self.plataforma, False)
			if impacto:
				self.jogador.posi.y = impacto[0].rect.top + 1
				self.jogador.velo.y = 0

		# Se ele ele for para frente
		if self.jogador.rect.right >= largura * 3 / 4:
			self.jogador.posi.x -= abs(self.jogador.velo.x)
			for plat in self.plataforma:
				plat.rect.x -= abs(self.jogador.velo.x)-1
		print(self.jogador.velo.x)


		# Se ele for para trás
		if self.jogador.rect.right <= largura * 1 / 4:
			self.jogador.posi.x -= self.jogador.velo.x
			for plat in self.plataforma:
				plat.rect.x -= self.jogador.velo.x

	# Eventos do looping
	def eventos(self):
		# Fecha tudo (encerra o loop 'jogando' e 'rodando')
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				if self.jogando:
					self.jogando = False
				self.rodando = False
			# Pulo
			if evento.type == pg.KEYDOWN:
				if evento.key == pg.K_SPACE:
					self.jogador.pulo()

	# Desenho do looping
	def desenho(self):
		self.tela.fill(preto)
		# self.tela.blit(fundo,(0,0))
		self.todos_sprites.draw(self.tela)
		pg.display.flip()

	def aperte_uma_tecla(self):
		espera=True
		while espera:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type==pg.QUIT:
					espera = False
				if event.type == pg.KEYUP:
					espera=False


	# Mostra a tela de começo
	def mostrar_tela_comeco(self):
		pass
		

	# Mostra a tela de adeus :(
	def mostrar_tela_adeus(self):
		pass
	def desenhar_texto(self,texto,tamanho,cor,x,y):
		pass

g = Jogo()
g.mostrar_tela_comeco()
while g.rodando:
	g.novo()
	g.mostrar_tela_adeus()

pg.quit()