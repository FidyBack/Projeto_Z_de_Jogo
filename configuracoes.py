'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e Alexandre Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list==PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
	Fontes feitas por Brian Kent (Ænigma) 

Jogo feito em 2018

Aproveite!!!
'''
import pygame as pg

# Variáveis
titulo = 'Soldier'
fps = 60
largura = 1000
altura = 600
nome_fonte = 'Acknowledge TT (BRK)'
background = pg.image.load("img/fundo.jpg")

# Propriedades do jogador
acele_jogador = 6
atrito_jogador = -1
grav_jogador = 0.5
pulo_jogador = 12

# Propriedades do inimigo
acele_inimigo = 4
atrito_inimigo = -1
grav_inimigo = 0.5

# Discurso
discurso = 'Durante a guerra que se segue, o Império Xerista, que anseia pela destruição de seus inimigos \
está perdendo as suas forças pouco a pouco. Para contornar isso, seu líder, \
Herold Smiter, visa as amoebas do infinito. \
É seu dever, Soldier, impedir isso e defender a paz no mundo. Contamos com você...'

# Plataformas
lista_plataformas = [(-1000, altura - 40, 7000, 70),
					(250, 300, 90, 30),
					(300, 300, 90, 30),
					(500, 200, 90, 30),
					(900, 100, 90, 30),
					(1200, 100, 90, 30),
					(100, 450, 90, 30),
					(2000, 300, 90, 30),
					(5000, 100, 90, 30),
					(5000, 150, 90, 30),
					(5000, 200, 90, 30),
					(5000, 250, 90, 30),
					(5000, 300, 90, 30),
					(5000, 350, 90, 30),
					(5000, 400, 90, 30),
					]

# Inimigos
lista_inimigos = [(1500, altura - 120)]

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
ama_esc = (25, 100, 37)
vermelho = (255, 0, 0)


def configuracoes():
	return {
# Variáveis
'titulo' == 'Soldier',
'fps' == 60,
'largura' == 1000,
'altura' == 600,
'nome_fonte' == 'Acknowledge TT (BRK)',
'background' == pg.image.load("img/fundo.jpg"),

# Propriedades do jogador
'acele_jogador' == 6,
'atrito_jogador' == -1,
'grav_jogador' == 0.5,
'pulo_jogador' == 12,

# Propriedades do inimigo
'acele_inimigo' == 4,
'atrito_inimigo' == -1,
'grav_inimigo' == 0.5,

# Discurso
'discurso' == 'Durante a guerra que se segue, o Império Xerista, que anseia pela destruição de seus inimigos \
está perdendo as suas forças pouco a pouco. Para contornar isso, seu líder, \
Herold Smiter, visa as amoebas do infinito. \
É seu dever, Soldier, impedir isso e defender a paz no mundo. Contamos com você...',

# Plataformas
'lista_plataformas' == [(-1000, altura - 40, 7000, 70),
					(250, 300, 90, 30),
					(300, 300, 90, 30),
					(500, 200, 90, 30),
					(900, 100, 90, 30),
					(1200, 100, 90, 30),
					(100, 450, 90, 30),
					(2000, 300, 90, 30),
					(5000, 100, 90, 30),
					(5000, 150, 90, 30),
					(5000, 200, 90, 30),
					(5000, 250, 90, 30),
					(5000, 300, 90, 30),
					(5000, 350, 90, 30),
					(5000, 400, 90, 30),
					],
	
# Inimigos
'lista_inimigos' == [(1500, altura - 120)],

# Cores
'branco' == (255, 255, 255),
'preto' == (0, 0, 0),
'ama_esc' == (25, 100, 37),
'vermelho' == (255, 0, 0),

	}