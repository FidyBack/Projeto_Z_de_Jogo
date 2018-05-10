'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

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
		self.nome_da_fonte = pg.font.match_font(nome_fonte)
		self.pulador = 0

	# Novo Jogo
	def novo(self):
		# Sprites
		self.todos_sprites = pg.sprite.Group()
		# Plataformas adicionadas
		self.plataforma = pg.sprite.Group()
		for plat in lista_plataformas:
			p = Plataforma(*plat)
			self.todos_sprites.add(p)
			self.plataforma.add(p)
		# Jogador adicionado
		self.jogador = Jogador(self)
		self.todos_sprites.add(self.jogador)
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
		# Colisão com o plataforma (Queda apenas)
		if self.jogador.velo.y > 0:
			impacto = pg.sprite.spritecollide(self.jogador, self.plataforma, False)
			if impacto:
				# Pegar apenas a plataforma de baixo, sem conflito com a de cima
				menor_plataforma = impacto[0]
				for batida in impacto:
					if batida.rect.bottom > menor_plataforma.rect.bottom:
						menor_plataforma = batida
				if self.jogador.posi.y < menor_plataforma.rect.centery:
					self.jogador.posi.y = menor_plataforma.rect.top + 1
					self.jogador.velo.y = 0
					self.jogador.pular = False

		# Se ele for para frente
		if self.jogador.rect.right >= largura * 3 / 4:
			self.jogador.posi.x -= abs(self.jogador.velo.x)
			for plat in self.plataforma:
				plat.rect.x -= abs(self.jogador.velo.x)

		# Se ele for para trás
		if self.jogador.rect.left <= largura * 1 / 4:
			self.jogador.posi.x += abs(self.jogador.velo.x)
			for plat in self.plataforma:
				plat.rect.x += abs(self.jogador.velo.x)

		# Se ele for para baixo (sim, isso existe)
		if self.jogador.rect.bottom >= altura and  self.jogador.rect.bottom < altura + 500:
			self.jogador.posi.y -= abs(self.jogador.velo.y)
			for plat in self.plataforma:
				plat.rect.y -= abs(self.jogador.velo.y)

		# Game Over
		if self.jogador.rect.bottom > altura + 100:
			self.jogando = False

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
					if self.pulador < 2:
						self.jogador.pulo()
						self.pulador += 1
						self.jogador.velo.y = -pulo_jogador
			# Pulo Menor
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_SPACE:
					self.jogador.pulo_parar_meio()

	# Desenho do looping
	def desenho(self):
		self.todos_sprites.draw(self.tela)
		pg.display.flip()
		self.tela.fill(preto)
		# self.tela.blit(background, (0, 0))

	# Mostra a tela de começo40
	def mostrar_tela_comeco(self):
		# game splash/start screen
		self.tela.fill(preto)
		a = 27
		b = 27
		palavras = discurso.split()
		idx_palavra = 0
		palavra_atual = palavras[0]
		idx_letra = 0

		conta_tick = 0
		while True:
			self.relogio.tick(fps/6)

			# Fecha tudo (encerra o loop 'jogando' e 'rodando')
			for evento in pg.event.get():
				if evento.type == pg.QUIT:
					self.rodando = False
					return
			
			if conta_tick % int(fps/16) == 0:
				if idx_letra >= len(palavra_atual):
					a+=27
					idx_letra = 0
					idx_palavra += 1
					if idx_palavra == len(palavras):
						break
					else:
						palavra_atual = palavras[idx_palavra]
						if len(palavra_atual) * 27 + a > 973:
							b += 27
							a = 27

				self.desenhar_texto(palavra_atual[idx_letra], 48, branco, a, b)
				a += 27
				idx_letra += 1
				pg.display.flip()

		self.introducao()
		self.aperte_uma_tecla()

	def aperte_uma_tecla(self):
		espera = True
		while espera:
			self.relogio.tick(fps)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					espera = False
					self.rodando = False
				if event.type == pg.KEYUP:
					espera = False
			
	def introducao(self):
		self.tela.fill(preto)
		pg.time.delay(100)
		image = pg.image.load('img/game_start.png')
		image_rect = image.get_rect()
		image_rect.midtop = (largura/2, altura/4)
		self.tela.blit(image,(image_rect))
		self.desenhar_texto("press any key to start", 20, branco, largura/2, altura * 7/8)
		pg.display.flip()

	# Mostra a tela de perda :(
	def mostrar_game_over(self):
		self.tela.fill(preto)
		pg.time.delay(100)
		image = pg.image.load('img/game_over.png')
		image_rect = image.get_rect()
		image_rect.midtop = (largura/2, altura/4)
		self.tela.blit(image, (image_rect))
		self.desenhar_texto("Press any key to continue", 20, branco, largura/2, altura * 7/8)
		pg.display.flip()
		self.aperte_uma_tecla()

	# Mostra a tela de texto
	def desenhar_texto(self,texto,tamanho,cor,x,y):
		fonte = pg.font.Font(self.nome_da_fonte,tamanho)
		texto_surface = fonte.render(texto,True, cor)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x,y)
		self.tela.blit(texto_surface, texto_rect)

g = Jogo()
g.mostrar_tela_comeco()
while g.rodando:
	g.novo()
	g.mostrar_game_over()

pg.quit()