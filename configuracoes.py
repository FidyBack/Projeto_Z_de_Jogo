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

# Variáveis
titulo = "Soldier"
fps = 60
largura = 1000
altura = 600
nome_fonte = 'Acknowledge TT (BRK)'
background = pg.image.load("img/fundo.jpg")

# # Camadas
# camada_jogador = 2
# camada_inimigo = 2
# camada_platafoma = 1

# Propriedades do jogador
grav_jogador = 0.5
pulo_jogador = 13
velo_jogador = 7

# Propriedades do inimigo
acele_inimigo = 4
atrito_inimigo = -1
grav_inimigo = 0.5

# Propriedades do inimigo
acele_inimigo = 4
atrito_inimigo = -1
grav_inimigo = 0.5

# Discurso
discurso = 'Durante a guerra que se segue, o Império Xerista,  \
está perdendo as suas forças pouco a pouco. Para contornar isso, seu líder, \
Herold Smiter, visa as amoebas do infinito. \
É seu dever, Soldier, impedir isso e defender a paz no mundo. Contamos com você...'

# Plataformas
lista_plataformas = [(0, altura - 40, 7000, 70),

					]

inimigos = {'golem':[
				(1000, altura - 120),

				],
			'dragao':[],
			'mineiro':[],
			'bomber':[],
			'':[]}
# Inimigos
lista_inimigos = [
				(500, altura/2)
	
				]

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
ama_esc = (25, 100, 37)
vermelho = (255, 0, 0)