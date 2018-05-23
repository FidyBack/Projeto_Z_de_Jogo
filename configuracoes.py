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
background = pg.image.load("img/fundo.png")
spritesheet_pedra = "sprites_pedra.png"
spritesheet_personagem = "sprites_personagem.png"
spritesheet_plataformas = "sprites_plataformas.png"

# Propriedades do jogador
grav_jogador = 1
pulo_jogador = 20
velo_jogador = 8

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

					'chaos' : [
								# Parte 1
									(40, altura - 120),
									(270, altura - 120),
									(500, altura - 120),
									(730, altura - 120),
									(1300, altura - 120),
									(1530, altura - 120),
									(2100, altura - 120),
									(2500, altura - 120),
									(2900, altura - 120),
									(3300, altura - 120),
									# Escada
									(4100, altura - 120),
									(4330, altura - 220),
									(4560, altura - 320),
									(4790, altura - 420),
									(5020, altura - 520),
									(5250, altura - 620),
								# Parte 2
									(5480, altura - 620),
									(8000, altura - 1750),
									(8230, altura - 1750),
									(8460, altura - 1750),
								# Parte 3
									(8690, altura - 620),
									(8920, altura - 620),
									(9150, altura - 620),
									(9380, altura - 620),
									(9610, altura - 620),
									(11900, altura - 1300),
								],

					'plataformas' : [
									# Parte 1
										(1500, altura - 300),
										(1546, altura - 300),
										(1592, altura - 300),
										(1638, altura - 300),

										(1800, altura - 410),
										(1846, altura - 410),
										(1892, altura - 410),
										(1938, altura - 410),

										(2600, altura - 530),
										(2646, altura - 530),
										(2692, altura - 530),
										(2738, altura - 530),

										(3400, altura - 530),
										(3446, altura - 530),
										(3492, altura - 530),
										(3538, altura - 530),
									
									# Parte 2
										(5800, altura - 850),
										(5846, altura - 850),
										(5892, altura - 850),
										(5938, altura - 850),

										(6100, altura - 1000),
										(6146, altura - 1000),
										(6192, altura - 1000),
										(6238, altura - 1000),

										(6400, altura - 1150),
										(6446, altura - 1150),
										(6492, altura - 1150),
										(6538, altura - 1150),

										(6700, altura - 1300),
										(6746, altura - 1300),
										(6792, altura - 1300),
										(6838, altura - 1300),

										(7000, altura - 1450),
										(7046, altura - 1450),
										(7092, altura - 1450),
										(7138, altura - 1450),

										(7300, altura - 1600),
										(7346, altura - 1600),
										(7392, altura - 1600),
										(7438, altura - 1600),

										(7600, altura - 1750),
										(7646, altura - 1750),
										(7692, altura - 1750),
										(7738, altura - 1750),

									# Parte 3
										(9850, altura - 1750),
										(9896, altura - 1750),
										(9942, altura - 1750),
										(9988, altura - 1750),

										(10400, altura - 1750),
										(10446, altura - 1750),
										(10492, altura - 1750),
										(10538, altura - 1750),

										(10950, altura - 1750),
										(10996, altura - 1750),
										(11042, altura - 1750),
										(11088, altura - 1750),

										(11500, altura - 1750),
										(11546, altura - 1750),
										(11592, altura - 1750),
										(11638, altura - 1750),

										(10125, altura - 1500),
										(10171, altura - 1500),
										(10217, altura - 1500),
										(10263, altura - 1500),

										(10675, altura - 1500),
										(10721, altura - 1500),
										(10767, altura - 1500),
										(10813, altura - 1500),

										(11250, altura - 1500),
										(11296, altura - 1500),
										(11342, altura - 1500),
										(11388, altura - 1500),

										(9850, altura - 1250),
										(9896, altura - 1250),
										(9942, altura - 1250),
										(9988, altura - 1250),

										(10400, altura - 1250),
										(10446, altura - 1250),
										(10492, altura - 1250),
										(10538, altura - 1250),

										(10950, altura - 1250),
										(10996, altura - 1250),
										(11042, altura - 1250),
										(11088, altura - 1250),

										(11500, altura - 1250),
										(11546, altura - 1250),
										(11592, altura - 1250),
										(11638, altura - 1250),

										(10125, altura - 1000),
										(10171, altura - 1000),
										(10217, altura - 1000),
										(10263, altura - 1000),

										(10675, altura - 1000),
										(10721, altura - 1000),
										(10767, altura - 1000),
										(10813, altura - 1000),

										(11250, altura - 1000),
										(11296, altura - 1000),
										(11342, altura - 1000),
										(11388, altura - 1000),

										(9850, altura - 750),
										(9896, altura - 750),
										(9942, altura - 750),
										(9988, altura - 750),

										(10400, altura - 750),
										(10446, altura - 750),
										(10492, altura - 750),
										(10538, altura - 750),

										(10950, altura - 750),
										(10996, altura - 750),
										(11042, altura - 750),
										(11088, altura - 750),

										(11500, altura - 750),
										(11546, altura - 750),
										(11592, altura - 750),
										(11638, altura - 750),

								]
}


# Inimigos
lista_inimigos = {
					'pedra': [
								(900, altura - 130),
								(5250, altura - 620),
								(5250, altura - 640),
								(5250, altura - 660),

							],
	
					'robo' : [

					],
	
					'mineiro' : [
					],
	
					'pb' : [


							],

					'spike' : [	

								]
}