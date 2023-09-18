'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e Alexandre Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
Fontes feitas por Brian Kent (Ænigma) 
Imagens:
	https://opengameart.org/content/rock-0
	https://www.reddit.com/r/PixelArt/comments/5nsr4e/newbieccmario_bobomb_walk_cycle/
	https://thehunterdrake.deviantart.com/art/Overwatch-Bastion-Sprite-Sheet-619616537
	http://www.sprites-inc.co.uk/sprite.php?local=Classic/MM3/Enemy/
	http://www.angelfire.com/mn2/ryuujin/sprites/megamanx.gif
	https://br.pinterest.com/pin/131237776614571895/?lp=true
	https://www.pixilart.com/art/pixel-heart-icon-1e12b04d25f94d7

Jogo feito em 2018

Aproveite!!!
'''

import pygame as pg
from .configuracoes import *
import math
from random import randrange

vec = pg.math.Vector2

# ================================================================================================================
# Animção
# ================================================================================================================

class Spritesheet():
	def __init__(self, arquivo):
		self.spritesheet = pg.image.load(arquivo).convert()

	# Pega uma imagem do spritesheet
	def get_image(self, x, y, largura, altura, lar_dim, alt_dim):
		image = pg.Surface ((largura, altura))
		image.blit(self.spritesheet, (0, 0), (x, y, largura, altura))
		image = pg.transform.scale(image, (largura * lar_dim, altura * alt_dim))
		return image

# ================================================================================================================
# Objetos
# ================================================================================================================

class Jogador(pg.sprite.Sprite):
	def __init__(self, jogo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.vida = 20
		self.contador_invencivel = 0
		self.invencivel = False
		self.olhar_direita = True
		self.andando = False
		self.pulando = False
		self.atirando = False
		self.temporizador = 0
		self.limite_vida = 20
		self.numero_granada = 10
		self.arrastando = False
		self.machucado = False

		# Animação
		self.ultimo_update = 0
		self.frame_atual = 0
		self.carregar_imagens()
		self.image = self.frames_parados_r[0]
		self.rect = self.image.get_rect()

		# Posição
		self.posi = vec(largura * 1 / 2, altura/2)
		self.velo = vec(0, 0)
		self.acele = vec(0, grav_jogador)

		# Tiro
		self.contador_tiro = 0
		self.tiro_reto = False
		self.tiro_parabola = False
		self.vel_tiro_reto = vec(20,0)
		self.vel_tiro_parabola = vec(10,-10)
		self.posicao_arma = vec(45,-38)

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.caracters.add(self)
		self.jogo.moviveis.add(self)
		self.jogo.caintes.add(self)

	# Imagens da animação
	def carregar_imagens(self):
		# Parado
		self.frames_parados_r = [	self.jogo.spritesheet_personagem.get_image(138, 116, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(138, 80, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(106, 241, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(138, 80, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(138, 116, 30, 34, 2, 2),
									]

		self.frames_parados_l = []
		for frame_parado in self.frames_parados_r:
			frame_parado.set_colorkey(preto)
			self.frames_parados_l.append(pg.transform.flip(frame_parado, True, False))

		# Andando
		self.frames_andando_r = [	self.jogo.spritesheet_personagem.get_image(257, 0, 20, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(232, 0, 23, 35, 2, 2),
									self.jogo.spritesheet_personagem.get_image(73, 0, 32, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(36, 211, 34, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(201, 258, 26, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(257, 204, 22, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(230, 204, 25, 35, 2, 2),
									self.jogo.spritesheet_personagem.get_image(107, 0, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(36, 246, 34, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(139, 36, 29, 33, 2, 2),
									]

		self.frames_andando_l = []
		for frame_andando in self.frames_andando_r:
			frame_andando.set_colorkey(preto)
			self.frames_andando_l.append(pg.transform.flip(frame_andando, True, False))

		# Pulando
		self.frames_pulando_r = [	self.jogo.spritesheet_personagem.get_image(231, 72, 24, 37, 2, 2),
									self.jogo.spritesheet_personagem.get_image(257, 84, 15, 41, 2, 2),
									self.jogo.spritesheet_personagem.get_image(257, 36, 19, 46, 2, 2),
									self.jogo.spritesheet_personagem.get_image(256, 241, 23, 41, 2, 2),
									self.jogo.spritesheet_personagem.get_image(201, 166, 27, 42, 2, 2),
									self.jogo.spritesheet_personagem.get_image(231, 111, 24, 38, 2, 2),
									self.jogo.spritesheet_personagem.get_image(37, 176, 30, 32, 2, 2),
									]

		self.frames_pulando_l = []
		for frame_pulando in self.frames_pulando_r:
			frame_pulando.set_colorkey(preto)
			self.frames_pulando_l.append(pg.transform.flip(frame_pulando, True, False))

		# Atirando
		self.frames_atirando_r = [	self.jogo.spritesheet_personagem.get_image(138, 152, 30, 34, 2, 2),
									]

		self.frames_atirando_l = []
		for frame_atirando in self.frames_atirando_r:
			frame_atirando.set_colorkey(preto)
			self.frames_atirando_l.append(pg.transform.flip(frame_atirando, True, False))

	# Movimento
	def update(self):
		self.animacao()

		# Esquerda
		keys = pg.key.get_pressed()
		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.velo.x = -velo_jogador
			self.andando = True
			self.olhar_direita = False
			self.atirando = False
			self.posicao_arma.x = -30

		# Direita
		elif keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.velo.x = velo_jogador
			self.andando = True
			self.olhar_direita = True
			self.atirando = False
			self.posicao_arma.x = 30
		else:
			self.velo.x = 0
			self.andando = False

		# Velocidade somada com a aceleração
		self.velo += self.acele
		if abs(self.velo.x) < 0.1:
			self.velo.x = 0
		if self.velo.y > 15:
			self.velo.y = 15

		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi
		# Máscara
		self.mask = pg.mask.from_surface(self.image)

	# Animação
	def animacao(self):
		agora = pg.time.get_ticks()
		if self.machucado:
			pass

		# Atirando
		elif not self.pulando and not self.andando and self.atirando:
			if agora - self.ultimo_update > 150:
				self.ultimo_update = agora
				self.frame_atual = (self.frame_atual + 1) % len(self.frames_atirando_r)
				bottom = self.rect.bottom
				if self.olhar_direita:
					self.image = self.frames_atirando_r[self.frame_atual]
				else:
					self.image = self.frames_atirando_l[self.frame_atual]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		# Pulando
		elif self.pulando and not self.atirando:
			if agora - self.ultimo_update > 40:
				self.ultimo_update = agora
				if self.frame_atual < 4:
					self.frame_atual = (self.frame_atual + 1) % len(self.frames_pulando_l)
				else:
					self.frame_atual=4
				bottom = self.rect.bottom
				if self.olhar_direita:
					self.image = self.frames_pulando_r[self.frame_atual]
				else:
					self.image = self.frames_pulando_l[self.frame_atual]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		# Animação andando
		elif self.andando and not self.atirando:
			if agora - self.ultimo_update > 37:
				self.ultimo_update = agora
				self.frame_atual = (self.frame_atual + 1) % len(self.frames_andando_l)
				bottom = self.rect.bottom
				if self.olhar_direita:
					self.image = self.frames_andando_r[self.frame_atual]
				else:
					self.image = self.frames_andando_l[self.frame_atual]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		# Animação parado
		elif not self.pulando and not self.andando and not self.atirando:
			if agora - self.ultimo_update > 150:
				self.ultimo_update = agora
				self.frame_atual = (self.frame_atual + 1) % len(self.frames_parados_r)
				bottom = self.rect.bottom
				if self.olhar_direita:
					self.image = self.frames_parados_r[self.frame_atual]
				else:
					self.image = self.frames_parados_l[self.frame_atual]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

	# Pulo
	def pulo(self):
		self.rect.y += 1
		colisao = pg.sprite.spritecollide(self, self.jogo.plataforma, False)
		self.rect.y -= 1
		if colisao:
			self.velo.y = -pulo_jogador
			self.andando = False
			self.pulando = True
			self.frame_atual = 0

	# Pulo pequeno
	def pulo_parar_meio(self):
		if self.pulando:
			if self.velo.y < -5:
				self.velo.y = -5

class Plataforma(pg.sprite.Sprite):
	def __init__(self, jogo, x, y):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_plataformas.get_image(274, 66, 48, 48, 1, 1)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.nao_moviveis.add(self)

class Chao1(Plataforma):
	def __init__(self, jogo, x, y):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_plataformas.get_image(370, 166, 48, 16, 1, 3)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.nao_moviveis.add(self)

class Chao2(Plataforma):
	def __init__(self, jogo, x, y):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = pg.Surface((48, 48))
		self.image.fill(cinza)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.nao_moviveis.add(self)

# ================================================================================================================
# Tiro
# ================================================================================================================

class Tiro(pg.sprite.Sprite):
	def __init__(self, jogo, x, y, largura, altura, lar_dim, alt_dim, dano, posicao, velo, acele, velo_personagem, direita, tempo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = vec(posicao[:])
		self.image = self.jogo.spritesheet_tiros.get_image(x, y, largura, altura, lar_dim, alt_dim)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.velo = vec(velo)
		self.vel = self.velo.x
		self.acele = acele
		self.dano = dano
		self.olhar_direita = direita
		self.tempo = tempo
		self.velo_personagem = vec(velo_personagem)
		self.vel_personagem = self.velo_personagem.x
		self.rect.center = self.posi
		
		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)
		self.jogo.tiros.add(self)

		Inverte(self, self.image)

	def update(self):
		self.posi = vec(self.rect.center)
		if self.olhar_direita:
			self.velo.x = self.vel
		else:
			self.velo.x = -self.vel
		self.eventos()
		self.tempo -= 1
		if self.tempo == 0:
			self.kill()
		self.velo += self.acele
		self.posi += self.velo + self.acele/2 
		self.posi.x += self.velo_personagem.x
		self.rect.center = self.posi
		# Colisão com máscara
		self.mask = pg.mask.from_surface(self.image)

	def eventos(self):
		pass

class Tiro_reto(Tiro):
	def __init__(self, jogo, posicao, velo, velo_personagem, direita):
	 	Tiro.__init__(self, jogo, 44, 57, 36, 18, 2, 2, 1, posicao, velo, vec(0, 0), velo_personagem, direita, fps)
	 	self.jogo.tiro_personagem.add(self)

class Tiro_parabola(Tiro):
	def __init__(self, jogo, posicao, velo, velo_personagem, direita):
		Tiro.__init__(self, jogo, 48, 48, 8, 6, 3, 3, 5, posicao, velo, vec(0, 0.5), velo_personagem, direita,fps)
		self.jogo.tiro_personagem.add(self)

# ================================================================================================================
# Inimigos
# ================================================================================================================

class Inim(pg.sprite.Sprite):
	def __init__(self, jogo, x, y, largura, altura, lar_dim, alt_dim, dano, vida, posix, posiy, velo, acele):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_inimigos.get_image(x, y, largura, altura, lar_dim, alt_dim)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.posi = vec(posix, posiy)
		self.rect.midbottom = self.posi
		self.vida = vida
		self.dano = dano
		self.olhar_direita = True
		self.velo = velo
		self.acele = acele
		self.invencivel = False

		# Adição nos grupos
		self.jogo.caracters.add(self)
		self.jogo.todos_sprites.add(self)
		self.jogo.inimigos.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)
		self.jogo.caintes.add(self)



	def update(self):

		self.posi=vec(self.rect.midbottom)
		if self.velo.x > 0:
			self.olhar_direita = False
		elif self.velo.x < 0:
			self.olhar_direita = True
		if self.posi.x >- 100 and self.posi.x < largura + 100:
			self.velo += self.acele
			self.posi += self.velo + 0.5 * self.acele
		self.rect.midbottom = self.posi
		
		# Colisão com máscara
		self.mask = pg.mask.from_surface(self.image) 
		self.eventos()

	def eventos(self):
		pass

class Pedra(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo , 47, 330, 30, 30, 4, 4, 3, 5, posix, posiy, vec(-3,0), vec(0, grav_jogador))

class Robo(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo, 0, 330, 45, 27, 2, 2, 3, 5, posix, posiy, vec(0, 0), vec(0, grav_jogador))
		self.contador = 0
		self.veltiro = vec(10, 0)
		self.velx = 5
		self.posicao_arma = vec(50, -40)
		self.tiro = 0

	def eventos(self):

		if self.olhar_direita:
			self.posicao_arma.x = 50
		else:
			self.posicao_arma.x = -50
		if self.contador == 120:
		 	self.velo.x = self.velx
		 	self.tiro = Tiro(self.jogo, 82, 124, 23, 16, 2, 2, 5, self.posi + self.posicao_arma, self.veltiro, vec(0, 0), self.velo, self.olhar_direita, fps)
		 	self.jogo.tiro_inimigo.add(self.tiro)

		elif self.contador == 150:
		 	self.velx =- self.velx
		 	self.olhar_direita = not self.olhar_direita
		 	self.velo.x = self.velx
		 	self.contador = 0
		self.contador += 1

class Voador(Inim):
	def __init__(self,jogo,posix,posiy):
		Inim.__init__(self, jogo , 193, 128, 29, 43, 2, 2, 3, 5, posix, posiy, vec(0,0), vec(0, 0))
		self.total_velo=4

	def eventos(self):
		total=(abs(self.rect.centerx-self.jogo.jogador.rect.centerx)**2+abs(self.rect.centery-self.jogo.jogador.rect.centery)**2)**0.5
		if total==0:
			total=1
		horizontal=(self.jogo.jogador.rect.centerx-self.rect.centerx)/total
		vertical=(self.jogo.jogador.rect.centery-self.rect.centery)/total

		self.velo=self.total_velo*vec(horizontal,vertical)

class Mineirinho(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo, 79, 336, 19, 20, 2, 2, 3, 2, posix, posiy, vec(-2, 0), vec(0, grav_jogador))
		self.contador = 0
		self.ataque = False
		self.posicao_arma = vec(10,-10)
		self.tiro = 0
	def eventos(self):
		if self.olhar_direita:
			self.posicao_arma.x = 10
		else:
			self.posicao_arma.x = -10
		esta_direita = self.posi.x > self.jogo.jogador.posi.x + 70
		esta_esquerda = self.posi.x < self.jogo.jogador.posi.x - 70

		if (esta_direita and not self.jogo.jogador.olhar_direita) or (esta_esquerda and self.jogo.jogador.olhar_direita) or self.ataque:
			self.invencivel = False
			if esta_direita:
				self.velo.x = -2
			elif esta_esquerda:
				self.velo.x = 2
			else:
				self.velo.x = 0
			 	
			self.contador += 1
		else:
			self.invencivel=True
			self.contador=0
			self.velo.x=0

		if self.contador==60:
			self.ataque=True
			self.velo.x=0
			self.tiro=Tiro(self.jogo, 48, 48, 8, 6, 3, 3, 5, self.posi+self.posicao_arma, vec(5, 0), vec(0, 0), self.velo, self.olhar_direita, fps)
			self.jogo.tiro_inimigo.add(self.tiro)

		if self.contador == 120:
			self.ataque = False
			self.contador = 0

class Pb(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo, 191, 286, 48, 48, 2, 2, 0, 2, posix, posiy, vec(3, 0), vec(0, grav_jogador))
		self.contador = 0
		self.contato = False
		self.explode = True
		self.tiro = 0
	def eventos(self):
		if abs(self.posi.x - self.jogo.jogador.posi.x) < 30:
			self.velo.x = 0
			if abs(self.posi.y - self.jogo.jogador.posi.y) < 30:
					self.contato = True
		else:
			if self.posi.x > self.jogo.jogador.posi.x:
				self.velo.x =- 3
			else:
				self.velo.x = 3

		if self.contato:
			self.velo.x = 0
		if self.contato:
			self.contador += 1
		if self.contador == 2 and self.explode:
			self.tiro = Tiro(self.jogo, 128, 339, 23, 16, 8, 8, 40, self.rect.midbottom, vec(0, 0), vec(0, 0), self.velo, self.olhar_direita, fps)
			self.jogo.tiro_inimigo.add(self.tiro)
		if self.contador == 2:
			self.kill()

class Chefe(Inim):
		def __init__(self, jogo, posix, posiy):
			Inim.__init__(self, jogo, 0, 191, 189, 137, 1, 1, 3, 40, posix, posiy, vec(-2,0), vec(0,0))
			self.contador=0
			self.contador_ataque=0
			self.modo=0
			self.angulo=90
			self.mao_direita=0
			self.mao_esquerda=0
			self.duas_maos=0
			self.ataque=0
			self.n_ataque=0
			self.jogo.chefe.add(self)
	
		def eventos(self):
			if self.modo==0:
				if self.contador <= 60:
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
					self.invencivel=False
				elif self.contador>=362:

					self.contador_ataque+=1
					
				if self.ataque==0:
					if self.contador_ataque==30:
						self.mao_direita=Inim(self.jogo,193, 0, 63, 126, 1, 1, 0, 50, largura-50,3*altura/4,vec(0,0),vec(0,0))
					elif self.contador_ataque==90 or self.contador_ataque==150 or self.contador_ataque==210:
						Tiro(self.jogo,'img/granada.png',4,self.mao_direita.rect.center,vec(-8,0),vec(0,0),self.velo,self._olhardireita,5*fps)
					elif self.contador_ataque==270:
						self.mao_direita.kill()
					elif self.contador_ataque==300:
						self.n_ataque+=1
						self.ataque=randrange(3)
						self.contador_ataque=0

				elif self.ataque==1:

					if self.contador_ataque==30:
						self.mao_esquerda=Inim(self.jogo, 258, 0, 60, 126, 1, 1, 5,50,50,7*altura/8,vec(0,0),vec(0.5,0))
						
					elif self.contador_ataque==150:
						self.mao_esquerda.kill()
						self.ataque=randrange(3)
						self.contador_ataque=0
						self.n_ataque+=1
				else:
					if self.contador_ataque==30:
						self.duas_maos=Inim(self.jogo,191, 191, 170, 93, 1, 1,5,50,largura/2,altura/2,vec(0,0),vec(0,0.5))

					elif self.contador_ataque==150:
						self.duas_maos.kill()
						self.ataque=randrange(3)
						self.n_ataque+=1
						self.contador_ataque=0

				if self.n_ataque==3:
					self.n_ataque=0
					self.contador=0
					if self.vida<20:
						self.modo=1


			elif self.modo==1:
				if self.contador<=30:
					self.velo=vec(0,6)
				elif self.contador<=150:
					self.invencivel=True
					self.velo=vec(20*math.sin(self.angulo*math.pi/180),20*math.cos(self.angulo*math.pi/180))
					self.angulo+=6
				elif self.contador<=180:
					self.velo=vec(0,-6)
				elif self.contador==181:
					self.velo=vec(0,0)
					self.ataque=randrange(5)
					self.invencivel=False
				elif self.contador>=362:

					self.contador_ataque+=1
					
				if self.ataque==0:
					if self.contador_ataque==30:
						self.mao_direita=Inim(self.jogo,193, 0, 63, 126, 1, 1, 0, 50, largura-50,3*altura/4,vec(0,0),vec(0,0))
					elif self.contador_ataque==90 or self.contador_ataque==150 or self.contador_ataque==210:
						Tiro(self.jogo,'img/granada.png',4,self.mao_direita.rect.center,vec(-8,0),vec(0,0),self.velo,self.olhar_direita,5*fps)
					elif self.contador_ataque==270:
						self.mao_direita.kill()
					elif self.contador_ataque==300:
						self.n_ataque+=1
						self.ataque=randrange(5)
						self.contador_ataque=0

				elif self.ataque==1:

					if self.contador_ataque==30:
						self.mao_esquerda=Inim(self.jogo, 258, 0, 60, 126, 1, 1, 5,50,50,7*altura/8,vec(0,0),vec(1.2,0))
						
					elif self.contador_ataque==105:
						self.mao_esquerda.kill()
						self.mao_esquerda=Inim(self.jogo, 258, 0, 60, 126, 1, 1, 5,50,50,6*altura/8,vec(0,0),vec(1.2,0))

					elif self.contador_ataque==180:
						self.mao_esquerda.kill()
						self.mao_esquerda=Inim(self.jogo, 258, 0, 60, 126, 1, 1, 5,50,50,5*altura/8,vec(0,0),vec(1.2,0))
					elif self.contador_ataque==255:
						self.mao_esquerda.kill()
						self.ataque=randrange(5)
						self.contador_ataque=0
						self.n_ataque+=1

				elif self.ataque==2:

					if self.contador_ataque==30 or self.contador_ataque==180 or self.contador_ataque==330:
						self.duas_maos=Inim(self.jogo, 191, 191, 170, 93, 1, 1, 5, 50,largura/2,altura/2,vec(0,0),vec(0,0.5))

					elif self.contador_ataque==150 or self.contador_ataque==300:
						self.duas_maos.kill()

					elif self.contador_ataque==450:
						self.duas_maos.kill()
						self.ataque=randrange(5)
						self.n_ataque+=1
						self.contador_ataque=0
				elif self.ataque==3:
					if self.contador_ataque==30:
						pass
					self.ataque=randrange(5)
				elif self.ataque==4:
					self.ataque=randrange(5)

				if self.n_ataque==3:
					self.n_ataque=0
					self.contador=0
				self.contador+=1

# ================================================================================================================
# Outros
# ================================================================================================================

class Powerup(pg.sprite.Sprite):
	def __init__(self,jogo,posicao):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = vec(posicao[:])
		self.tempo = 300
		self.aleatorio=randrange(10)
		self.velo=vec(0,0)
		self.acele=vec(0,0.5)
		if self.aleatorio == 0 or self.aleatorio == 1:
			self.image = self.jogo.spritesheet_vida.get_image(0, 0, 48, 41, 1, 1)
		else:
			self.image = self.jogo.spritesheet_tiros.get_image(48, 48, 8, 6, 3, 3)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.rect.midbottom = self.posi

		# Adição nos grupos
		if self.aleatorio==1 or self.aleatorio==2 :
			self.jogo.todos_sprites.add(self)
			self.jogo.interacoes.add(self)
			self.jogo.powerup.add(self)
			self.jogo.nao_moviveis.add(self)
			self.jogo.caintes.add(self)

	def update(self):
		self.posi=self.rect.midbottom
		self.velo+=self.acele
		self.posi+=self.velo+self.acele/2
		self.rect.midbottom=self.posi
		self.tempo-=1
		if self.tempo==0:
			self.kill()

	def atributo(self):
		if self.aleatorio==0 or self.aleatorio==1:
			self.jogo.jogador.vida+=5
		elif self.aleatorio==2:
			self.jogo.jogador.numero_granada+=1

class Bloco_Cai(pg.sprite.Sprite):
	def __init__(self, jogo, posicao):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = vec(posicao[:])
		self.rect = self.image.get_rect()

		# Adição nos grupos
		if self.aleatorio==1 or self.aleatorio==2 :
			self.jogo.todos_sprites.add(self)
			self.jogo.interacoes.add(self)
			self.jogo.powerup.add(self)
			self.jogo.nao_moviveis.add(self)
			self.jogo.caintes.add(self)


	def update(self):
		self.posi = self.rect.midbottom
		self.velo += self.acele
		self.posi += self.velo + self.acele/2
		self.rect.midbottom = self.posi
		self.tempo -= 1
		if self.tempo == 0:
			self.kill()

class Inverte(pg.sprite.Sprite):
	def __init__(self, personagem, image):

		self.todos_sprites = personagem

		self.direita = self.todos_sprites.image
		self.esquerda = pg.transform.flip(self.direita, True, False)

		if self.todos_sprites.olhar_direita:
			self.todos_sprites.image = self.direita
		else:
			self.todos_sprites.image = self.esquerda