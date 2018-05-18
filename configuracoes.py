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
grav_jogador = 0.5
pulo_jogador = 15
velo_jogador = 18

# Propriedades do inimigo
grav_inimigo = 0.5

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verd_esc = (25, 100, 37)
azul_ceu = (0, 255, 255)
vermelho = (255, 0, 0)

# Discurso
discurso = 'Durante a guerra que se segue, o Império Xerista,  \
está perdendo as suas forças pouco a pouco. Para contornar isso, seu líder, \
Herold Smiter, visa as amoebas do infinito. \
É seu dever, Soldier, impedir isso e defender a paz no mundo. Contamos com você...'

# ================================================================================================================
# Listas
# ================================================================================================================

# Plataformas
lista_plataformas = {

					'chãos' : [ # Parte 1
								(0, altura - 120, 1000, 200),
								(1300, altura - 120, 500, 200),
								(2100, altura - 120, 20, 200),
								(2500, altura - 120, 20, 200),
								(2900, altura - 120, 20, 200),
								(3300, altura - 120, 20, 200),
								(3700, altura - 120, 20, 200),
								# Escada
								(4100, altura - 120, 200, 200),
								(4300, altura - 220, 200, 300),
								(4500, altura - 320, 200, 400),
								(4700, altura - 420, 200, 500),
								(4900, altura - 520, 200, 600),
								(5100, altura - 620, 200, 700),
								# Parte 2
								(5300, altura - 620, 2700, 710),
								(8000, altura - 1750, 1500, 1860),
								# Parte 3
								(9500, altura - 620, 2400, 710),
								(11900, altura - 1300, 2000, 800)
							],

					'plataformas' : [
										# Parte 1
										(1500, altura - 300, 200, 25),
										(1800, altura - 410, 200, 25),
										(2600, altura - 530, 200, 25),
										(3400, altura - 530, 200, 25),
										
										# Parte 2
										(5800, altura - 850, 200, 25),
										(6100, altura - 1000, 200, 25),
										(6400, altura - 1150, 200, 25),
										(6700, altura - 1300, 200, 25),
										(7000, altura - 1450, 200, 25),
										(7300, altura - 1600, 200, 25),
										(7600, altura - 1750, 200, 25),
										
										# Parte 3
										(9850, altura - 1750, 200, 25),
										(10400, altura - 1750, 200, 25),
										(10950, altura - 1750, 200, 25),
										(11500, altura - 1750, 200, 25),

										(10125, altura - 1500, 200, 25),
										(10675, altura - 1500, 200, 25),
										(11250, altura - 1500, 200, 25),

										(9850, altura - 1250, 200, 25),
										(10400, altura - 1250, 200, 25),
										(10950, altura - 1250, 200, 25),
										(11500, altura - 1250, 200, 25),

										(10125, altura - 1000, 200, 25),
										(10675, altura - 1000, 200, 25),
										(11250, altura - 1000, 200, 25),

										(9850, altura - 750, 200, 25),
										(10400, altura - 750, 200, 25),
										(10950, altura - 750, 200, 25),
										(11500, altura - 750, 200, 25),

								]
}


# Inimigos
lista_inimigos = {
					'pedra': [
								(5000, altura - 630),
								(1000, altura - 120),
								(2000, altura - 120),
							],
	
					'dragao' : [],
	
					'mineiro' : [],
	
					'pb' : [],
}