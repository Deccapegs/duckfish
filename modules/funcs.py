from __main__ import pygame,screen_height,screen_width,window,json,random,chunk_size,screen
import math
game=None
class Func:
	def set_main_game(game_):
		global game
		game=game_
def withscroll(pos):
	return [(pos[0]+game.scroll[0]),(pos[1]+game.scroll[1])]
def withoutscroll(pos):
	return [pos[0]-game.scroll[0],pos[1]-game.scroll[1]]
def add_poses(p1,p2):
	return (p1[0]+p2[0],p1[1]+p2[1])
def get_hyp(list_2):
	return(list_2[0]**2+list_2[1]**2)**0.5
def get_surf_from_sheet(sheet,sheetpos,size):
	s=pygame.Surface(size,pygame.SRCALPHA).convert_alpha()
	s.fill((0,0,0,0))
	s.blit(sheet,sheetpos)
	return s
def make_surf(size,colour,alpha=0):
	surf=pygame.Surface(size,alpha).convert_alpha() if alpha==pygame.SRCALPHA else pygame.Surface(size,alpha).convert()
	surf.fill(colour)
	return surf
def make_circle_surf(radius,colour):
	surf=pygame.Surface([radius*2,radius*2],pygame.SRCALPHA).convert_alpha()
	surf.fill((0,0,0,0))
	pygame.draw.circle(surf,colour,(radius,radius),radius)
	return surf
def make_hole(surf,hole_surf,pos=(0,0))->pygame.Surface:
	mask=pygame.mask.from_surface(hole_surf)
	hole=mask.to_surface(setcolor=(255,255,255),unsetcolor=(0,0,0)).convert()
	hole.set_colorkey((0,0,0,0))
	surf.blit(hole,pos,special_flags=pygame.BLEND_RGB_SUB)
	return surf
def mouse_get_pos():
	x,y=pygame.mouse.get_pos()
	scale=[screen_width/window.get_width(),screen_height/window.get_height()]
	return [x*scale[0],y*scale[1]]
def mouse_get_speed():
	x,y=pygame.mouse.get_rel()
	scale=[screen_width/window.get_width(),screen_height/window.get_height()]
	return [x*scale[0],y*scale[1]]
def get_dist(p1,p2):
	return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5
def clamp(val,range_):
	range_.sort()
	return min(max(val,range_[0]),range_[1])
def add_dicts(list_of_dicts):
	l=list_of_dicts
	keys=[]
	for d in l:
		for i in d:
			if i not in keys:
				keys.append(i)
	d_={k:0 for k in keys}
	for k in keys:
		for d in l:
			try:
				d_[k]+=d[k]
			except KeyError:
				pass
	return d_
def dict_insert(dict_,key_value_pair,place_after_key):
	d_=dict_
	kv=key_value_pair
	p=place_after_key
	kvs=[(key,d_[key]) for key in d_]
	pos= [i for i,k in enumerate(d_) if k==p][0]+1
	kvs.insert(pos,kv)
	return {k[0]:k[1] for k in kvs}
def dict_choice(dict_:dict):
	choice=random.random()*sum(list(dict_.values()))
	num=[0,0]
	for key,val in list(dict_.items()):
		num[0]+=val
		if num[0]>choice>num[1]:
			return key
		num[1]=float(num[0])
	return None

def sign_of(int_)->int:
	return 1 if int_>=0 else -1
class timer():
	def __init__(self,interval):
		self.interval=interval
		self.timer=0
		self.tick=False
	def update(self):
		self.timer+=1
		self.tick=False
		if self.timer>=self.interval:
			self.timer=0
			self.tick=True
	def reset(self):
		self.timer=0
class Sin():
	def __init__(self,frequency,height,start=0):
		self.frequency=frequency
		self.height=height
		self.val=0
		self.start=start
		self.timer=start
		self.reset_=1/frequency*math.pi*2

	def update(self):
		self.timer+=self.frequency
		self.timer%=self.reset_
		self.val=math.sin(self.timer)*self.height
	def reset(self):
		self.timer=self.start
class curve_mult():
	def __init__(self,frequency=1/60,height=1,offset=-0.5):
		self.sin=Sin(frequency,height,offset)
		self.val=self.sin.val
	def update(self):
		self.sin.update()

		self.val=self.sin.val
	def reset(self):
		self.sin.reset()
class file():
	def __init__(self,path):
		self.path=str(path)
		self.file=open(self.path)
		self.file.close()
	def overwrite(self,dict_,indent_=4):
		with open(self.path,"w") as self.file:
			self.file.write(json.dumps(dict_,indent=indent_))
	def read(self):
		with open(self.path,"r") as file:
			return json.load(file)
def get_house_rect(img,height=1/3,init_pos=[0,0],check_heights=[0]):
	#if height is <1, the the returned height with be the product of the img height and parameter height
	size=list(img.get_size())
	check_pos=[0,size[1]-1]
	pos=[0,0]
	offset=0
	for i in range(size[0]):
		check_pos[0]=i
		
		colour=img.get_at(check_pos)
		if (alpha:=colour[3])==255:
			offset=int(i)
			pos[0]=i
			size[0]-=i
			break

	for i in range(size[0]):
		check_pos[0]=size[0]-i-1+offset
		colour=img.get_at(check_pos)
		if (alpha:=colour[3])==255:
			size[0]-=i
			break
	new_height=1
	if height<1:
		new_height=size[1]*height
	else:
		new_height=height
	pos[1]-=new_height#math is not spagagtti
	size[1]=new_height
	rect=pygame.Rect(add_poses(pos,init_pos),size)
	return rect
def get_tile_pos(pos,tile_size=32):
	return [math.floor(pos[0]/32),math.floor(pos[1]/32)]

def get_chunk_pos(pos,tile=False):
	return [math.floor(pos[0]/32/chunk_size[0]),math.floor(pos[1]/32/chunk_size[1])]
	
def center_surf(surf):
	rect=surf.get_rect(center=(screen_width/2,screen_height/2))
	return list(rect.topleft)