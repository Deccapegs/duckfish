
def make_decr():
	class cdecr():
		def __init__(self,img,pos,anchor="midleft"):
			self.pos=pos
			self.img=img
			try:
				self.rect=self.img.get_rect()
				self.size=self.img.get_size()
			except AttributeError:
				self.size=self.img.img.get_size()
				self.rect=self.img.img.get_rect()
			setattr(self.rect,anchor,self.pos)
			self.y_order=self.rect.midbottom[1]
			game.drawlist.append(self)
		def update(self):
			try:
				self.img.update()
			except AttributeError:
				pass
		def draw(self):
			try:
				screen.blit(self.img,withscroll((self.rect.topleft)))
			except TypeError:
				self.img.draw(withscroll((self.rect.topleft)))
	return cdecr
def make_wave():
	class cWave():
		def __init__(self,pos):
			self.pos=pos
			self.img=animation(image.wave,[25,5],15)
			self.timer=0
			game.waves.append(self)
			self.y_order=self.pos[1]-5
		def update(self): 
			self.img.update()
			self.timer+=1
			if self.timer>=150:
				self.pop()
				return None
		def draw(self):
			self.img.draw(withscroll(self.pos))
		def pop(self):
			try:
				game.waves.remove(self)
				game.drawlist.remove(self)
				del self
				return None
			except ValueError:
				pass
	return cWave