'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

Jogo feito em 2018

Aproveite!!!
'''
import pygame as pg

# Variáveis
titulo = "Soldier"
fps = 60
largura = 1000
altura = 600
nome_fonte = 'Times New Roman'
# background = pg.image.load("img/fundo.png")

# Propriedades do jogador
<<<<<<< HEAD
acele_jogador = 5
atrito_jogador = -1
grav_jogador = 0.6
pulo_jogador = 15
=======
acele_jogador = 6
atrito_jogador = -1
grav_jogador = 0.5
pulo_jogador = 12
>>>>>>> 1a07f37bd3e7bf92b6861346dc8617796bb7fbd2

# Plataformas
lista_plataformas = [(-1000, altura - 40, 7000, 40),
					(250, 300, 90, 30),
					(300, 300, 90, 30),
					(500, 200, 90, 30),
					(900, 100, 90, 30),
					(1200, 100, 90, 30),
					(100, 450, 90, 30),
					(2000, 300, 90, 30)]

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
ama_esc = (25, 100, 37)
<<<<<<< HEAD
vermelho = (255, 0, 0)

#fonte
nome_da_fonte='Acknowledge TT (BRK)'

discurso='O império Xeirista quer acabar com os seus inimigos. \
Durante a guerra que se segue, o império está perdendo as suas \
forças pouco a pouco. Para contornar isso, o lider do império \
Xerista Herold Smiter quer as Amoebas do Infinito. É seu dever, \
Soldier, impedir isso e defender a paz no mundo. Vá na sua aventura...'
 
def get_configuracoes():
	return {
			'titulo': "Fat Yoshi",
			'fps': 60,
			'largura': 1000,
			'altura': 600,

			# Propriedades do jogador
			'acele_jogador': 1.7,
			'atrito_jogador': -0.5,
			'grav_jogador': 0.2,
			'pulo_jogador': 10,

			# Plataformas
			'lista_plataformas': [(-1000, altura - 40, 7000, 400),
								(100, 400, 100, 20),
								(300, 300, 90, 20),
								(500, 200, 90, 20),
								(900, 100, 90, 20),
								(1200, 100, 90, 20),
								(2000, 300, 90, 20)],

			# Cores
			'branco': (255, 255, 255),
			'preto': (0, 0, 0),
			'verd_esc': (25, 100, 37),
			'vermelho': (255, 0, 0),
	}
=======
vermelho = (255, 0, 0)
>>>>>>> 1a07f37bd3e7bf92b6861346dc8617796bb7fbd2
