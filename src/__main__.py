import pygame as pg

from .main import Jogo
from os import path

# ================================================================================================================
# Looping em sí
# ================================================================================================================

if __name__ == "__main__":
    g = Jogo()
    g.introducao()

    game = g.novo()
    while g.rodando:
        try:
            while True:
                next(game)

                if not g.jogando and g.rodando:
                    g.mostrar_tela_final(
                        path.join(path.dirname(__file__), "img/game_over.png"),
                        "press any key to continue",
                    )

                if not g.jogando and g.rodando and g.venceu:
                    g.you_win()
        except StopIteration:
            game = g.novo()

    pg.quit()
