'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

2018

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
		p1 = Plataforma(0, altura - 40, largura, 400)
		self.plataforma.add(p1)
		self.todos_sprites.add(p1)
		p2 = Plataforma(largura / 2 - 50, altura * 3 / 4, 100, 20)
		self.plataforma.add(p2)
		self.todos_sprites.add(p2)
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
		impacto = pg.sprite.spritecollide(self.jogador, self.plataforma, False)
		if impacto:
			self.jogador.posi.y = impacto[0].rect.top +1
			self.jogador.velo.y = 0

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

	# Mostra a tela de começo
	def mostrar_tela_comeco(self):
		pass

	# Mostra a tela de adeus :(
	def mostrar_tela_adeus(self):
		pass

g = Jogo()
g.mostrar_tela_comeco()
while g.rodando:
	g.novo()
	g.mostrar_tela_adeus()

pg.quit()