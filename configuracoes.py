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
acele_jogador = 6
atrito_jogador = -1
grav_jogador = 0.5
pulo_jogador = 12

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
vermelho = (255, 0, 0)