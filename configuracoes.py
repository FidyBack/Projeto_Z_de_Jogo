'''
Jogo feito por Abel Cavalcante, Rodrigo de Jesus e André Cury

Jogo baseado na videoaula da ONG 'KidsCanCode', que ensina jovens à programar
	Canal no youtube: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
	Playlist usada para essa programação: https://www.youtube.com/playlist?list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq

Jogo feito em 2018

Aproveite!!!
'''


# Configurações do jogo
# Variáveis
titulo = "Fat Yoshi"
fps = 60
largura = 1000
altura = 600

# Propriedades do jogador
acele_jogador = 5
atrito_jogador = -1
grav_jogador = 0.6
pulo_jogador = 15

# Plataformas
lista_plataformas = [(-1000, altura - 40, 7000, 400),
					(100, 400, 100, 20),
					(300, 300, 90, 20),
					(500, 200, 90, 20),
					(900, 100, 90, 20),
					(1200, 100, 90, 20),
					(2000, 300, 90, 20)]

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
ama_esc = (25, 100, 37)
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
