class Tiro(pg.sprite.Sprite):
		def _init_(self,jogo):
			pg.sprite.Sprite._init_(self)
			self.jogo=jogo
			self.image = pg.image.load('img/FatYoshi.png')
			self.rect = self.image.get_rect()
			self.rect.center=(self.jogo.jogador.posi)
			self.velo=vec(10,0)
		def atirar(self):
			keys = pg.get_pressed()
			if keys[pg.K_j]
				self.rect.x+=vel_tiro