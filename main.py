'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e Alexandre Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

Jogo feito em 2018

Aproveite!!!
'''

# Importações
import pygame as pg
from configuracoes import *
from sprites import *
import math
from random import randrange


class Jogo:
	# Inicia o básico do sistema
	def __init__(self):
		pg.init()
		pg.mixer.init()
		pg.display.set_caption(titulo)
		self.tela = pg.display.set_mode((largura, altura))
		self.relogio = pg.time.Clock()
		self.nome_da_fonte = pg.font.match_font(nome_fonte)
		self.rodando = True
		self.jogando = True

	# Novo Jogo
	def novo(self):

		# ================================================================================================================
		# Grupos
		# ================================================================================================================

		# Sprites em geral
		self.todos_sprites = pg.sprite.Group()
		# Inimigos
		self.inimigos = pg.sprite.Group()
		# Plataformas
		self.plataforma = pg.sprite.Group()
		# Inimigo + Plataforma + Ataque
		self.interacoes = pg.sprite.Group()
		# Inimigo + Personagem + Ataque
		self.moviveis = pg.sprite.Group()
		# Inimigo + Personagem
		self.caracters = pg.sprite.Group()
		# Tiros como grupo
		self.tiros = pg.sprite.Group()
		# Tiro do personagem
		self.tiro_personagem = pg.sprite.Group()
		# Tiro de inimigos
		self.tiro_inimigo = pg.sprite.Group()

		# ================================================================================================================
		# Adição dos sprites no jogo
		# ================================================================================================================

		# Plataformas adicionadas
		for plat in lista_plataformas['plataformas']:
			Plataforma(self, *plat)

		# Chão adicionado
		for gnd in lista_plataformas['chãos']:
			Plataforma(self, *gnd)

		# Golem adicionado
		for pedra in lista_inimigos['pedra']:
			Pedra(self, *pedra)

		for pb in lista_inimigos['pb']:
			Pb(self, *pb)

		for robo in lista_inimigos['robo']:
			Robo(self, *robo)

		for mineiro in lista_inimigos['mineiro']:
			Mineirinho(self, *pb)

		for spike in lista_inimigos['spike']:
			Spike(self, *spike)

		# Jogador adicionado
		self.jogador = Jogador(self)

		# Rodar
		self.rodar()

	# Mostra a tela de começo
	def introducao(self):

		# Tela de discurso do jogo
		self.tela.fill(preto)
		a = 27
		b = 27
		palavras = discurso.split()
		idx_palavra = 0
		palavra_atual = palavras[0]
		idx_letra = 0
		conta_tick = 0
		rode = False

		# Looping do discurso
		while True:
			self.relogio.tick(fps)

			# Fecha tudo (encerra o loop 'jogando' e 'rodando')
			for evento in pg.event.get():
				if evento.type == pg.QUIT:
					self.rodando = False
					return

			# Mata a tela de introdução
				if evento.type == pg.KEYUP:
					rode = True
			if rode:
				break

			# Condição qualquer para entrar no if
			if conta_tick % int(fps) == 0:

				# Reconhece quando uma palavra acaba
				if idx_letra >= len(palavra_atual):
					
					# dá espaço entre as palavras
					a += 27
					# Zera o contador
					idx_letra = 0
					# Adiciona no contador de palavras
					idx_palavra += 1
					
					# Garante que quando o discurso acabe quando o contador de palavras seja igual ao len do discurso
					if idx_palavra == len(palavras):
						break

					# Transfere a palavra para a próxima
					else:
						palavra_atual = palavras[idx_palavra]
						
						# Se é estiver no limite da tela, pula uma linha e volta pro começo dela
						if len(palavra_atual) * 27 + a > 1000:
							b += 27
							a = 27

				self.desenhar_texto(palavra_atual[idx_letra], 48, branco, a, b)
				self.musica('msc/tecla.wav', 1)
				pg.time.delay(100)

				# Adiciona efeito legal de pausa
				if palavra_atual[idx_letra] == '.' or palavra_atual[idx_letra] == ',':
					pg.time.delay(200)

				# Coloca espaço entre as letras de uma palavra
				a += 27
				# Percorre as letras entre a palavra atual
				idx_letra += 1
				pg.display.flip()

		# Mostra a tela de início
		self.mostrar_tela("img/game_start.png","press any key to start")

	# Tela inicial e final
	def mostrar_tela(self, imagem, texto):
		# Atributos do brilho
		i = 0
		b = 0
		brilho = 0
		image = pg.image.load(imagem)
		image_rect = image.get_rect()
		image_rect.midtop = (largura/2, altura/4)
		
		# Início do loop da piscada dos menus
		while i < 7:

			# Piscada lenta (Antes de apertar o botão)
			if i == 0:
				if brilho <= 0:
					b = 5
				elif brilho >= 255:
					b = (-5)

			# Piscada rápida (Após clicar em alguma tecla)
			elif i > 0:
				if brilho <= 0:
					b = 51
				elif brilho >= 255:
					b = (-51)
					i += 1
			self.relogio.tick(fps)

			# Fechando o jogo
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.rodando = False
					if self.jogando:
						self.jogando = False
					return

				# Apertando uma tecla para pular
				if event.type == pg.KEYDOWN and i == 0:
					i = 1
					self.musica('msc/entrada.wav', 1)

			# Jogando na tela,
			self.tela.fill(preto)
			brilho += b
			self.tela.blit(image,(image_rect))
			self.desenhar_texto(texto, 20, (brilho,brilho,brilho), largura/2, altura*7/8)
			pg.display.flip()

	# Inicia o looping
	def rodar(self):
		self.jogando = True
		while self.jogando:
			self.relogio.tick(fps)
			self.eventos()
			self.update()
			self.desenho()

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


				# Tiro
				if evento.key == pg.K_j :
					Tiro_reto(self,self.jogador.posi+self.jogador.posicao_arma[:],self.jogador.vel_tiro_reto[:],self.jogador.velo[:],self.jogador.direita)

				# Granada
				if evento.key == pg.K_i:
					Tiro_parabola(self,self.jogador.posi+self.jogador.posicao_arma[:],self.jogador.vel_tiro_parabola[:],self.jogador.velo[:],self.jogador.direita)

			# Pulo Menor
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_SPACE:
					self.jogador.pulo_parar_meio()

	#  Atualiza o looping
	def update(self):
		self.todos_sprites.update()

		# ================================================================================================================
		# Personagem e inimigo
		# ================================================================================================================

		# Colisão com a plataforma (Queda apenas)
		for personagem in self.caracters:
			if personagem.velo.y > 0:
				impacto = pg.sprite.spritecollide(personagem, self.plataforma, False)

				# Pegar apenas a plataforma de baixo, sem conflito com a de cima
				if impacto:
					menor_plataforma = impacto[0]
					for batida in impacto:
						if batida.rect.bottom > menor_plataforma.rect.bottom:
							menor_plataforma = batida

					# Colisão com a plataforma
					if personagem.posi.y < menor_plataforma.rect.centery:
						personagem.posi.y = menor_plataforma.rect.top + 1
						personagem.velo.y = 0
					
			# morte por falta de vidas do personagem e dos inimigos
			if personagem.vida <= 0:
				personagem.kill()

		# Colisão com o inimigo
		colisao_mob = pg.sprite.spritecollide(self.jogador, self.inimigos, False, pg.sprite.collide_mask)
		if colisao_mob:
			if not self.jogador.invencivel:
				self.jogador.vida -= colisao_mob[0].dano
				self.jogador.invencivel = True

		# Invencibilidade após a colisão com o inimigo
		if self.jogador.invencivel:
			self.jogador.contador_invencivel += 1

		if self.jogador.contador_invencivel == fps:
			self.jogador.invencivel = False
			self.jogador.contador_invencivel = 0

		# Morte por falta de vidas (Jogador)
		if self.jogador.vida <= 0:
			self.jogando = False

		# ================================================================================================================
		# Tiro
		# ================================================================================================================

		# Colisão tiro - inimigo
		for inimigo in self.inimigos:

			tiro_para_inimigo = pg.sprite.spritecollide(inimigo, self.tiro_personagem, False, pg.sprite.collide_mask)
			if tiro_para_inimigo:
				inimigo.vida -= tiro_para_inimigo[0].dano
				tiro_para_inimigo[0].kill()
				if not inimigo.invencivel:
					inimigo.vida-=tiro_para_inimigo[0].dano
				

		# Morte do tiro por sair da tela
		for tiro in self.tiro_personagem:
			if tiro.rect.x > largura or tiro.rect.x < 0 or tiro.rect.y > altura or tiro.rect.y < 0 - 25:
				tiro.kill()
	
		# ================================================================================================================
		# Câmera
		# ================================================================================================================
		
		# Se ele for para frente
		if self.jogador.rect.right > largura * 0.5:
			for plat in self.plataforma:
				plat.rect.x -= self.jogador.velo.x
			for personagem in self.moviveis:
				personagem.posi.x-=self.jogador.velo.x

		# Se ele for para trás
		elif self.jogador.rect.left < largura * 0.5:
			for plat in self.plataforma:
				plat.rect.x -= self.jogador.velo.x
			for personagem in self.moviveis:
				personagem.posi.x -= self.jogador.velo.x


		# Se ele for para cima
		if self.jogador.rect.y <= altura * 1 / 4:
			for plat in self.plataforma:
				plat.rect.y -= self.jogador.velo.y
			for personagem in self.moviveis:
				personagem.posi.y-=self.jogador.velo.y

		# Se ele for para baixo
		elif self.jogador.rect.y >= altura * 3 / 4:
			for plat in self.plataforma:
				plat.rect.y -= (self.jogador.velo.y + self.jogador.acele.y)
			for personagem in self.moviveis:
				personagem.posi.y -= (self.jogador.velo.y + self.jogador.acele.y)

		# ================================================================================================================
		# Queda e Fim de Jogo
		# ================================================================================================================
		
		# Game Over
		if self.jogador.rect.bottom > altura + 50:
			self.jogando = False

	# Desenho do looping
	def desenho(self):
		self.tela.fill(azul_ceu)
		self.todos_sprites.draw(self.tela)
		self.desenhar_texto('Vida = {}'.format(self.jogador.vida), 20, preto, 50, 0)
		pg.display.flip()

	# Mostra a tela de texto
	def desenhar_texto(self, texto, tamanho, cor, x, y):
		fonte = pg.font.Font(self.nome_da_fonte, tamanho)
		texto_surface = fonte.render(texto, True, cor)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x, y)
		self.tela.blit(texto_surface, texto_rect)

	# musica
	def musica(self,musica,repeticoes):
		pg.mixer.music.load(musica)
		pg.mixer.music.play(repeticoes)

# Looping
g = Jogo()
g.introducao()

while g.rodando:
	g.novo()
	if not g.jogando and g.rodando:
		g.mostrar_tela("img/game_over.png", "press any key to continue")

pg.quit()