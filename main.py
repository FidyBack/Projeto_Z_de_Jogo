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
from os import path
from mapa import mapa
class Jogo:
	def __init__(self):
		pg.init()
		pg.mixer.init()
		pg.display.set_caption(titulo)
		self.tela = pg.display.set_mode((largura, altura))
		self.relogio = pg.time.Clock()
		self.nome_da_fonte = pg.font.match_font(nome_fonte)
		self.rodando = True
		self.jogando = True
		self.load_data()

# ================================================================================================================
# Looping Principal
# ================================================================================================================

	def novo(self):

		# ================================================================================================================
		# Grupos
		# ================================================================================================================

		self.todos_sprites = pg.sprite.Group()
		self.inimigos = pg.sprite.Group()
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
		self.tiro_inimigo = pg.sprite.Group()
		self.powerup = pg.sprite.Group()
		self.nao_moviveis= pg.sprite.Group()

		# ================================================================================================================
		# Adição dos sprites no jogo
		# ================================================================================================================

		# Mapa
		for y in  range(len(mapa)):
			linha = mapa[y]
			for x in range(len(linha)):
				bloco = linha[x]
				if bloco.isnumeric():
					if bloco == '1':
						Plataforma(self, 48 * (x-1), 48 * (y-1))
				else:
					if bloco == 'P':
						Pedra(self, 48 * (x-1), 48 * (y-1))
					elif bloco == 'B':
						Pb(self, 48 * (x-1), 48 * (y-1))
					elif bloco == 'R':
						Robo(self, 48*(x-1), 48*(y-1))
					elif bloco == 'M':
						Mineirinho(self, 48*(x-1), 48*(y-1))
					elif bloco == 'B':
						Pb(self, 48*(x-1), 48*(y-1))
					# elif bloco == 'C':
					# 	Chefe(self, 48*(x-1), 48*(y-1))
		
		# Jogador adicionado
		self.jogador = Jogador(self)

		# Boss adicionado
		# self.boss = Chefe(self, )

		# Rodar
		self.rodar()

	def rodar(self):
		self.jogando = True
		while self.jogando:
			self.relogio.tick(fps)
			self.eventos()
			self.update()
			self.desenho()

	def eventos(self):
		self.jogador.contador_tiro += 1
		
		# Fecha o jogo
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
					self.jogador.tiro_reto = True

				# Granada
				if evento.key == pg.K_i:
					self.jogador.tiro_parabola = True

			# Pulo Menor
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_SPACE:
					self.jogador.pulo_parar_meio()


		if self.jogador.tiro_reto and self.jogador.contador_tiro >= 6:
			Tiro_reto(self, self.jogador.posi + self.jogador.posicao_arma[:], self.jogador.vel_tiro_reto[:], self.jogador.velo[:], self.jogador.olhar_direita)
			self.jogador.contador_tiro = 0
			self.jogador.tiro_reto = False

		if self.jogador.tiro_parabola and self.jogador.contador_tiro >= 6:
			Tiro_parabola(self, self.jogador.posi + self.jogador.posicao_arma[:], self.jogador.vel_tiro_parabola[:], self.jogador.velo[:], self.jogador.olhar_direita)
			self.jogador.contador_tiro = 0
			self.jogador.tiro_parabola = False

	def update(self):
		self.todos_sprites.update()
		# ================================================================================================================
		# Personagem e inimigo
		# ================================================================================================================

		for personagem in self.caracters:
			impacto = pg.sprite.spritecollide(personagem, self.plataforma, False)
			if impacto:

				for plataforma in impacto:
					intersect=personagem.rect.clip(plataforma.rect)
					
					if personagem.rect.left < plataforma.rect.right  and personagem.rect.right > plataforma.rect.left and abs(intersect.width)>=abs(intersect.height)   :
						if personagem.velo.y > 0 and personagem.rect.bottom==intersect.bottom:
							personagem.rect.bottom = plataforma.rect.top
							personagem.posi = vec(personagem.rect.midbottom)
							personagem.velo.y = 0
							if personagem == self.jogador:
								self.jogador.pulando=False
							
						elif personagem.velo.y < 0 and personagem.rect.top==intersect.top:
							personagem.rect.top = plataforma.rect.bottom
							personagem.posi = vec(personagem.rect.midbottom)
							personagem.velo.y = 0
							
					if personagem.rect.top < plataforma.rect.bottom  and personagem.rect.bottom>plataforma.rect.top and abs(intersect.height)>abs(intersect.width):
						if personagem.velo.x>0 and personagem.rect.right==intersect.right:
							personagem.rect.right = plataforma.rect.left
							personagem.posi=vec(personagem.rect.midbottom)
							personagem.velo.x=0
							if personagem==self.jogador:
								personagem.andando=False
					
						elif personagem.velo.x < 0 and personagem.rect.left==intersect.left:
							personagem.rect.left = plataforma.rect.right
							personagem.posi = vec(personagem.rect.midbottom)
							personagem.velo.x = 0
							if personagem==self.jogador:
								personagem.andando=False


			# morte por falta de vidas do personagem e dos inimigos
			if personagem.vida <= 0:

				#alteration
				if personagem in self.inimigos:
					Powerup(self,personagem.posi)
				personagem.kill()

		# Colisão com o inimigo
		colisao_mob = pg.sprite.spritecollide(self.jogador, self.inimigos, False)
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
			tiro_para_inimigo = pg.sprite.spritecollide(inimigo, self.tiro_personagem, False)
			if tiro_para_inimigo:
				inimigo.vida -= tiro_para_inimigo[0].dano
				tiro_para_inimigo[0].kill()
				if not inimigo.invencivel:
					inimigo.vida-=tiro_para_inimigo[0].dano
				
		# Morte do tiro por sair da tela
		for tiro in self.tiro_personagem:
			if tiro.rect.x > largura or tiro.rect.x < 0 or tiro.rect.y > altura or tiro.rect.y < 0 - 25:
				tiro.kill()

		colisao_tiro = pg.sprite.spritecollide(self.jogador, self.tiro_inimigo, False)
		if colisao_tiro:
			if not self.jogador.invencivel:
				self.jogador.vida -= colisao_tiro[0].dano
				self.jogador.invencivel = True
		#alteration
		colisao_powerup = pg.sprite.spritecollide(self.jogador, self.powerup, False)
		if colisao_powerup:
			for powerup in colisao_powerup:
				self.jogador.vida+=powerup.vida
				powerup.kill()
				if self.jogador.vida>self.jogador.limite_vida:
					self.jogador.vida=self.jogador.limite_vida

		# for powerup in self.powerup:
		# 	colisao_powerup_plataforma=pg.sprite.spritecollide(powerup, self.plataforma, False)
		# 	if colisao_powerup_plataforma:
		# 		powerup.velo.y = 0
		# 		powerup.rect.bottom = colisao_powerup_plataforma[0].rect.top


		# ================================================================================================================
		# Câmera
		# ================================================================================================================
		
		# Se ele for para frente
		if self.jogador.rect.centerx > largura * 0.5:
			for nao_movivel in self.nao_moviveis:
				nao_movivel.rect.x -= self.jogador.velo.x
			for personagem in self.moviveis:
				personagem.posi.x-=self.jogador.velo.x

		# Se ele for para trás
		elif self.jogador.rect.centerx < largura * 0.5:
			for nao_movivel in self.nao_moviveis:
				nao_movivel.rect.x -= self.jogador.velo.x
			for personagem in self.moviveis:
				personagem.posi.x -= self.jogador.velo.x

		# Se ele for para cima
		if self.jogador.rect.centery <= altura * 1 / 4:
			for nao_movivel in self.nao_moviveis:
				nao_movivel.rect.y -= (self.jogador.velo.y + self.jogador.acele.y/2)
			for personagem in self.moviveis:
				personagem.posi.y-=(self.jogador.velo.y + self.jogador.acele.y/2)

		# Se ele for para baixo
		elif self.jogador.rect.centery >= altura * 3 / 4:
			for nao_movivel in self.nao_moviveis:
				nao_movivel.rect.y -= (self.jogador.velo.y + self.jogador.acele.y/2)
			for personagem in self.moviveis:
				personagem.posi.y -= (self.jogador.velo.y + self.jogador.acele.y/2)

		# ================================================================================================================
		# Queda e Fim de Jogo
		# ================================================================================================================
		
		# Game Over
		if self.jogador.rect.bottom > altura + 50:
			self.jogando = False

# ================================================================================================================
# Funções de tela
# ================================================================================================================	

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
						if len(palavra_atual) * 27 + a > largura:
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
		self.mostrar_tela_inicio("img/game_start.png","press any key to start")

	# Tela inicial
	def mostrar_tela_inicio(self, imagem, texto):
		# Atributos do brilho
		i = 0
		b = 0
		brilho = 0
		image = pg.image.load(imagem)
		image_rect = image.get_rect()
		image_rect.midtop = (largura / 2, altura / 4)
		
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
			self.desenhar_texto('Jump : Space  Shoot : j  grenade : i  Move: a/d', 20, branco, largura/2, altura*3/4)
			pg.display.flip()

	# Tela de Game Over
	def mostrar_tela_final(self, imagem, texto):
		# Atributos do brilho
		i = 0
		b = 0
		brilho = 0
		image = pg.image.load(imagem)
		image_rect = image.get_rect()
		image_rect.midtop = (largura / 2, altura / 4)
		
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
			self.desenhar_texto(texto, 20, (brilho,brilho,brilho), largura/2, altura * 7/8)
			self.desenhar_texto('Tente Novamente', 20, branco, largura/2, altura * 3/4)
			pg.display.flip()

# ================================================================================================================
# Funções Suporte
# ================================================================================================================

	# Procura por aquivos
	def load_data(self):
		self.direct = path.dirname(__file__)
		img_dir = path.join(self.direct, "img")

		# Pegar imagem do spritesheet
		self.spritesheet_inimigos = Spritesheet(path.join(img_dir, spritesheet_inimigos))
		self.spritesheet_personagem = Spritesheet(path.join(img_dir, spritesheet_personagem))
		self.spritesheet_plataformas = Spritesheet(path.join(img_dir, spritesheet_plataformas))

	# Desenho do looping
	def desenho(self):
		self.tela.blit(background, (0, 0))
		self.todos_sprites.draw(self.tela)
		self.desenhar_texto('Vida = {}'.format(self.jogador.vida), 20, branco, 50, 0)
		pg.display.flip()

	# Música
	def musica(self,musica,repeticoes):
		pg.mixer.music.load(musica)
		pg.mixer.music.play(repeticoes)

	# Mostra a tela de texto
	def desenhar_texto(self, texto, tamanho, cor, x, y):
		fonte = pg.font.Font(self.nome_da_fonte, tamanho)
		texto_surface = fonte.render(texto, True, cor)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x, y)
		self.tela.blit(texto_surface, texto_rect)

# ================================================================================================================
# Looping em sí
# ================================================================================================================

g = Jogo()
g.introducao()

while g.rodando:
	g.novo()
	if not g.jogando and g.rodando:
		g.mostrar_tela_final("img/game_over.png", "press any key to continue")

pg.quit()