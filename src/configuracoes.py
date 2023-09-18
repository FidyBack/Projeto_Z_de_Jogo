"""
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
"""

import pygame as pg
from os import path

# Variáveis
titulo = "Soldier"
fps = 60
largura = 576
altura = 576
nome_fonte = "Acknowledge TT (BRK)"
background = pg.image.load(path.join(path.dirname(__file__), "img", "fundo.png"))
spritesheet_inimigos = "spritesheet_inimigos.png"
spritesheet_personagem = "spritesheet_personagem.png"
spritesheet_plataformas = "spritesheet_plataformas.png"
spritesheet_vida = "spritesheet_vida.png"
spritesheet_tiros = "spritesheet_tiros.png"

# Propriedades do jogador
grav_jogador = 1
pulo_jogador = 15
velo_jogador = 9

# Propriedades do inimigo
grav_inimigo = 1

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verd_esc = (25, 100, 37)
azul_ceu = (0, 255, 255)
vermelho = (255, 0, 0)
cinza = (0, 65, 102)

# Discurso
discurso = "Durante a guerra que se segue, o Império Xerista, \
está perdendo as suas forças pouco a pouco. Para contornar isso, seu líder, \
Herold Smiter, visa as amoebas do infinito. \
É seu dever, Soldier, impedir isso e defender a paz no mundo. Contamos com você ..."
