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
		self.pulador = 0
		self.contador_invencivel = 0
		self.invencivel = False
		self.pular = False
		self.olhar_direita = True
		self.andando = False
		self.pulando = False
		self.temporizador = 0
		# Animação
		self.ultimo_update = 0
		self.frame_atual = 0
		self.carregar_imagens()
		self.image = self.frames_parados_r[0]
		self.rect = self.image.get_rect()
		# Posição
		self.posi = vec(largura * 1 / 2, altura - 130)
		self.velo = vec(0, 0)
		self.acele = vec(0, grav_jogador)
		# Tiro
		self.contador_tiro = 0
		self.tiro_reto = False
		self.tiro_parabola = False
		self.vel_tiro_reto = vec(20,0)
		self.vel_tiro_parabola = vec(10,-10)
		self.posicao_arma = vec(20,-25)
		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.caracters.add(self)
		self.jogo.moviveis.add(self)

	# Imagens da animação
	def carregar_imagens(self):
		# Parado
		self.frames_parados_r = [self.jogo.spritesheet_personagem.get_image(183, 72, 30, 34, 2, 2),
								self.jogo.spritesheet_personagem.get_image(191, 411, 30, 34, 2, 2),
								self.jogo.spritesheet_personagem.get_image(202, 181, 30, 34, 2, 2),
								self.jogo.spritesheet_personagem.get_image(191, 411, 30, 34, 2, 2),
								self.jogo.spritesheet_personagem.get_image(183, 72, 30, 34, 2, 2),]

		self.frames_parados_l = []
		for frame_parado in self.frames_parados_r:
			frame_parado.set_colorkey(preto)
			self.frames_parados_l.append(pg.transform.flip(frame_parado, True, False))

		# Andando
		self.frames_andando_r = [self.jogo.spritesheet_personagem.get_image(305, 0, 20, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(285, 308, 23, 35, 2, 2),
									self.jogo.spritesheet_personagem.get_image(136, 232, 32, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(93, 267, 34, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(247, 47, 26, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(294, 94, 22, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(283, 441, 25, 35, 2, 2),
									self.jogo.spritesheet_personagem.get_image(183, 36, 30, 34, 2, 2),
									self.jogo.spritesheet_personagem.get_image(114, 0, 34, 33, 2, 2),
									self.jogo.spritesheet_personagem.get_image(226, 279, 29, 33, 2, 2),]

		self.frames_andando_l = []
		for frame_andando in self.frames_andando_r:
			frame_andando.set_colorkey(preto)
			self.frames_andando_l.append(pg.transform.flip(frame_andando, True, False))

		# Pulando
		self.frames_pulando_r = [self.jogo.spritesheet_personagem.get_image(286, 241, 24, 37, 2, 2),
									self.jogo.spritesheet_personagem.get_image(312, 181, 15, 41, 2, 2),
									self.jogo.spritesheet_personagem.get_image(310, 364, 19, 46, 2, 2),
									self.jogo.spritesheet_personagem.get_image(287, 163, 23, 41, 2, 2),
									self.jogo.spritesheet_personagem.get_image(257, 264, 27, 42, 2, 2),
									self.jogo.spritesheet_personagem.get_image(284, 389, 24, 38, 2, 2),
									self.jogo.spritesheet_personagem.get_image(195, 245, 30, 32, 2, 2)]

		self.frames_pulando_l = []
		for frame_pulando in self.frames_pulando_r:
			frame_pulando.set_colorkey(preto)
			self.frames_pulando_l.append(pg.transform.flip(frame_pulando, True, False))

	# Movimento
	def update(self):
		self.animacao()

		# Esquerda
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.velo.x = -velo_jogador
			self.andando = True
			self.olhar_direita = False
			self.posicao_arma.x = -20
		# Direita
		elif keys[pg.K_d]:
			self.velo.x = velo_jogador
			self.andando = True
			self.olhar_direita = True
			self.posicao_arma.x = 20
		else:
			self.velo.x = 0
			self.andando = False

		# Velocidade somada com a aceleração
		self.velo += self.acele
		if abs(self.velo.x) < 0.1:
			self.velo.x = 0
		# Sorvetão (Indica a pórxima posição do personagem)
		self.posi += self.velo + 0.5 * self.acele
		# Define a posição do centro do personagem embaixo
		self.rect.midbottom = self.posi

	# Animação
	def animacao(self):
		agora = pg.time.get_ticks()

		# Animação andando
		if self.andando:
			if agora - self.ultimo_update > 40:
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
		if not self.pulando and not self.andando:
			if self.frame_atual == 4:
				agora -= 3000
			if agora - self.ultimo_update > 50:
				self.ultimo_update = agora
				self.frame_atual = (self.frame_atual + 1) % len(self.frames_parados_r)
				bottom = self.rect.bottom
				if self.olhar_direita:
					self.image = self.frames_parados_r[self.frame_atual]
				else:
					self.image = self.frames_parados_l[self.frame_atual]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		# Animação atirando

	# Pulo
	def pulo(self):

		# Pula apenas se o número de pulos for menor que 2
		if self.pulador < 2:
			self.pular = True
			self.pulando = True
			self.andando = False
			if self.pular:
					self.velo.y = -pulo_jogador
			self.pulador += 1
			if self.posi.y < 0:
				self.velo.y = 0
			self.pular = False

	# Pulo pequeno
	def pulo_parar_meio(self):
		if self.pular:
			if self.velo.y < -5:
				self.velo.y = -5

class Plataforma(pg.sprite.Sprite):
	def __init__(self, jogo, x, y):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_plataformas.get_image(322, 82, 48, 48, 1, 1)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)

class Chao(Plataforma):
	def __init__(self, jogo, x, y):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_plataformas.get_image(322, 82, 48, 48, 5, 5)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Adição nos grupos
		self.jogo.todos_sprites.add(self)
		self.jogo.plataforma.add(self)
		self.jogo.interacoes.add(self)

# ================================================================================================================
# Tiro
# ================================================================================================================

class Tiro(pg.sprite.Sprite):
	def __init__(self, jogo, image, dano, posicao, velo, acele, velo_personagem, direita, tempo):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.posi = vec(posicao[:])
		self.image = pg.image.load(image)
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

	def update(self):
		if self.olhar_direita:
			self.velo.x = self.vel
		else:
			self.velo.x = -self.vel
		self.eventos()
		self.tempo-=1
		if self.tempo==0:
			self.kill()
		self.velo += self.acele
		self.posi += self.velo + self.acele/2 
		self.posi.x += self.velo_personagem.x
		self.rect.center = self.posi

	def eventos(self):
		pass

class Tiro_reto(Tiro):
	def __init__(self, jogo, posicao, velo, velo_personagem, direita):
	 	Tiro.__init__(self, jogo, 'img/Fireball.png', 1, posicao, velo, vec(0, 0), velo_personagem, direita, fps)
	 	self.jogo.tiro_personagem.add(self)

class Tiro_parabola(Tiro):
	def __init__(self,jogo,posicao,velo,velo_personagem,direita):
		Tiro.__init__(self, jogo, 'img/granada.png', 5, posicao, velo, vec(0, 0.5), velo_personagem, direita,fps)
		self.jogo.tiro_personagem.add(self)

# ================================================================================================================
# Inimigos
# ================================================================================================================

class Inim(pg.sprite.Sprite):
	def __init__(self, jogo, x, y, largura, altura, lar_dim, alt_dim, dano, vida, posix, posiy, velo, acele):
		pg.sprite.Sprite.__init__(self)
		self.jogo = jogo
		self.image = self.jogo.spritesheet_pedra.get_image(x, y, largura, altura, lar_dim, alt_dim)
		self.image.set_colorkey(preto)
		self.rect = self.image.get_rect()
		self.posi = vec(posix,posiy)
		self.rect.midbottom = self.posi
		self.vida = vida
		self.dano = dano
		self.direita = True
		self.velo = velo
		self.acele = acele
		self.invencivel = False

		# Adição nos grupos
		self.jogo.caracters.add(self)
		self.jogo.todos_sprites.add(self)
		self.jogo.inimigos.add(self)
		self.jogo.interacoes.add(self)
		self.jogo.moviveis.add(self)

	def update(self):
		if self.velo.x > 0:
			self.direita = True
		elif self.velo.x < 0:
			self.direita = False
		if self.posi.x >- 100 and self.posi.x < largura + 100:
			self.velo += self.acele
			self.posi += self.velo + 0.5 * self.acele
		self.rect.midbottom = self.posi
		self.eventos()

	def eventos(self):
		pass

class Pedra(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo , 32, 32, 30, 30, 6, 6, 3, 5, posix, posiy, vec(-3,0), vec(0, grav_jogador))

	# def carregar_imagem(self):
	# 	# Andando
	# 	self.frames_parados_r = [self.jogo.spritesheet_personagem.get_image(183, 72, 30, 34, 2, 2),
	# 							self.jogo.spritesheet_personagem.get_image(191, 411, 30, 34, 2, 2),
	# 							self.jogo.spritesheet_personagem.get_image(202, 181, 30, 34, 2, 2),
	# 							self.jogo.spritesheet_personagem.get_image(191, 411, 30, 34, 2, 2),
	# 							self.jogo.spritesheet_personagem.get_image(183, 72, 30, 34, 2, 2),]


	# def eventos(self):
	# 	if self.andando:
	# 		if agora - self.ultimo_update > 40:
	# 			self.ultimo_update = agora
	# 			self.frame_atual = (self.frame_atual + 1) % len(self.frames_andando_l)
	# 			bottom = self.rect.bottom
	# 			if self.velo.x > 0:
	# 				self.image = self.frames_andando_r[self.frame_atual]
	# 			else:
	# 				self.image = self.frames_andando_l[self.frame_atual]
	# 			self.rect = self.image.get_rect()
	# 			self.rect.bottom = bottom

class Robo(Inim):
	def __init__(self, jogo, posix, posiy):
		Inim.__init__(self, jogo, "img/robo.png", 3, 5, posix, posiy, vec(0, 0), vec(0, grav_jogador))
		self.contador = 0
		self.veltiro = vec(10, 0)
		self.velx = 0
		self.posicao_arma = vec(50, -100)
		self.tiro = 0

	def eventos(self):
		if self.direita:
			self.posicao_arma.x = 50
		else:
			self.posicao_arma.x = -50
		if self.contador == 120:
		 	self.velo.x = 0
		 	self.tiro = Tiro(self.jogo, 'img/granada.png', 5, self.posi + self.posicao_arma, self.veltiro, vec(0, 0), self.velo, self.direita, fps)
		 	self.jogo.tiro_inimigo.add(self.tiro)

		elif self.contador == 150:
		 	self.velx =- self.velx
		 	self.direita = not self.direita
		 	self.velo.x = self.velx
		 	self.contador = 0
		
		self.contador += 1

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

class Spike(Inim):
		def __init__(self, jogo, posix, posiy):
			Inim.__init__(self, jogo, "img/espinho.png", 500, 400, posix, posiy, vec(0,0), vec(0,0))
			self.invencivel = True

class Chefe(Inim):
		def __init__(self,jogo,posix,posiy):
			Inim.__init__(self,jogo,"img/head.png",3,40,posix,posiy,vec(-2,0),vec(0,0))
			self.contador=0
			self.contador_ataque=0
			self.modo=0
			self.angulo=90
			self.mao_direita=0
			self.mao_esquerda=0
			self.duas_maos=0
			self.ataque=0
			self.n_ataque=0
			
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
						self.mao_direita=Inim(self.jogo,"img/right.png",0,50,largura-50,3*altura/4,vec(0,0),vec(0,0))
					elif self.contador_ataque==90 or self.contador_ataque==150 or self.contador_ataque==210:
						Tiro(self.jogo,'img/granada.png',4,self.mao_direita.rect.center,vec(-8,0),vec(0,0),self.velo,self.direita,5*fps)
					elif self.contador_ataque==270:
						self.mao_direita.kill()
					elif self.contador_ataque==300:
						self.n_ataque+=1
						self.ataque=randrange(3)
						self.contador_ataque=0

				elif self.ataque==1:

					if self.contador_ataque==30:
						self.mao_esquerda=Inim(self.jogo,"img/left.png",5,50,50,7*altura/8,vec(0,0),vec(0.5,0))
						
					elif self.contador_ataque==150:
						self.mao_esquerda.kill()
						self.ataque=randrange(3)
						self.contador_ataque=0
						self.n_ataque+=1
				else:
					if self.contador_ataque==30:
						self.duas_maos=Inim(self.jogo,"img/both.png",5,50,largura/2,altura/2,vec(0,0),vec(0,0.5))

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
						self.mao_direita=Inim(self.jogo,"img/right.png",0,50,largura-50,3*altura/4,vec(0,0),vec(0,0))
					elif self.contador_ataque==90 or self.contador_ataque==150 or self.contador_ataque==210:
						Tiro(self.jogo,'img/granada.png',4,self.mao_direita.rect.center,vec(-8,0),vec(0,0),self.velo,self.direita,5*fps)
					elif self.contador_ataque==270:
						self.mao_direita.kill()
					elif self.contador_ataque==300:
						self.n_ataque+=1
						self.ataque=randrange(5)
						self.contador_ataque=0

				elif self.ataque==1:

					if self.contador_ataque==30:
						self.mao_esquerda=Inim(self.jogo,"img/left.png",5,50,50,7*altura/8,vec(0,0),vec(1.2,0))
						
					elif self.contador_ataque==105:
						self.mao_esquerda.kill()
						self.mao_esquerda=Inim(self.jogo,"img/left.png",5,50,50,6*altura/8,vec(0,0),vec(1.2,0))

					elif self.contador_ataque==180:
						self.mao_esquerda.kill()
						self.mao_esquerda=Inim(self.jogo,"img/left.png",5,50,50,5*altura/8,vec(0,0),vec(1.2,0))
					elif self.contador_ataque==255:
						self.mao_esquerda.kill()
						self.ataque=randrange(5)
						self.contador_ataque=0
						self.n_ataque+=1

				elif self.ataque==2:

					if self.contador_ataque==30 or self.contador_ataque==180 or self.contador_ataque==330:
						self.duas_maos=Inim(self.jogo,"img/both.png",5,50,largura/2,altura/2,vec(0,0),vec(0,0.5))

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
#alteration
class Powerup(pg.sprite.Sprite):
	def __init__(self,jogo,posicao):
		pg.sprite.Sprite.__init__(self)
		self.jogo=jogo
		self.posicao=vec(posicao[:])
		self.image = pg.Surface((32,32))
		self.image.fill(vermelho)
		self.rect = self.image.get_rect()
		self.rect.midbottom=self.posicao
		self.tempo=300
		self.vida=5

		# Adição nos grupos
		if randrange(2)==1:
			self.jogo.todos_sprites.add(self)
			self.jogo.interacoes.add(self)
			self.jogo.powerup.add(self)


	def update(self):
		self.tempo-=1
		if self.tempo==0:
			self.kill()

