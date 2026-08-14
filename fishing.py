import pygame, random,math,json,sys,os,threading
from random import randint
from collections import Counter
pygame.init()
screen_width=236
screen_height=118
chunk_size=[6,4]

info=pygame.display.Info()
window= pygame.display.set_mode((info.current_w,info.current_h-63),pygame.RESIZABLE)
#window= pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)
screen=pygame.Surface((screen_height,screen_width)).convert_alpha()
pygame.display.set_caption("fishing game")
clock=pygame.time.Clock()
import ctypes
import os
import platform

# Fix for Windows
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
        except Exception:
            pass
from modules.funcs import*
import modules.maps as maps
if __name__!="__main__":
	sys.exit()
class Types():
	def __init__(self):
		self.stall_1=0
		self.golf_cart_part=1
		self.cog=30
		self.v12_engine=29
		self.coco_right=27
		self.pine=439
		self.gcbs=28
		self.anchovyfisher=31
		self.duckling=32
		self.eagle=33

		self.mayors_house=428
		self.church=429
		self.lighthouse=431
		self.house_1=430
		self.brewery=432
		self.stone_houses=[self.mayors_house,self.church,self.lighthouse,self.house_1,self.brewery]

		self.bush=433
		self.big_weeping_willow=434
		self.shrine= 439
		self.rock=435
		self.pine_tree=436
		self.cocoright=437
		self.cocoleft=438
t=Types()
class decr():
	def __init__(self,img,pos,anchor="bottomleft",colliderect=None,type_house=False):
		self.pos=list(pos)
		self.img=img
		if colliderect!=None:
			self.crect=pygame.Rect(*colliderect)
			game.world.wallrectlist.append(self.crect)
		elif type_house:
			self.crect=pygame.Rect([self.pos[0],self.pos[1]-24],(self.img.get_width(),24))
			game.world.wallrectlist.append(self.crect)
		try:
			self.rect=self.img.get_rect()
			self.size=self.img.get_size()
		except AttributeError:
			self.size=self.img.img.get_size()
			self.rect=self.img.img.get_rect()
		setattr(self.rect,anchor,self.pos)
		
		self.y_order=self.rect.midbottom[1]
		game.drawlist.append(self)
		game.world.assign_chunk(self,get_chunk_pos(self.pos))

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
class Wave():
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

class world():
	def __init__(self):
		self.gamemap=maps.create_world()
		self.obj_data=maps.get_obj_data()
		self.obj_derc_data=maps.get_derc_obj_data()
		self.layer1=self.gamemap[0]
		self.nonwallrectlist=[]
		self.tilelist=[]
		self.wallrectlist=[]
		self.nonstonewallwalllist=[]
		self.tilebackdecrolist=[]
		self.waterlist=[]
		self.placebridgelist=[]
		self.objs=[]
		self.chunks=[[]]
		self.chunksize=chunk_size
		for i in range(math.ceil(len(self.layer1)/self.chunksize[1])):
			self.chunks.append([])
		for y,row in enumerate(self.chunks):
			for x in range(math.ceil(len(self.layer1[1])/self.chunksize[0])):
				row.append(chunk([x,y]))
				
	def initother(self):
		y=0
		for row in self.layer1:
			x=0
			for tile in row:
				sheetpos=[0,0]
				if tile not in [0,3]:
					try:
						row[x-1]
					except IndexError:
						sheetpos[0]-=64
						if row[x+1] not in [0,3]:
							sheetpos[0]+=32
					else:
						try:
							row[x+1]
						except IndexError:
							sheetpos[0]=0
							if row[x-1] not in [0,3]:
								sheetpos[0]-=32
						else:
							if row[x-1] not in [0,3]:
								sheetpos[0]-=64
								if row[x+1] not in [0,3]:
									sheetpos[0]+=32
							if row[x+1] not in [0,3]:
								sheetpos[0]=0
								if row[x-1] not in [0,3]:
									sheetpos[0]-=32
					try:
						self.layer1[y-1]
					except IndexError:
						sheetpos[1]=0
						if self.layer1[y+1][x] not in [0,3]:
							sheetpos[1]-=32
					else:
						try:
							self.layer1[y+1]
						except IndexError:
							sheetpos[1]-=64
							if self.layer1[y-1][x] not in [0,3]:
								sheetpos[1]+=32
						else:
							if self.layer1[y-1][x] not in [0,3]:
								sheetpos[1]-=64
								if self.layer1[y+1][x] not in [0,3]:
									sheetpos[1]+=32
							if self.layer1[y+1][x] not in [0,3]:
								sheetpos[1]=0
								if self.layer1[y-1][x] not in [0,3]:
									sheetpos[1]-=32
				if tile==0:
					a=[]
					b=[]
					try:
						self.layer1[y-1]
					except IndexError:
						a.append(self.waterlist)
					else:
						if not self.layer1[y-1][x] in [1,2]:
							a.append(self.waterlist)
							b.append(self.wallrectlist)
					Tile(1,0,[x*32,y*32],lists=a,rectlists=b)
				elif tile==1:
					if sheetpos[1]==-64:
						Tile(0,1,[x*32,(y*32)+32],[sheetpos[0],0],lists=[self.tilebackdecrolist,self.nonstonewallwalllist],rectlists=[self.wallrectlist],img=image.woodpolesheet)
					Tile(1,1,[x*32,y*32],sheetpos,lists=[self.tilelist],rectlists=[self.nonwallrectlist],img=image.wooddecksheet)
				elif tile==2:
					Tile(1,2,[x*32,y*32],[sheetpos[0]-32,sheetpos[1]-32],lists=[self.tilelist,self.nonwallrectlist],img=image.grasssheet)
					if sheetpos[1]==-64:
						Tile(0,0,[x*32,(y*32)+32],[sheetpos[0]-32,-128],lists=[self.tilebackdecrolist,self.nonstonewallwalllist],rectlists=[self.wallrectlist],img=image.grasssheet)
					elif sheetpos[1]==0:
						Tile(0,0,[x*32,(y*32)-32],[sheetpos[0]-32,0],lists=[self.tilelist],img=image.grasssheet)
					if sheetpos[0]==-64:
						Tile(0,0,[x*32+32,y*32],[-128,sheetpos[1]-32],lists=[self.tilelist],img=image.grasssheet)
					elif sheetpos[0]==0:
						Tile(0,0,[x*32-32,y*32],[0,sheetpos[1]-32],lists=[self.tilelist],img=image.grasssheet)

				elif tile==3:
					Tile(1,3,[x*32,y*32],sheetpos=(0,16),lists=[self.tilelist],rectlists=[self.wallrectlist],img=image.wallbottom)
					Tile(2,1,[x*32,y*32-16],lists=[self.tilelist,game.drawlist])
					Tile(0,6,[x*32,y*32+32],lists=[self.tilebackdecrolist],img=image.true_wallbottom)
				elif tile==4:
					Tile(1,4,[x*32,y*32],lists=[self.tilelist],rectlists=[self.nonwallrectlist],img=image.placebridge,child=Tile(0,5,[x*32,y*32+32],lists=[self.tilebackdecrolist],sheetpos=(0,-32),img=image.placebridge))
				elif tile==5:
					Tile(1,5,[x*32,y*32],[sheetpos[0]-32,sheetpos[1]-32],lists=[self.tilelist],rectlists=[self.nonwallrectlist],img=image.snowgrasssheet)
					if sheetpos[1]==-64:
						Tile(0,2,[x*32,(y*32)+32],[sheetpos[0]-32,-128],lists=[self.tilebackdecrolist,self.nonstonewallwalllist],rectlists=[self.wallrectlist],img=image.snowgrasssheet)
					elif sheetpos[1]==0:
						Tile(0,2,[x*32,(y*32)-32],[sheetpos[0]-32,0],lists=[self.tilelist],img=image.snowgrasssheet)
					if sheetpos[0]==-64:
						Tile(0,2,[x*32+32,y*32],[-128,sheetpos[1]-32],lists=[self.tilelist],img=image.snowgrasssheet)
					elif sheetpos[0]==0:
						Tile(0,2,[x*32-32,y*32],[0,sheetpos[1]-32],lists=[self.tilelist],img=image.snowgrasssheet)
				elif tile==6:
					Tile(1,6,[x*32,y*32],[sheetpos[0]-32,sheetpos[1]-32],lists=[self.tilelist,self.nonwallrectlist],img=image.sandsheet)
					if sheetpos[1]==-64:
						Tile(0,4,[x*32,(y*32)+32],[sheetpos[0]-32,-128],lists=[self.tilebackdecrolist,self.nonstonewallwalllist],rectlists=[self.wallrectlist],img=image.sandsheet)
					elif sheetpos[1]==0:
						Tile(0,4,[x*32,(y*32)-32],[sheetpos[0]-32,0],lists=[self.tilelist],img=image.sandsheet)
					if sheetpos[0]==-64:
						Tile(0,4,[x*32+32,y*32],[-128,sheetpos[1]-32],lists=[self.tilelist],img=image.sandsheet)
					elif sheetpos[0]==0:
						Tile(0,4,[x*32-32,y*32],[0,sheetpos[1]-32],lists=[self.tilelist],img=image.sandsheet)
				x+=1
			y+=1
		for pos in game.save.read()["placebridge"]:
			a=Tile(1,4,pos,lists=[self.tilelist,self.placebridgelist],rectlists=[self.nonwallrectlist],img=image.placebridge,child=Tile(0,5,[pos[0],pos[1]+32],lists=[self.tilebackdecrolist],img=image.placebridge,sheetpos=(0,-32)))
			a.initother()
		for data in self.obj_data:
			#if data[0] in [27,28]:
			#	obj(data,lists=[game.drawlist])
			if data[0]==t.gcbs:
				npc(t.gcbs,data[1])
			elif data[0] in [t.v12_engine,t.cog]:
				npc(t.golf_cart_part,data[1],imgs={"engine":[image.v12_engine,(0,0)]} if data[0]==t.cog else {"cog":[image.cogs,(0,0)]})
			elif data[0]==t.anchovyfisher:
				npc(t.anchovyfisher,data[1])
			elif data[0]==t.duckling:
				npc(t.duckling,data[1])
			elif data[0]==t.eagle:
				npc(t.eagle,data[1])
			elif data[0]==t.shrine:
				npc(t.shrine,data[1])


		for data in self.obj_derc_data:
			if data[0] in t.stone_houses:
				dercv=decr(img:=image.objs[data[0]],data[1],type_house=True,colliderect=get_house_rect(img,20,init_pos=data[1]))
			elif data[0] == t.big_weeping_willow:
				dercv=decr(image.objs[data[0]],data[1],colliderect=get_house_rect(img,15,init_pos=(data[1])))
			else:
				dercv=decr(image.objs[data[0]],data[1])
				#chunk_pos
			c_p=get_chunk_pos(dercv.pos)
			self.chunks[c_p[1]][c_p[0]].decrlist.append(dercv)
	def assign_chunk(self,obj,pos,type="decr"):
		if type=="decr":
			self.chunks[pos[1]][pos[0]].decrlist.append(obj)
			try:
				obj.parent_chunk=self.chunks[pos[1]][pos[0]]
			except AttributeError:
				pass


class chunk():
	def __init__(self,pos):
		self.pos=pos
		self.nonwallrectlist=[]
		self.wallrectlist=[]
		self.nonstonewallwalllist=[]
		self.tilebackdecrolist=[]
		self.waterlist=[]
		self.decrlist=[]
		self.tiles=[]
		self.nodes=[]
		self.hitbox=pygame.Surface((chunk_size[0]*32,chunk_size[1]*32))
		self.hitbox.fill((random.random()*255,random.random()*255,0))
	def update(self):
		#for tilev in self.tiles:
		#	tilev.update()
		for node in self.nodes:
			node.update()
	def draw_tiles(self):
		for tile in self.tilebackdecrolist:
			tile.draw()
		for tilev in self.tiles:
			tilev.draw()

		screen.blit(self.hitbox,withscroll([self.pos[0]*32,self.pos[1]*32]))
	def draw_nodes(self):
		for node in self.nodes:
			node.draw()
	def draw_nodes_2(self):
		for node in self.nodes:
			node.draw2()
	def draw_nodes_fish(self):
		for node in self.nodes:
			node.draw_fish()
	def add_tiles(self,tiles):
		self.tiles+=tiles
	def add_node(self,node):
		self.node.append(node)

def obj(data,type=decr,lists=[],rectlists=[]):
	if type==decr:
		return decr(image.objs[data[0]],data[1])

	elif type==npc:
		return npc(data[0],data[1])
class Tile():
	def __init__(self,layer,type,pos:list,sheetpos=[0,0],size=[32,32],lists=[],rectlists=[],img:pygame.Surface=None,child=None):
		#layer 0, images e.g, cliff, waves (as decor)
		#layer 1, flooring, rickty bigde
		#layer 2, images e.g, tree (as decor)
		#layer 3, intractable
		self.colour=(randint(0,255),randint(0,255),randint(0,255))
		self.type=type
		self.img=pygame.Surface(size,pygame.SRCALPHA).convert_alpha()
		self.img.fill((0,0,0,0))
		self.layer=layer
		self.type=type
		self.pos=pos
		self.map_pos=[pos[0]/32,pos[1]/32]
		self.chunkpos=[math.floor(pos[0]/(32*game.world.chunksize[0])),math.floor(pos[1]/(32*game.world.chunksize[1]))]
		self.child=child
		if not game.world.tilebackdecrolist in lists:
			try:
				game.world.chunks[self.chunkpos[1]][self.chunkpos[0]].tiles.append(self)
			except IndexError:
				try:
					game.world.chunks[self.chunkpos[1]][len(game.world.chunks[0])].tiles.append(self)
				except IndexError:
					try:
						game.world.chunks[len(game.world.chunks)][self.chunkpos[0]].tiles.append(self)
					except IndexError:
						pass
		else:
			try:
				game.world.chunks[self.chunkpos[1]][self.chunkpos[0]].tilebackdecrolist.append(self)
			except IndexError:
				try:
					game.world.chunks[self.chunkpos[1]][len(game.world.chunks[0])].tilebackdecrolist.append(self)
				except IndexError:
					try:
						game.world.chunks[len(game.world.chunks)][self.chunkpos[0]].tilebackdecrolist.append(self)
					except IndexError:
						pass


		if layer==1:
			#type 1, deck
			#type 0, water
			#type 2, grass
			#type 3, wall(collide)
			#type 4, rickty bridge
			#type 5, snow grass
			#type 6, sand
			if type==4:
				self.overtaken=None
		elif layer==2:
			if type==1:
				self.img.blit(image.wall)
				game.world.assign_chunk(self,get_chunk_pos(self.pos))
		if img !=None:
			self.img.blit(img,sheetpos)
		self.rect=pygame.rect.Rect(self.pos,size)
		self.y_order=self.rect.midbottom[1]
		self.lists=lists
		self.rectlists=rectlists
		for list_ in lists:
			list_.append(self)
		for list_ in rectlists:
			list_.append(self.rect)

	def update(self):
		pass
	def initother(self):
		if self.layer==1:
			if self.type==4:
				a=[(water.map_pos,water) for water in game.world.waterlist]+[(tilec.map_pos,tilec) for tilec in game.world.nonstonewallwalllist]
				for pos,water in a:
					if pos==self.map_pos:
						try:
							game.world.nonstonewallwalllist.remove(water)
						except ValueError:
							pass
						try:
							game.world.wallrectlist.remove(water.rect)
						except ValueError:
							pass
						self.overtaken=water
						return None
		
	def pop(self):
		for list_ in self.lists:
			try:
				list_.remove(self)
			except ValueError:
				pass
		for list_ in self.rectlists:
			try:
				list_.remove(self)
			except ValueError:
				pass
		try:
			game.world.chunks[self.chunkpos[1]][self.chunkpos[0]].tiles.remove(self)
		except ValueError:
			try:
				game.world.chunks[self.chunkpos[1]][self.chunkpos[0]].tilebackdecrolist.remove(self)
			except ValueError:
				pass
		if self.overtaken!=None:
			for list_  in self.overtaken.lists:
				if self.overtaken not in list_:
					list_.append(self)
			for list_  in self.overtaken.rectlists:
				if self.overtaken not in list_:
					list_.append(self)
		try:
			self.child.pop()
		except AttributeError:
			pass
		del self

	def draw(self):
		screen.blit(self.img,(self.pos[0]+game.scroll[0],self.pos[1]+game.scroll[1]))
	#	pygame.draw.rect(screen,self.colour,self.rect)


def pallette_swap(surf,old,new,alpha_key=(0,0,0)):
	s=pygame.Surface(surf.get_size())
	s.fill(new)
	s2=pygame.Surface(surf.get_size())
	s2.fill(alpha_key)
	s2.blit(surf)
	s2.set_colorkey(old)
	s.blit(s2)
	s.set_colorkey(alpha_key)
	return s
def pallettes_swap(surf,colour_pairs,alpha_key_=(0,0,0)):
	for c,d in colour_pairs:
		surf=pallette_swap(surf,c,d,alpha_key=alpha_key_)
	return surf
class Tutorial():
	def __init__(self):
		self.tutorials_shown=game.save.read()["tutorials_shown"]#{"speed tech":["bhop"]*90}
		#self.change(["woah"]*90)
		self.delay_args={
		"text":[],
		"name":None,
		"reshow":False
		}
		self.start_change=False
		self.delay=60
		self.delay_timer=timer(int(self.delay))

	def change(self,text,name=None,reshow=False):
		try:
			game.change_stage("tutorial") #if game.stage!="tutorial" else game.change_stage("play")
		except NameError:
			pass
		if name in self.tutorials_shown.keys() and not reshow:
			game.change_stage(game.last_stage)
			return "woah"

		elif name != None:
			self.tutorials_shown[name]=text
			self.current_tutorial=name
		else:
			self.current_tutorial=None
		self.para=Para(text)
		self.bg=image.tutorial
		bg_rect=self.bg.get_rect(center=(screen_width/2,screen_height/2))
		self.bg_draw_pos=bg_rect.topleft
		self.para_pos=center_surf(self.para.img)
		self.exit_size=(11,11)
		self.exit_y_max=40
		self.exit_img=image.exit_button.copy()
		self.exit_pos=center_surf(self.exit_img)
		self.exit_pos[1]+=min(self.para.img.get_height()+10+self.exit_size[1],self.exit_y_max)
		self.exit=Button(self.exit_img,self.exit_pos)
	def update(self):
		self.exit.update()
		
		if self.exit.pressed:
			game.tutorial_menu.add_tutorial(self.current_tutorial)
			game.change_stage("tutorial") if game.last_stage=="tutorial" else game.change_stage(game.last_stage)
			#game.tutorial_menu.tutorial_buttons[self.current_tutorial]=Button(text.render(self.current_tutorial),)
	def always_update(self):
		if self.start_change:
			self.delay_timer.update()
			if self.delay_timer.tick:
				self.start_change=False
				self.change(*self.delay_args.values())
	def draw(self):
		screen.blit(self.bg,self.bg_draw_pos)
		self.exit.draw()
		screen.blit(self.para.img,self.para_pos)
	def delay_change(self,text,name=None,reshow=False,delay=60):
		self.delay_args={
		"text":text,
		"name":name,
		"reshow":reshow
		}
		print(self.delay_args)
		self.delay_timer=timer(int(delay))
		self.delay=60
		self.start_change=True

class Tutorial_menu():
	def __init__(self):
		self.tutorial=game.tutorial
		self.tutorials_shown=self.tutorial.tutorials_shown
		self.tutorial_buttons={}
		self.offset=[7,8]
		self.dist=8
		for i,key in enumerate(self.tutorials_shown.keys()):
			self.tutorial_buttons[key]=Button(text.render(key),[self.offset[0],self.offset[1]+i*self.dist])
	#def get_tutorials(self):
	#	self.__init__()
	def add_tutorial(self,name):
		if name == None:
			return "no"
		self.tutorial_buttons[name]=Button(text.render(name),[self.offset[0],self.offset[1]+len(self.tutorial_buttons)*self.dist])
	def update(self):
		for key,button in self.tutorial_buttons.items():
			button.update()
			if button.pressed:
				self.tutorial.change(self.tutorials_shown[key],reshow=True)
	def draw(self):
		screen.blit(image.tutorial,(0,0))
		for button in self.tutorial_buttons.values():
			button.draw()
class images():
	def __init__(self):
		self.iconpleasework=pygame.image.load("imgs/icon.png").convert_alpha()

		self.bigfish=pygame.image.load("imgs/fish.png").convert_alpha()
		self.anchovy=pygame.image.load("imgs/anchovy.png").convert_alpha()
		self.sardine=pygame.image.load("imgs/sardine.png").convert_alpha()
		self.bass=pygame.image.load("imgs/bass.png").convert_alpha()
		self.chub_mackerel=pygame.image.load("imgs/chub mackerel.png").convert_alpha()
		self.pink_rockling=pygame.image.load("imgs/pink rockling.png").convert_alpha()
		self.rockling=pygame.image.load("imgs/rockling.png").convert_alpha()
		self.pink_salmon=pygame.image.load("imgs/pink salmon.png").convert_alpha()
		self.duckfish=pygame.image.load("imgs/duck fish.png").convert_alpha()
		self.yellow_perch=pygame.image.load("imgs/yellow perch.png").convert_alpha()
		self.black_marlin=pygame.image.load("imgs/black marlin.png").convert_alpha()

		self.copper=pygame.image.load("imgs/coin.png").convert_alpha()
		self.mallet=pygame.image.load("imgs/mallet.png").convert_alpha()
		self.yellow_mold=pygame.image.load("imgs/yellow mold.png").convert_alpha()
		self.rotting_wood=pygame.image.load("imgs/rotting wood.png").convert_alpha()

		self.stonesheet=pygame.image.load("imgs/stone houses.png")
		self.house_1=get_surf_from_sheet(self.stonesheet,(-184,-85),(143,96))
		self.mayors_house=get_surf_from_sheet(self.stonesheet,(0,0),(184,181))
		self.church=get_surf_from_sheet(self.stonesheet,(0,-181),(222,181))
		self.lighthouse=get_surf_from_sheet(self.stonesheet,(-222,-181),(74,181))
		self.brewery=get_surf_from_sheet(self.stonesheet,(-331,-184),(163,84))


		self.playersheet=pygame.image.load("imgs/new duck.png").convert_alpha()
		self.wooddecksheet=pygame.image.load("imgs/wooddeck.png").convert()
		self.woodpolesheet=pygame.image.load("imgs/pole.png").convert_alpha()
		self.grasssheet=pygame.image.load("imgs/new grass.png").convert_alpha()
		self.snowgrasssheet=pygame.image.load("imgs/snowgrass.png").convert_alpha()
		self.sandsheet=pygame.image.load("imgs/sand.png").convert_alpha()
		self.placebridge=pygame.image.load("imgs/rickty bridge.png").convert_alpha()
		self.placebridgeicon=pygame.transform.scale(get_surf_from_sheet(self.placebridge,(0,0),(32,32)),(16,16))
		self.coconut_tree=pygame.image.load("imgs/coconut tree.png").convert_alpha()
		self.flip_coco=pygame.transform.flip(self.coconut_tree,True,False)
		self.trees_sheet=pygame.image.load("imgs/trees.png").convert_alpha()
		self.pine_tree=get_surf_from_sheet(self.trees_sheet,(-90,0),(32,64))
		self.weeping_willow_sheet=pygame.image.load("imgs/very big.png").convert_alpha()
		self.big_weeping_willow=self.weeping_willow_sheet#get_surf_from_sheet(self.weeping_willow_sheet,(-47,-35),(73,81))
		self.shrine=pygame.image.load("imgs/shrine 2.png").convert_alpha()
		self.bush=pygame.image.load("imgs/bush.png").convert_alpha()
		self.rock=pygame.image.load("imgs/rock 2.png").convert_alpha()

		self.wall=pygame.image.load("imgs/wall.png").convert_alpha()
		self.wallbottom=pygame.image.load("imgs/wall bottom.png").convert_alpha()
		self.true_wallbottom=pygame.image.load("imgs/wall truebottom.png").convert_alpha()
		self.splashsheet=pygame.image.load("imgs/splash.png").convert_alpha()
		self.wave=pygame.image.load("imgs/wave.png").convert_alpha()

		self.chicken=pygame.image.load("imgs/chicken.png").convert_alpha()
		self.stallsheet=pygame.image.load("imgs/stall.png").convert_alpha()

		self.crow=pygame.image.load("imgs/crow.png")
		self.gcbs_sheet=pygame.image.load("imgs/gcbs.png")
		self.golf_cart_part=pygame.image.load("imgs/golf cart part.png").convert_alpha()
		self.golf_cart=pygame.image.load("imgs/golf cart.png").convert_alpha()
		self.v12_engine=pygame.image.load("imgs/v12 engine.png").convert_alpha()
		self.cogs=pygame.image.load("imgs/cog.png").convert_alpha()
		self.golf_cart_no_duck=pygame.image.load("imgs/golf cart no duck.png").convert_alpha()
		self.npcsheet=pygame.image.load("imgs/npcs.png").convert_alpha()
		self.duckling=get_surf_from_sheet(self.npcsheet,(0,0),(16,14))
		self.duck=get_surf_from_sheet(self.npcsheet,(-16,0),(33,22))
		self.eagle=get_surf_from_sheet(self.npcsheet,(-13,-36),(23,31))

		self.lampsheet=pygame.image.load("imgs/lamp.png").convert_alpha()
		self.etotalk=pygame.image.load("imgs/e to talk.png").convert_alpha()
		self.etointeract=pygame.image.load("imgs/e to interact.png").convert_alpha()
		self.etodothings=pygame.image.load("imgs/e to do things.png").convert_alpha()
		self.etorefill=get_surf_from_sheet(self.etodothings,(0,0),(50,11))
		self.responsebox=pygame.image.load("imgs/rbox.png").convert_alpha()
		self.textbox=pygame.image.load("imgs/diabox.png").convert_alpha()
		self.textsheet=pygame.image.load("imgs/letters.png").convert_alpha()
		self.smalltextsheet=pygame.image.load("imgs/6x5 letters.png").convert_alpha()
		self.inventory=pygame.image.load("imgs/invetory.png").convert_alpha()
		self.tutorial=pygame.image.load("imgs/tut.png").convert_alpha()
		self.exit_button=pygame.image.load("imgs/exit button.png").convert_alpha()
		self.sellbuttons=pygame.image.load("imgs/sell buttons.png").convert_alpha()

		self.player_icon_sheet=pygame.image.load("imgs/player loc.png").convert_alpha()
		self.objs={
		t.coco_right:self.flip_coco,
	#	t.coco_left:self.coconut_tree,
		t.pine:self.pine_tree,
		t.gcbs:self.crow,
		t.house_1:self.house_1,
		t.mayors_house:self.mayors_house,
		t.church:self.church,
		t.lighthouse:self.lighthouse,
		t.brewery:self.brewery,
		t.bush:self.bush,
		t.big_weeping_willow:self.big_weeping_willow,
		t.rock:self.rock,
		t.pine_tree:self.pine_tree,
		t.cocoleft:self.coconut_tree,
		t.cocoright:self.flip_coco,
		t.shrine:self.shrine

		}
	def add(self,name,path):
		setattr(self,name, pygame.image.load(path).convert_alpha())

image=images()
pygame.display.set_icon(image.iconpleasework)
pygame.display.set_icon(pygame.image.load("imgs/icon.png").convert_alpha())
class animation():
	def __init__(self,image,size:list,delay:int,frame=0):
		self.delay=delay
		self.timer=0
		self.frames=image
		self.frame=frame
		self.size=size
		self.img=pygame.Surface(size,pygame.SRCALPHA)
		self.img.fill((0,0,0,0))
		if type(image) in [list,tuple]:
			for itemv in image:
				if type(itemv) is not pygame.Surface:
					raise ValueError("image list/tuple contains non pygame.Surface object(s)")
			self.type="list"
			self.frames_amount=len(self.frames)
		elif type(image) is pygame.Surface:
			self.img.blit(self.frames)
			self.type="sheet"
			length=self.frames.get_width()
			self.frames_amount=length/self.size[0]
		else:
			raise ValueError("argument, image, is not a pygame.Surface or list object")
	def update(self):
		self.timer+=1
		if self.timer>=self.delay:
			if self.type=="sheet":
				self.timer=0
				self.frame+=1
				self.frame%=self.frames_amount
				self.img.fill((0,0,0,0))
				self.img.blit(self.frames,(self.frame*-self.size[0],0))			
			else:
				self.timer=0
				self.frame+=1
				self.frame%=self.frames_amount
				self.img.fill((0,0,0,0))
				self.img.blit(self.frames[frame],(0,0))			
	def draw(self,pos=(0,0)):
		screen.blit(self.img,pos)
	def jumpto(self,frame):
		self.frame=frame
		self.frame%=self.frames_amount+1
		self.img.fill((0,0,0,0))
		self.img.blit(self.frames,(self.frame*-self.size[0],0))			
class Particle:
	def __init__(self
			,size:float or int
			,angle: float or int 
			,pos:list
			,totalspeed=10
			,colour=(255,255,255)
			,gravity=0.5
			,lifeloss=0.5
			,staticspeed=[0,0]
			,alphaloss=0
			,alpha=255
			,blendflag=pygame.BLENDMODE_NONE
			):
		self.pos=list(pos)
		self.angle=math.radians(angle)
		self.size=size
		self.totalspeed=totalspeed
		self.staticspeed=list(staticspeed)
		self.colour=colour
		self.alpha=alpha
		self.flag=blendflag
		self.gravity=gravity
		self.lifeloss=lifeloss
		self.alphaloss=alphaloss
		self.img=pygame.Surface((size*2,size*2),pygame.SRCALPHA)
		game.particles.append(self)
	def update(self):
		self.staticspeed[0]*=0.95
		self.staticspeed[1]*=0.95
		self.totalspeed*=0.98
		self.size-=self.lifeloss
		self.staticspeed[1]+=self.gravity
		self.pos[0]+=math.sin(self.angle)*self.totalspeed
		self.pos[1]+=math.cos(self.angle)*self.totalspeed
		self.pos[0]+=self.staticspeed[0]
		self.pos[1]+=self.staticspeed[1]
		self.img=pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
		self.img.fill((0,0,0,0))
		pygame.draw.circle(self.img,self.colour,(self.size,self.size),self.size)
		self.alpha-=self.alphaloss
		self.img.set_alpha(self.alpha)
		
		if self.size<=0 or self.alpha<=0:
			game.particles.remove(self)
			del self
			return None
	def draw(self):
		screen.blit(self.img,withscroll([self.pos[0]-self.size,self.pos[1]-self.size]),special_flags=self.flag)

class text():
    def __init__(self):
        self.letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0",".","!",",","?","+","-","'","[","]",":","/","%"]
    def render(self,text,letter_size=[6,5],sheet=image.smalltextsheet):
        digit=-1
        textsurf=pygame.Surface((len(text)*letter_size[0],letter_size[1]),flags=pygame.SRCALPHA).convert_alpha()
        img=pygame.Surface((letter_size[0],letter_size[1]),flags=pygame.SRCALPHA).convert_alpha()
        for letter in text:
            digit+=1
            try:
                frame=self.letters.index(letter)
            except ValueError:
                frame=-1
            img.fill((0,0,0,0))
            img.blit(sheet,((1-(frame*letter_size[0])),0))
            textsurf.blit(img,(digit*letter_size[0],0))
        return textsurf
text=text()
class Para():
	def __init__(self,text_:list,height=6,width=7):
		self.text=text_
		if text_==[]:
			self.para=pygame.Surface((1,1),pygame.SRCALPHA).convert_alpha()
		else:
			self.para=pygame.Surface((max(len(line) for line in text_)*height,len(text_)*height),pygame.SRCALPHA).convert_alpha()
		self.para.fill((0,0,0,0))
		for y in range(len(text_)):
				self.para.blit(text.render(str(self.text[y])),(0,y*height))
		self.img=self.para
def str_to_para(str_,size:int):
	return [str_[(i-1)*size:i*size] for i in range(1,math.ceil(len(str_)/size)+1)]


class Notice():
	def __init__(self,textv:str,image=None,begin=True):
		game.notice_board.notices.append(self)
		self.strtext=textv
		self.img=image
		if self.img==None:
			self.img=pygame.Surface((0,0))
		self.textsurf=text.render(self.strtext)
		self.noticesurf=pygame.Surface((self.textsurf.get_width()+self.img.get_width()+5,max(self.textsurf.get_height(),self.img.get_height()) ),pygame.SRCALPHA).convert_alpha()
		self.noticesurf.fill((0,0,0,0))
		self.noticesurf.blit(self.textsurf,(0,self.noticesurf.get_height()/2-self.textsurf.get_height()/2))
		self.noticesurf.blit(self.img,(self.textsurf.get_width()+1,0))
		self.fade=pygame.Surface(self.noticesurf.get_size(),pygame.SRCALPHA).convert_alpha()
		self.fade.fill((0,0,0,255/180))
		self.begindel=begin
		self.place=0
		self.timer=0
	def update(self):
		qwfx=-1
		for itemv in game.notice_board.notices:
			qwfx+=1
			if itemv==self:
				break
		self.place=qwfx
		if self.begindel==True:
			
			self.timer+=1
			if self.timer>=180:
				self.noticesurf.blit(self.fade,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
				if self.timer>=360:
					game.notice_board.notices.remove(self)
					del self

	def draw(self):
		screen.blit(self.noticesurf,(0,(self.place)*12+1))
class Notification_Center():
	def __init__(self):
		self.notices=[]
		self.amount=len(self.notices)
	def update(self):
		self.amount=len(self.notices)
		for notice in self.notices:
			notice.update()
	def draw(self):
		for notice in self.notices:
			notice.draw()


def controller(flag="key"):
	key = pygame.key.get_pressed()
	mouse=pygame.mouse.get_pressed()
	if flag=="key":
		return key
	elif flag=="mouse":
		return mouse
	elif flag=="all":
		return [key,mouse]
	else:
		return None

class fishingnode():
	def __init__(self,pos:list,density:list,range_=4,respawn_rate=60,fish_limit=5,regen=300):
		self.pos=pos
		self.density=density#init amount
		self.truedensity=dict(density)#current amount
		self.fishs=[]
		self.remove_fishs=[]
		self.range=range_
		self.fish_limit=fish_limit
		self.sin=Sin(0.01,7,start=random.random()*math.pi*7)
		self.sin2=Sin(0.007,12,start=random.random()*math.pi*12)
		self.timer=timer(respawn_rate)
		self.regen_timer=timer(regen)
		game.nodelist.append(self)
	def initother(self,density):
		self.truedensity=dict(density)
	def add_fish(self):
		a=random.random()*sum(self.density.values())
		fish=[0,0]
		for f in self.density:
			fish[0]+=self.density[f]
			if fish[0]>a>fish[1]:
				self.truedensity[f]=min(self.truedensity[f]+1,self.density[f])
				return None
			fish[1]=fish[0]
	def update(self):
		self.timer.update()
		self.regen_timer.update()
		if self.regen_timer.tick:
			self.add_fish()
		if self.timer.tick:
			if len(self.fishs)<self.fish_limit:
				angle=random.random()*math.pi*2
				key=dict_choice(self.truedensity)
				if key!=None:
					ran=random.random()
					Fish(add_poses(self.pos,[math.cos(angle)*self.range*32*ran,math.sin(angle)*self.range*32*ran]),node=self,type=key)
					self.truedensity[key]-=1
		for fish in self.fishs:
			fish.update()
		self.fishs=[fish for fish in self.fishs if not fish in self.remove_fishs]
		self.remove_fishs=[]
	#def spawn_fish(self,fish):
	#	if fish==""
	def draw(self):
		self.sin.update()
		pygame.draw.circle(screen,(40,90,190),withscroll(self.pos),self.range*32+self.sin.val-self.sin.height-10)
	def draw2(self):
		self.sin2.update()
		pygame.draw.circle(screen,(45,95,200),withscroll(self.pos),self.range*32+self.sin2.val-self.sin2.height+10)
	def draw_fish(self):
		for fish in self.fishs:
			fish.draw()
	def get_all_fish(self):
		fishies=Counter([fish.type for fish in self.fishs])
		fishies.update(Counter(self.truedensity))
		return dict(fishies)


class Fish():
	def __init__(self,pos,size=7,range_=40,run_speed=0.5,interval=600,type="duckfish",node:fishingnode=None,attraction_speed=0.7):
		self.pos=list(pos)
		self.size=float(size)
		self.ogsize=float(size)
		self.range=float(range_)
		self.run_speed=float(run_speed)
		self.dest=(self.pos[0]+(random.random()*self.run_speed*120)-self.run_speed*60,
					self.pos[1]+(random.random()*self.run_speed*120)-self.run_speed*60
					)		
		self.dest_angle=math.atan2(-(self.pos[1]-self.dest[1]),self.pos[0]-self.dest[0])
		self.timer=timer(interval)
		self.return_timer=timer(5)
		self.touch_timer=timer(60)
		self.curve_mult=curve_mult()
		self.type=type
		self.attraction_speed=attraction_speed
		game.fishs.append(self)
		self.node=node
		if node!=None:
			node.fishs.append(self)
	def update(self):

		self.timer.update()
		self.curve_mult.update()

		if self.timer.tick or get_dist(self.dest,self.pos)<6:
			self.curve_mult.reset()
			self.return_timer.update()
			if not self.return_timer.tick:
				self.dest=(self.pos[0]+random.random()*self.run_speed*120-self.run_speed*60,
						self.pos[1]+random.random()*self.run_speed*120-self.run_speed*60
						)
				self.dest_angle=math.atan2(-(self.pos[1]-self.dest[1]),self.pos[0]-self.dest[0])
			else:
				
				self.dest=add_poses(list(self.node.pos),(self.node.range*32*(random.random()-0.5),self.node.range*32*(random.random()-0.5)))
				self.dest_angle=math.atan2(-(self.pos[1]-self.dest[1]),self.pos[0]-self.dest[0])
		if get_dist(self.pos,game.player.fishingline.line[1])<=self.size and game.player.fishingline.landed:
			
			if self.touch_timer.timer<=15:
				self.touch_timer.update()
			elif c.mouse[0][0]==True and self.touch_timer.timer>=15:
				self.pop()
			if self.touch_timer.timer>=15:
				self.size=self.ogsize+2
		elif get_dist(self.pos,game.player.fishingline.line[1])<=self.size+self.range and game.player.fishingline.landed:
			angle=math.atan2((game.player.fishingline.line[1][1]-self.pos[1]),game.player.fishingline.line[1][0]-self.pos[0])
			self.pos[0]+=math.cos(angle)*self.attraction_speed*self.range/get_dist(self.pos,game.player.fishingline.line[1])/4
			self.pos[1]+=math.sin(angle)*self.attraction_speed*self.range/get_dist(self.pos,game.player.fishingline.line[1])/4
		else:
			self.touch_timer.reset()
		if self.touch_timer.timer<=15:
			self.pos[0]+=((math.cos(self.dest_angle))*(-self.curve_mult.val-0.5))*self.run_speed/4
			self.pos[1]-=((math.sin(self.dest_angle))*(-self.curve_mult.val-0.5))*self.run_speed/4
			self.size=self.ogsize
	def draw(self):
		pygame.draw.circle(screen,(20,65,170),withscroll(self.pos),self.size)
		#screen.set_at(withscroll(self.dest),(255,0,255))
	def pop(self):
		game.sell_tutorial()
		game.player.add_inventory(self.type,1,with_notice=True)
		self.node.remove_fishs.append(self)


class rope():
	def __init__(self,pos_start:list,speed:list):
		self.speed=speed
		self.splash=animation(image.splashsheet,[15,15],10,0)
		self.sin=0
		self.sinx=0
		self.line=[pos_start,pos_start]
		self.truey=self.line[1][1]
		self.landed=False
	def update(self):
		if self.parent.fishingtimer<=90:
			self.speed[1]+=0.1
			self.speed[0]+=0
			self.line[1][0]+=self.speed[0]
			self.line[1][1]+=self.speed[1]
			self.truey=self.line[1][1]
		elif self.parent.fishon==False:
			self.line[1][1]=self.truey
			self.sinx+=0.01
			self.sin=math.sin(self.sinx)*2+math.sin(self.sinx/2)*2
			self.line[1][1]=self.sin+self.truey
		else:
			self.line[1][1]=self.truey
		self.landed=True if self.parent.fishingtimer>90 and self.parent.fishing else False
	def draw(self):
		pygame.draw.line(screen,(255,255,255),(self.line[0][0]+game.scroll[0],self.line[0][1]+game.scroll[1]),(self.line[1][0]+game.scroll[0],self.line[1][1]+game.scroll[1]))
	def reinit(self,pos_start:list,speed:list):
		self.splash.jumpto(0)
		self.speed=speed 
		self.line=[list(pos_start),list(pos_start)]
		self.parent=game.player
class Golf_cart():
	def __init__(self):
		self.fuel=game.save.read()["golf cart"]["fuel"]
		self.max_fuel=36000
		self.rate=5
		self.accel=0.13
		self.maxspeed=100
		self.fric=0.965
		self.no_duck_fric=0.98
		self.pos=game.save.read()["golf cart"]["pos"]
		self.speed=[0,0]
		self.img=image.golf_cart
		self.disimg=self.img
		self.no_duck_img=image.golf_cart_no_duck
		self.rect=self.img.get_rect(topleft=self.pos)
		self.rect.height=20
		self.rect.width=30
		self.y_order=self.rect.midbottom[1]
		self.bar=frontdecr(None,None,init=frontdecr.init_golf_cart_bar,method=frontdecr.golf_cart_bar_update,draw_method=frontdecr.golf_cart_bar_draw,parent=self)
		self.set_max_speed()
		self.level=0
		#self.upgrade("fric",0.999,set_=True)
	def update(self):
		self.moving=False
		self.moving=self.controller_move() if game.player.golfcarting and self.fuel>=0 else False
		if self.max_fuel/2+60>self.fuel>self.max_fuel/2:
			game.tutorial.delay_change(["to refuel your golf cart, hold a","fish out and press [e] near the","golf cart"],"refuelling")
		self.fuel-=self.rate if game.player.golfcarting and self.moving else 0
		self.bar.update()
		self.bar.make_show(True) if game.player.golfcarting else self.bar.make_show(False)
		sign=[sign_of(self.speed[0]),sign_of(self.speed[1])]
		collidelist=game.world.wallrectlist

		self.pos[0]+=round(self.speed[0]*10)/10
		self.speed[0]*=self.fric if game.player.golfcarting else self.no_duck_fric
		self.speed[0]=min(abs(self.speed[0]),self.maxspeed)*sign[0]
		self.rect.x=self.pos[0]+13
		
		rect_index=self.rect.collidelist(collidelist)
		if rect_index!=-1:
			if self.speed[0]<0:
				for i in range(math.ceil(abs(self.speed[0]))):
					self.pos[0]+=1
					self.rect.x+=1
					if self.rect.collidelist(collidelist)==-1:
						break
			elif self.speed[0]>0:
				for i in range(math.ceil(self.speed[0])):
					self.pos[0]-=1
					self.rect.x-=1
					if self.rect.collidelist(collidelist)==-1:
						break
			self.speed[0]=0
		self.pos[1]+=round(self.speed[1]*10)/10
		self.speed[1]*=self.fric if game.player.golfcarting else self.no_duck_fric
		self.speed[1]=min(abs(self.speed[1]),self.maxspeed)*sign[1]
		self.rect.y=self.pos[1]+38

		rect_index=self.rect.collidelist(collidelist)
		if rect_index!=-1:
			if self.speed[1]<0:
				for i in range(math.ceil(abs(self.speed[1]))):
					self.pos[1]+=1
					self.rect.y+=1
					if self.rect.collidelist(collidelist)==-1:
						break
			elif self.speed[1]>0:
				for i in range(math.ceil(self.speed[1])):
					self.pos[1]-=1
					self.rect.y-=1	
					if self.rect.collidelist(collidelist)==-1:
						break
			self.speed[1]=0

		if not game.player.golfcarting:
			self.disimg=self.no_duck_img
		else:
			if c.key["d"][0]==True:
				self.disimg=pygame.transform.flip(self.img,True,False)
			elif c.key["a"][0]==True:
				self.disimg=self.img
		self.y_order=self.rect.midbottom[1]
		if c.otherkey["e"]==[True,False]:
				if game.player.held==None:
					self.seat_duck()
				else:
					try:
						o_f=int(self.fuel) #stands for orignal fuel
						self.fuel=min(game.fuel_info[game.player.held]+self.fuel,self.max_fuel)
						Notice(f"refilled for {self.fuel-o_f}")
						Notice(f"-1 {game.player.held}",getattr(image,game.player.held))
						game.player.add_inventory(game.player.held,-1)
						game.player.unhold_item()
					except KeyError as e:
						self.seat_duck()

	def seat_duck(self):
		close=True if not game.player.golfcarting and get_dist(game.player.rect.center,game.golf_cart.rect.center)<=60 else False
		game.player.golfcarting=close
		game.golf_cart.set_img(game.golf_cart.img) if close else None
	def go_to(self,midbottom):
		self.rect.midbottom=midbottom
		self.pos=list(self.rect.topleft)
	def set_max_speed(self,iterations=120):
		speed=0
		for i in range(iterations):
			speed+=self.accel
			speed*=self.fric
		self.maxspeed=math.floor(speed)
	def controller_move(self):
		if c.pkey["w"]:
			self.speed[1]-=self.accel
		if c.pkey["s"]:
			self.speed[1]+=self.accel
		if c.pkey["a"]:
			self.speed[0]-=self.accel
		if c.pkey["d"]:
			self.speed[0]+=self.accel
		if True in list(c.pkey.values()):
			return True 
		else: 
			return False

	def set_img(self,img):
		self.disimg=img
	def upgrade(self,stat_str:str,amount:int,set_=False):
		if set_:
			setattr(self,stat_str,amount)
		else:
			setattr(self,stat_str,getattr(self,stat_str)+amount)
		if stat_str in ["accel","fric"]:
			self.set_max_speed(240)
		
	def levelup(self):
		self.level+=1
		info=game.upgrade_info["info"][self.level-1]
		self.upgrade(info[0],info[1],True)
	def respawn(self):
		self.pos=list(game.player.pos)
	def draw(self):
		screen.blit(self.disimg,withscroll(self.pos))
class Button():
	def __init__(self,img,screen_pos,rect:pygame.Rect=None):
		self.img=img
		self.pos=screen_pos
		self.rect=self.img.get_rect(topleft=self.pos) if rect==None else rect
		self.hover=pygame.Surface(self.img.get_size(),pygame.SRCALPHA).convert_alpha()
		self.hover.fill((0,0,0,32))
		self.m_hover_and_down=False
		self.m_hover=False
		self.pressed=False
	def update(self):
		m_pos=mouse_get_pos()
		self.pressed=False
		if self.rect.collidepoint(m_pos):
			self.m_hover=True
			if c.mouse[0]==[True,False]:
				self.m_hover_and_down=True
		else:
			self.m_hover_and_down=False
			self.m_hover=False
		if self.m_hover_and_down:
			if c.mouse[0]==[False,True] and self.rect.collidepoint(m_pos):
				self.pressed=True
	def draw(self):
		screen.blit(self.img,self.pos)
		screen.blit(self.hover,self.pos) if self.m_hover else None 
		screen.blit(self.hover,self.pos) if self.m_hover_and_down else None 
		screen.blit(self.hover,self.pos) if self.pressed else None 


class inventory():
	def __init__(self):
		self.back=image.inventory
		self.item_surf=pygame.Surface((512,1000),pygame.SRCALPHA).convert_alpha()
		self.item_img=pygame.Surface((111,106),pygame.SRCALPHA).convert_alpha()
		self.window_rect=pygame.Rect((6,6),(111,106))
		self.descrp_img=pygame.Surface((108,106),pygame.SRCALPHA).convert_alpha()
		self.itemtypes=list(game.player.inventory.keys())
		self.fishtypes=list(game.sellinfo["fish"].keys())
		self.items={}
		descrps=file("jsons/fishopedia.json")
		self.descrps={key: Para(descrps.read()[key]) for key in descrps.read()}
		self.costs={key: str(game.sellinfo[key]) for key in game.sellinfo}
		self.selected=None
		self.selected_box=[0,0]
		self.hover_box=[0,0]
		self.sellboxs={
		"1":{"img":get_surf_from_sheet(image.sellbuttons,(0,-11),(23,11)),"rect":pygame.Rect((123,100),(23,11))},
		"50%":{"img":get_surf_from_sheet(image.sellbuttons,(0,-22),(23,11)),"rect":pygame.Rect((148,100),(23,11))},
		"all":{"img":get_surf_from_sheet(image.sellbuttons,(0,0),(23,11)),"rect":pygame.Rect((173,100),(23,11))}
		}
		self.hold_box=Button(get_surf_from_sheet(image.sellbuttons,(0,-33),(23,11)),(198,100))
		self.parent=game.player
		self.mouse=[False,False]
		self.offset=[0,0]
		self.mdownrect=None
		self.last_held="duckfish"
	def refresh(self):
		self.item_surf.fill((0,0,0,0))
		x=0
		for type in game.player.inventory:
			fish=self.parent.inventory[type]
			if fish!=0 or self.parent.total[type]:
				textv=text.render(f"{type}:{fish}")
				#textv=text.render(f"{fish}:")
				img=getattr(image,type)
				if type =="placebridge":
					img=pygame.Surface((16,16),pygame.SRCALPHA).convert_alpha()
					img.blit(pygame.transform.scale(getattr(image,type),(16,32)))
				itemsurf=pygame.Surface((textv.get_width()+img.get_width()+2,max(textv.get_height(),img.get_height())+1),pygame.SRCALPHA).convert_alpha()
				itemsurf.fill((0,0,0,0))

				itemsurf.blit(img,(textv.get_width()+1,itemsurf.get_height()/2-img.get_height()/2))
				itemsurf.blit(textv,(0,itemsurf.get_height()/2-textv.get_height()/2))

				#itemsurf=pygame.Surface((img.get_width()+2,img.get_height()+1),pygame.SRCALPHA).convert_alpha()
				#itemsurf.blit(img,(1,0))

				itemrect=itemsurf.get_rect(topleft=(7,x*16+7))
				self.items.update({type:{"rect":itemrect,"img":itemsurf}})
				x+=1
	def refresh_descrp(self,type_:str):
		para=self.descrps[type_]
		self.descrp_img.fill((0,0,0,0))
		self.descrp_img.blit(para.img)
	def refresh_single(self,type:str):
		try:
			self.items[type]
		except KeyError:
			self.refresh()
		else:
			textv=text.render(f"{type}:{self.parent.inventory[type]}")
			img=getattr(image,type)
			if type =="placebridge":
				img=pygame.Surface((16,16),pygame.SRCALPHA).convert_alpha()
				img.blit(pygame.transform.scale(getattr(image,type),(16,32)))
			itemsurf=pygame.Surface((textv.get_width()+img.get_width()+2,max(textv.get_height(),img.get_height())+1),pygame.SRCALPHA).convert_alpha()
			itemsurf.fill((0,0,0,0))
			itemsurf.blit(img,(textv.get_width()+1,itemsurf.get_height()/2-img.get_height()/2))
			itemsurf.blit(textv,(0,itemsurf.get_height()/2-textv.get_height()/2))
			itemrect=itemsurf.get_rect(topleft=self.items[type]["rect"].topleft)
			self.items.update({type:{"rect":itemrect,"img":itemsurf}})

	def update(self):
		moe=pygame.mouse.get_pressed()
		self.mouse[1]=self.mouse[0]
		self.mouse[0]=moe[0]
		a,d=pygame.mouse.get_pos()
		scale=[screen_width/window.get_width(),screen_height/window.get_height()]
		mpos=[a*scale[0],d*scale[1]]
		a,b= pygame.mouse.get_rel()
		if moe[2]:
			pass
		speed=[a*scale[0],b*scale[1]] if True in c.mouse[0] else c.mouse_scroll
		if (speed!=[0,0] or True in self.mouse) and self.window_rect.collidepoint(mpos):
			self.offset=[min(1,self.offset[0]+speed[0]),min(1,self.offset[1]+speed[1])]
			speed=[0,0] if True in c.mouse[0] else c.mouse_scroll
		else:
			self.offset=[min(0,self.offset[0]),min(0,self.offset[1])]
		

		if self.mouse==[True,False]:
			for i in self.items:
				if self.items[i]["rect"].collidepoint(mpos[0]-self.offset[0],mpos[1]-self.offset[1])==True:
					self.mdownrect=self.items[i]["rect"]
					break
			else:
				if self.window_rect.collidepoint(mouse_get_pos()):
					self.selected_box=[0,0]
					self.selected=None
					self.mdownrect=None
					self.descrp_img.fill((0,0,0,0))


		check=lambda obj: self.items[obj]["rect"].collidepoint((mouse_get_pos()[0]-self.offset[0],mouse_get_pos()[1]-self.offset[1])) and self.parent.total[obj]!=0 and self.mdownrect==self.items[obj]["rect"] and self.window_rect.collidepoint(mouse_get_pos()) and self.mouse==[False,True]
		check_hover=lambda obj: self.items[obj]["rect"].collidepoint((mouse_get_pos()[0]-self.offset[0],mouse_get_pos()[1]-self.offset[1])) and self.parent.total[obj]!=0 and self.window_rect.collidepoint(mouse_get_pos())

		
		if self.hold_box.pressed==True and self.parent.inventory[self.selected]!=0:
			self.hold_item(self.selected)
		for item in self.itemtypes:
			try:
				if check(item):
					self.selected=item
					self.refresh_descrp(item)
					self.selected_box=[make_surf(self.items[item]["rect"].size,(0,0,0,64),pygame.SRCALPHA),(self.items[item]["rect"].topleft[0]-6,self.items[item]["rect"].topleft[1]-6)]
			except KeyError:
				pass
		for type in self.itemtypes:
			try:
				self.items[type]
			except KeyError:
				pass 
			else:
				if self.selected!=type:
					if check_hover(type):
						self.hover_box=[make_surf(self.items[type]["rect"].size,(0,0,0,32),pygame.SRCALPHA),(self.items[type]["rect"].topleft[0]-6,self.items[type]["rect"].topleft[1]-6)]
						break
					if check(type):
						self.selected_box=[make_surf(self.items[type]["rect"].size,(0,0,0,64),pygame.SRCALPHA),(self.items[type]["rect"].topleft[0]-6,self.items[type]["rect"].topleft[1]-6)]
						break
		else:
			self.hover_box=[0,0]
		try:
			self.parent.inventory[self.selected]
		
		except KeyError:
			pass
		else:
			if self.selected in self.fishtypes:
				
				#tut_buy=lambda a= ():None
				if self.sellboxs["1"]["rect"].collidepoint(mouse_get_pos()) and self.mouse==[False,True]:
					if self.parent.inventory[self.selected]-1!=-1:
						self.parent.inventory[self.selected]-=1
						self.parent.inventory["copper"]+=game.sellinfo["fish"][self.selected]
						self.parent.total["copper"]+=game.sellinfo["fish"][self.selected]
						self.refresh_single(self.selected)
						self.refresh_single("copper")
						#tut_buy()
						game.buy_tutorial()
				elif self.sellboxs["50%"]["rect"].collidepoint(mouse_get_pos()) and self.mouse==[False,True]:
					self.parent.inventory["copper"]+=(x:=game.sellinfo["fish"][self.selected]//2*self.parent.inventory[self.selected])
					self.parent.total["copper"]+=x
					self.parent.inventory[self.selected]//=2
					self.refresh_single(self.selected)
					self.refresh_single("copper")
					#tut_buy()
					game.buy_tutorial()
				elif self.sellboxs["all"]["rect"].collidepoint(mouse_get_pos()) and self.mouse==[False,True]:
					self.parent.inventory["copper"]+=(x:=game.sellinfo["fish"][self.selected]*self.parent.inventory[self.selected])
					self.parent.total["copper"]+=x
					self.parent.inventory[self.selected]=0
					self.refresh_single(self.selected)
					self.refresh_single("copper")
					#tut_buy()
					game.buy_tutorial()
		self.hold_box.update()
	def hold_item(self,item):
		if self.parent.inventory[item]<=0:
			return None
		game.stage="play"
		self.last_held=str(item)
		game.player.hold_item(item)
		if item=="placebridge":
			game.player.placingbridge=True
		elif item=="mallet":
			game.player.malleting=True
		
	def draw(self):
		screen.blit(self.back)
		self.item_img.fill((0,0,0,0))
		#self.item_img.blit(self.item_surf,self.offset)
		screen.blit(self.descrp_img,(122,7))
		#screen.blit()
		try:
			self.item_img.blit(self.selected_box[0],add_poses(self.selected_box[1],self.offset))
		except TypeError:
			pass
		try:
			self.item_img.blit(self.hover_box[0],add_poses(self.hover_box[1],self.offset))
		except TypeError:
			pass
		for key in self.items:
			self.item_img.blit(self.items[key]["img"],add_poses(self.items[key]["rect"].topleft,[self.offset[0]-6,self.offset[1]-6]))
			#pygame.draw.rect(screen,(255,0,255),self.items[key]["rect"])
		self.item_img.set_at((0, 0), (0,0,0,0))
		self.item_img.set_at((0, 105), (0,0,0,0))
		screen.blit(self.item_img,(6,6))
		if self.selected in self.fishtypes:
			for box in self.sellboxs:
				screen.blit(self.sellboxs[box]["img"],self.sellboxs[box]["rect"])
		self.hold_box.draw() if self.selected!=None else None

class c():
	def __init__(self):
		self.key={
		"w":[False,False],
		"a":[False,False],
		"s":[False,False],
		"d":[False,False]
		}
		self.otherkey={
		"e":[False,False],
		"q":[False,False]
		}
		self.mouse={
		0:[False,False]
		}
		self.pkey={
		"w":False,
		"a":False,
		"s":False,
		"d":False,
		"LSHIFT":False
		}
		self.mouse_speed=mouse_get_speed()
		self.mouse_scroll=[0,0]
	def update(self):
		key=pygame.key.get_pressed()
		mouse=pygame.mouse.get_pressed()
		self.mouse_speed=mouse_get_speed()
		for k in self.key:
			self.key[k][1]=self.key[k][0]
			self.key[k][0]=key[getattr(pygame,f"K_{k}")]
		for k in self.pkey:
			self.pkey[k]=key[getattr(pygame,f"K_{k}")]
		for k in self.otherkey:
			self.otherkey[k][1]=self.otherkey[k][0]
			self.otherkey[k][0]=key[getattr(pygame,f"K_{k}")]
		for k in self.mouse:
			self.mouse[k][1]=self.mouse[k][0]
			self.mouse[k][0]=mouse[0]
c=c()

class Player():
	def __init__(self):

		self.sheet=image.playersheet
		self.img=pygame.Surface((24,20),pygame.SRCALPHA).convert_alpha()
		self.frame=0
		self.animation_timer=0
		self.sit_clock=0
		self.img.blit(self.sheet,(self.frame*-24,0))
		self.disimg=self.img
		self.showing=True
		self.pos=game.save.read()["pos"]
		self.truepos=list(self.pos)
		self.chunkpos=[math.floor(self.pos[0]/(32*game.world.chunksize[0])),math.floor(self.pos[1]/(32*game.world.chunksize[1]))]
		self.y_order=self.pos[1]-13
		self.speed=[1,1]
		self.new_speed=list(self.speed)
		self.rect=self.img.get_rect(topleft=self.pos)
		self.size=list(self.img.get_size())
		self.rect.height=10
		self.rect.width=10

		self.fishingline=rope(self.pos,[0,0])

		self.direction=[0,0]
		self.mousepressed=[False,False]
		self.P_pressed=[False,False]

		self.fishing=False
		self.fishinganimationtimer=0
		self.fishingtimer=0
		self.fishon=False

		self.placingbridge=False
		self.malleting=False
		self.golfcarting=False

		self.held=None
		self.held_img=get_surf_from_sheet(image.playersheet,(0,0),(24,20))#replace w/ smth for LOQRE
		self.held_rpos=[6,9]
		self.held_bob_timer=0
		self.hold_item("duck",self.held_img)
		self.unhold_item()

		self.speed_timer=countdown(2**32)

		self.inventory=game.save.read()["inventory"]
		self.total=game.save.read()["total"]
		self.money=0
	def update(self):
		#print(self.speed,self.new_speed,self.speed_timer.timer,self.speed_timer.tick)
		self.key=controller(flag="key")
		if self.key[pygame.K_0] and game.path=="jsons/dev save.json":
			self.speed=[14,14]
		else:
			if self.speed_timer.tick:
				self.speed=[1,1]
			elif self.speed_timer.timer>0:
				self.speed=list(self.new_speed)
			else:
				self.speed=[1,1]

		key=self.key
		mousepos=list(pygame.mouse.get_pos())
		scale=[screen_width/window.get_width(),screen_height/window.get_height()]
		mousepos[0]*=scale[0]
		mousepos[1]*=scale[1]
		self.P_pressed[1]=self.P_pressed[0]
		self.ppos=self.truepos
		if self.golfcarting:
			game.current_screen_size[1]=1.2*screen_height
			game.current_screen_size[0]=1.2*screen_width
			self.showing=False
		else:
			game.current_screen_size[1]=screen_height
			game.current_screen_size[0]=screen_width
			self.showing=True
		if True in [key[pygame.K_d],key[pygame.K_a],key[pygame.K_s],key[pygame.K_w]]:
			self.direction=[0,0]			
		self.controller_move() if not self.golfcarting else None
		if not self.golfcarting:
			self.pos=self.truepos
		else:
			self.truepos=self.pos=[game.golf_cart.rect.midbottom[0]-12,game.golf_cart.rect.midbottom[1]-20]


		#self.pos=[self.truepos[0],self.truepos[1] if self.truepos[1]%1==self.truepos[0]%1 else round(self.truepos[1])]
		if key[pygame.K_p]:
			self.P_pressed[0]=True
		else:
			self.P_pressed[0]=False
		if self.P_pressed==[True,False] and False:
			rhbtrss=0
			for i2 in game.sellinfo["fish"]:
				rhbtrss+=game.sellinfo["fish"][i2]*self.inventory[i2]
				self.inventory[i2]=0
			self.inventory["copper"]+=rhbtrss
			self.total["copper"]+=rhbtrss
			Notice("sold all fish")
			Notice("+"+str(rhbtrss),image.copper)

		if  True in (key[pygame.K_d],key[pygame.K_a],key[pygame.K_s],key[pygame.K_w]):
			self.sit_clock=0
			self.animation_timer+=1
			if self.animation_timer>=6:
				self.animation_timer=0
				self.frame+=1
				self.frame%=8
				self.img.fill((0,0,0,0))
				self.img.blit(self.sheet,(self.frame*-24,0))
				self.disimg=self.img
				wrere=self.rect.collidelist(game.world.tilelist)
				tilev=game.world.tilelist[wrere]
				if tilev.type==1:
					Particle(2,randint(150,210),list(self.rect.midbottom),0.7,(202,130,56),gravity=0.1,lifeloss=0.1)
				elif tilev.type==2:
					Particle(2,randint(150,210),list(self.rect.midbottom),0.7,(22,190,66),gravity=0.1,lifeloss=0.1)
				elif tilev.type==4:
					Particle(2,randint(150,210),list(self.rect.midbottom),0.7,(130,50,30),gravity=0.1,lifeloss=0.1)
		else:
			self.img.fill((0,0,0,0))
			self.sit_clock+=1
			if self.sit_clock>=1800:
				self.img.blit(self.sheet,(0,-20))		
			else:
				self.animation_timer=9
				self.img.blit(self.sheet)
			self.disimg=self.img
		self.rect.x=self.pos[0]+7
		if self.speed[0]!=14:
			if self.rect.collidelist(game.world.wallrectlist)!=-1:
				if self.direction[0]==-1:
					for i in range(math.ceil(abs(self.speed[0]))):
						self.pos[0]+=1
						self.rect.x+=1
						if self.rect.collidelist(game.world.wallrectlist)==-1:
							break
				if self.direction[0]==1:
					for i in range(math.ceil(self.speed[0])):
						self.pos[0]-=1
						self.rect.x-=1
						if self.rect.collidelist(game.world.wallrectlist)==-1:
							break
			
		self.rect.y=self.pos[1]+10
		if self.speed[1]!= 14:
			if self.rect.collidelist(game.world.wallrectlist)!=-1:
				if self.direction[1]==-1:
					for i in range(math.ceil(abs(self.speed[1]))):
						self.pos[1]+=1
						self.rect.y+=1
						if self.rect.collidelist(game.world.wallrectlist)==-1:
							break
				if self.direction[1]==1:
					for i in range(math.ceil(self.speed[1])):
						self.pos[1]-=1
						self.rect.y-=1	
						if self.rect.collidelist(game.world.wallrectlist)==-1:
							break



		if self.direction[0]==1:
			self.disimg=pygame.transform.flip(self.img,True,False)
		self.chunkpos=[math.floor(self.pos[0]/(32*game.world.chunksize[0])),math.floor(self.pos[1]/(32*game.world.chunksize[1]))]
		self.mousepressed[1]=self.mousepressed[0]
		self.mousepressed[0]=pygame.mouse.get_pressed()[0]
		self.held_bob_timer+=1
		if self.held_bob_timer==89:
			self.held_rpos[1]-=1
		elif self.held_bob_timer==44:
			self.held_rpos[1]+=1
		self.held_bob_timer%=90
		self.update_fishing()
		self.update_placebridging_and_malleting()
		self.y_order=self.rect.midbottom[1]


	def draw(self):
		if self.showing:
			screen.blit(self.disimg,withscroll(self.pos))
			try:
				screen.blit(self.held_img,withscroll(add_poses(self.pos,self.held_rpos)))
			except TypeError:
				pass

	def controller_move(self):
		key=self.key
		if key[pygame.K_d]:
			self.direction[0]+=1
			if key[pygame.K_w] or key[pygame.K_s]:
				self.truepos[0]+=self.speed[0]
			else:
				self.truepos[0]+=self.speed[0]
		if key[pygame.K_a]:
			self.direction[0]-=1
			if key[pygame.K_w] or key[pygame.K_s]:
				self.truepos[0]-=self.speed[0]
			else:
				self.truepos[0]-=self.speed[0]
		if key[pygame.K_w]:
			self.direction[1]-=1
			if key[pygame.K_a] or key[pygame.K_d]:
				self.truepos[1]-=self.speed[1]
			else:
				self.truepos[1]-=self.speed[1]
		if key[pygame.K_s]:
			self.direction[1]+=1		
			if key[pygame.K_a] or key[pygame.K_d]:
				self.truepos[1]+=self.speed[1]
			else:
				self.truepos[1]+=self.speed[1]
	def add_inventory(self,item_:str,amount_:int,with_notice=False):
		if with_notice:
			try:
				getattr(image,item_)
			except AttributeError:
				Notice(f"+{amount_} {item_}")
			else:
				Notice(f"+{amount_} {item_}",getattr(image,item_))
		if item_=="placebridge":
			game.tutorial.delay_change(["good job on your first placebridge","use can use the placebridge by ","going to the inventory, hold the","placebridge and place it on the waters.","","now go explore new lands!"],"using placebridge")
		self.inventory[item_]+=amount_
		self.total[item_]+=max(amount_,0)
	def update_fishing(self):
		key=self.key
		if self.fishing==True:
			self.fishingline.update()
			if self.fishinganimationtimer<90:
				self.fishinganimationtimer+=1
				self.fishingtimer+=1
			elif self.fishingtimer==90:
				
				self.fishingtimer+=1
				collided=False
				for tilev in game.world.waterlist:
					if tilev.rect.collidepoint(self.fishingline.line[1]):
						collided=True
						break
				if collided==False:
					self.fishing=False
					self.fishon=False
					self.fishingtimer=0
				else:
					for i in range(5):
						Particle(5,randint(150,210),self.fishingline.line[1],randint(10,25)/10,(255,255,255),alpha=128,lifeloss=0.1,gravity=0.1)
			self.fishingline.draw()
			"""
			else:
				if randint(0,360)==14 or self.fishingtimer>=600:
					self.fishon=True
				self.fishingtimer+=1
			
			if self.fishon==True:
				self.fishingline.splash.update()
				dfvsa=withscroll(self.fishingline.line[1])
				self.fishingline.splash.draw([dfvsa[0]-7,dfvsa[1]-7])
			"""
		else:
			self.fishon=False
			self.fishingline.landed=False
		if self.mousepressed==[True,False] and self.fishing==False:
			self.fishinganimationtimer=0
			final_y=(mouse_get_pos()[1]-game.scroll[1])
			gravity=0.1
			time=90
			speed=[((mouse_get_pos()[0]-game.scroll[0])-self.rect.center[0])/time,((final_y-self.rect.center[1])/time)-gravity*time/2]
			if self.direction[0] in [-1,0]:
				self.fishingline.reinit(self.pos,speed)
			else:
				self.fishingline.reinit([self.pos[0]+23,self.pos[1]],speed)
			self.fishing=True
		elif (self.mousepressed==[True,False] or True in (key[pygame.K_d],key[pygame.K_a],key[pygame.K_s],key[pygame.K_w])) and self.fishing==True:
			self.fishing=False
			self.fishingtimer=0
			"""
			if self.fishon==True:
				listv=[]
				a=0
				fish=self.reelfish(self.fishingline.line[1])
				try:
					self.inventory[fish]+=1
				except KeyError:
					Notice("no fish in this area ]:")
				else:
					Notice(f"+1 {fish}",getattr(image,fish))
			"""
			self.fishon=False
	def update_placebridging_and_malleting(self):
		key=self.key
		a=(math.floor((mouse_get_pos()[0]-game.scroll[0])/32)*32+game.scroll[0],math.floor((mouse_get_pos()[1]-game.scroll[1])/32)*32+game.scroll[1])
		if self.placingbridge:
			screen.blit(image.placebridge,a )
			if c.mouse[0]==[False,True]:
				for tilev in game.world.waterlist+game.world.nonstonewallwalllist:
					if tilev.rect.collidepoint(withoutscroll(mouse_get_pos())):
						self.placingbridge=False

						tilev=Tile(1,4,[a[0]-game.scroll[0],a[1]-game.scroll[1]],lists=[game.world.tilelist,game.world.placebridgelist],rectlists=[game.world.nonwallrectlist],img=image.placebridge,child=Tile(0,5,[a[0]-game.scroll[0],a[1]-game.scroll[1]+32],lists=[game.world.tilebackdecrolist],img=image.placebridge,sheetpos=(0,-32)))
						tilev.initother()
						self.inventory["placebridge"]-=1
						game.tutorial.delay_change(["you can quickly hold the last item "," you held by pressing: [q]","you can also unhold by pressing [g]"],"quick holding and unholding")
						self.unhold_item()
		elif self.malleting:
			x=mouse_get_pos()
			u=withoutscroll(x)
			screen.blit(image.mallet,(x[0]-7,x[1]-8))
			v=False
			if c.mouse[0]==[False,True]:
				for b in game.world.placebridgelist:
					if b.rect.collidepoint(u):
						v=True
						if not b.rect.colliderect(self.rect):
							self.malleting=False
							self.add_inventory("rotting_wood",1,with_notice=True)
							if random.random()>0.8:
								Notice("+1 yellow_mold",image.yellow_mold)
								self.inventory["yellow_mold"]+=1
							b.pop()
						else:
							Notice("cannot mallet this")
				if not v:
					Notice("cannot mallet this")
		if key[pygame.K_g]:
			self.placingbridge=False
			self.malleting=False
			self.unhold_item()
	def reelfish(self,pos):
		list_=[]
		for node in game.nodelist:
			if ((node.pos[0]-pos[0])**2+(node.pos[1]-pos[1])**2)**0.5<=32*node.range:
				list_.append(node.truedensity)
		if list_==[]:
			return None
		d_=add_dicts(list_)
		a=random.random()*sum(list(d_.values()))
		fish=[0,0]
		for d in list_:
			for f in d:
				fish[0]+=d[f]
				if fish[0]>a>fish[1]:
					d[f]-=1
					d[f]=max(d[f],0)
					self.total[f]+=1
					return f
				fish[1]=fish[0]
	def hold_item(self,item:str,img=None):
		if img==None:
			self.held_img=getattr(image,item)
		else:
			self.held_img=img
		self.held=item
		if item=="placebridge":
			self.held_img=image.placebridgeicon
		rect=self.held_img.get_rect()
		self.held_rpos=[self.size[0]/2-rect.width/2,-rect.height-2]
	def unhold_item(self):
		self.held_img=None 
		self.held=None	
	def speed_boost(self,speed=2,time=120*60):
		self.speed_timer.timer+=time
		self.new_speed=[speed,speed]

				
class npc():
	def __init__(self,type,pos,imgs:dict=None):
		self.id=len(game.npcdict)
		game.npcdict[self.id]=self
		try:
			self.popped=game.save.read()["npcs_not_popped"][str(self.id)]
		except KeyError:
			self.popped=False			
		self.type=type
		self.pos=pos
		self.rect=pygame.Rect(pos,(1,1))
		self.range=1
		self.parent_chunk=None
		self.in_dialogue=False
		self.diamessage="none"
		self.state="none"
		self.s_update=lambda:None

		if self.type==t.stall_1:
			self.imgs={
			"roof":[get_surf_from_sheet(image.stallsheet,(-45,0),(45,48)),[0,0]],
			"chicken":[get_surf_from_sheet(image.chicken,(0,0),(24,21)),[17,24],[0,0]],
			"bottom":[get_surf_from_sheet(image.stallsheet,(0,0),(45,48)),[0,0]]
			}
			game.world.assign_chunk(self,get_chunk_pos(self.pos))
			self.rect=pygame.Rect((self.pos[0],self.pos[1]),(50,48))
			self.range=1.2
			self.etotalk=frontdecr(image.etotalk,(self.pos[0]+5,self.pos[1]+5))
			def s():
				self.bob("chicken")
			self.s_update=s
			def s_s():
				game.speech.update_speech("how can i help you?",{
					'3 copper: 3 placebridge':[{"placebridge":3},{"copper":3},"cont_placebridge"],
					"20 copper 4 bass:1 mallet":[{"mallet":1},{"copper":20,"bass":4},"cont"],
					"bye":[{},{},"exit"]
					})
			self.s_speech=s_s
		elif self.type==t.golf_cart_part:
			self.imgs={"part":[image.golf_cart_part,[0,0]]}
			self.rect=pygame.Rect(self.pos,(7,12))
			self.range=1
			self.etotalk=frontdecr(image.etointeract,(self.pos[0]-15,self.pos[1]-5),appendtolist=True)

			def s_s():
				game.speech.update_speech("you found a golf cart part!",
					{"cont":[{"golf_cart_part":1},{},"exit_pop"]})
				#Notice("+1 golf cart part",image.golf_cart_part)
			def s():
				if "pop" in self.state:
					self.pop()
					return None
			self.s_update=s
			self.s_speech=s_s
		elif self.type==t.gcbs:
			print(self.pos)
			decr(get_surf_from_sheet(image.gcbs_sheet,(0,0),(162,84)),self.pos,"topleft",colliderect=((self.pos[0]+19,self.pos[1]+64),(162-38,24) ))
			decr(get_surf_from_sheet(image.gcbs_sheet,(-162,0),(85,31)),add_poses(self.pos,(63,65)),"topleft",colliderect=((self.pos[0]+19,self.pos[1]+64),(162-38,15) ))
			self.imgs={"crow":[image.crow,[84,66],[0,0]]}
			game.world.assign_chunk(self,get_chunk_pos(self.pos),"decr")
			self.etotalk=frontdecr(image.etotalk,[self.pos[0]+100,self.pos[1]+50])
			self.rect=pygame.Rect(self.pos,(200,84))
			self.state="congrates"
			def s_s():

				if game.golf_cart.pos[0]<=-696:
					game.speech.update_speech(["if you got 3 golf cart parts","and 50 coppers i can make you a golf cart"],{
						'ooh ok ':[{"golf_cart":1},{"golf_cart_part":3,"copper":50},"congrates"],
						"bye":[{},{},"exit"]	
						})
				elif game.diamessage=="congrates":
					game.speech.update_speech(("for your scavenging i present to","you a golf cart!"),{
						"cont":[{},{},"exit"]
						})
				elif game.diamessage=="returngc":
					game.speech.update_speech("don't worry, i got you",
						{
						"[cont ]":[{},{},"exit"]
						})
				else:
				 game.speech.update_speech("its the golf cart duck!",
				 	{"i lost it...":[{"golf cart return":1},{},"returngc"],
				 	"bye":[{},{},"exit"]
				 	})
			self.s_speech=s_s
			def s():
				self.bob("crow")		
				if game.diamessage=="congrates":
					self.s_speech()
			self.s_update=s
			self.range=1.7
		elif self.type==t.anchovyfisher:
			self.imgs={"duck":[image.duck,[0,0],[0,0]]}
			self.etotalk=frontdecr(image.etotalk,(self.pos[0]-15,self.pos[1]-5))
			self.rect=self.imgs["duck"][0].get_rect(topleft=self.pos)
			def s_s():
				game.speech.update_speech("anchovies.",{
					"give 2":[{"copper":5},{"anchovy":2},"cont"],
					"leave":[{},{},"exit"]
					})
			self.s_speech=s_s
		elif self.type==t.duckling:
			self.imgs={"ducking":[image.duckling,[0,0],[0,0]]}
			self.etotalk=frontdecr(image.etotalk,(self.pos))
			self.rect=self.imgs["ducking"][0].get_rect(topleft=self.pos)
			def s_s():
				game.speech.update_speech("hey mr goose!",
					{"intresting.[leave]":[{},{},"exit"]})
			self.s_speech=s_s
		elif self.type==t.eagle:
			self.imgs={"eagle":[image.eagle,[0,0]]}
			self.etotalk=frontdecr(image.etotalk,add_poses(self.pos,(0,-8)))
			self.rect=self.imgs["eagle"][0].get_rect(topleft=self.pos)
			self.state="give"
			def s_s():
				if self.state=="give":
					game.speech.update_speech(["a prestiged marlin appears in our","local lake once a day.   if you catch","it i will reward you greatly!"],
						{"okay! (accept quest)":[{},{},"accept_marlin_quest_exit"],
						"i'll pass":[{},{},"exit"]})
				elif self.state=="wait":
					game.speech.update_speech(["the marlins are at the ","lake on the between the islands"],
						{
						"i caught it!  [give 1 black marlin] ":[{"copper":25},{"black_marlin":1},"black_marlin_quest_complete_exit"],
						"okay":[{},{},"exit"]
						})
				
			def s():
				if game.diamessage=="accept_marlin_quest_exit":
					self.state="wait"
				elif game.diamessage=="black_marlin_quest_complete_exit":
					self.state="give"
			self.s_update=s
			self.s_speech=s_s
		elif self.type==t.shrine:
			self.imgs={"shrine":[image.shrine,[0,0]]}
			self.etotalk=frontdecr(image.etointeract,add_poses(self.pos,(20,20)))
			self.rect=self.imgs["shrine"][0].get_rect(topleft=self.pos)
			def s_s():
				game.speech.update_speech(["you peer into the shrine in awe.","you think about giving it some offerings"],
					{
					"offer 50 coppers":[{"speed boost":4*60*60},{"copper":50},"exit"],
					"leave without offering":[{},{},"exit"]
					})
			self.s_speech=s_s

		if imgs!=None:

			self.imgs=imgs
		self.y_order=self.rect.midbottom[1]
		if self.type==t.gcbs:
			self.talk_pos=self.etotalk.pos

		else:
			self.talk_pos=self.rect.center
		game.world.assign_chunk(self,get_chunk_pos(self.pos),"decr")
		game.npclist.append(self)
		game.drawlist.append(self)
	def update(self):
		if self.popped:
			self.pop()
		#try:
		self.s_update()
		"""
			try:
				self
			except ValueError:
				return None
		except AttributeError:
			pass
		"""
		dist=get_dist(self.talk_pos,game.player.rect.center)
		if not game.in_dialogue:
			self.in_dialogue=False
		if self.in_dialogue:
			if dist>=32*self.range:
				game.in_dialogue=False
				self.etotalk.show=False
				self.in_dialogue=False
		elif dist<=32*self.range:
			self.etotalk.show=True
			if c.otherkey["e"]==[False,True]:
				
				game.in_dialogue=True
				self.in_dialogue=True

		elif dist>=32*self.range:
			self.etotalk.show=False
			self.in_dialogue=False

		if self.in_dialogue==True:
			game.npc_in_dialogue=self
			try:
				self.s_speech()
			except AttributeError:
				game.speech.update_speech(["this one's ability to speak has been","impounded by ved-dev..."],{"cont":[{},{},"exit"]})

	def bob(self,key):
		self.imgs[key][2][1]=self.imgs[key][2][0]
		self.imgs[key][2][0]+=1
		for k in c.key:
			if c.key[k]==[False,True]:
				self.imgs[key][2][0]+=9		
		if self.imgs[key][2][0]> 45 >=self.imgs[key][2][1]:
			self.imgs[key][1][1]+=1
		elif self.imgs[key][2][0]> 90 >=self.imgs[key][2][1]:
			self.imgs[key][1][1]-=1

		self.imgs[key][2][0]%=91		

	def draw(self):
		#pygame.draw.rect(screen,(255,0,255),self.rect)
		for i in self.imgs:
			screen.blit(self.imgs[i][0],withscroll((self.imgs[i][1][0]+self.pos[0],self.imgs[i][1][1]+self.pos[1])))
	def pop(self):
		lists=[game.npclist,game.drawlist,self.parent_chunk.decrlist]
		for i,list_ in enumerate(lists):

			try:
				list_.remove(self)
			except ValueError:
				pass
		self.etotalk.pop()
		self.popped=True

class Speech():
	def __init__(self):
		self.box=image.textbox
		self.rbox=pygame.Surface((1,1),pygame.SRCALPHA).convert_alpha()
		self.rboxsheet=image.responsebox
		self.rsize=[0,0]
		self.rtext=[text.render("unloaded 303")]
		self.speech=text.render("unloaded 404")
		self.mpressed=[False,False]
		self.mdownrect=None
		self.hover_surf={"surf":pygame.Surface((1,1),pygame.SRCALPHA).convert_alpha(),"pos":[0,0]}
	def update_speech(self,speech_:str,responses:dict):
		game.in_dialogue=True
		self.speech=text.render(speech_) if type(speech_)==str else Para(speech_).img
		"""
		responses={
			"trade name 1":[items_get_from_npc:dict,items_give_to_npc:dict,contiue message:str]
			"trade name 2":[items_get_from_npc:dict,items_give_to_npc:dict,contiue message:str]
			"response 1":[None,None,]
			...
		}
		"""
		self.rtext=[[text.render(r),pygame.Rect( (0,0),(len(r)*8+2,8)),responses[r]] for i,r in enumerate(responses)]
		self.rsize=[max(r[0].get_width() for r in self.rtext)+8,len(self.rtext)*8+8]
		for i,thing in enumerate(self.rtext):
			thing[1].topleft=(4,i*8+2+screen_height-self.rsize[1]-self.box.get_height()-1)
		self.rbox=pygame.Surface(self.rsize,pygame.SRCALPHA).convert_alpha()
		for y in range(0,math.ceil(self.rsize[1])+8,8):
			for x in range(0,math.ceil(self.rsize[0])+8,8):
				if [x,y]==[0,0]:
					s=get_surf_from_sheet(self.rboxsheet,(0,0),(8,8))
				elif [x,y]==[self.rsize[0]-8,self.rsize[1]-8]:
					s=get_surf_from_sheet(self.rboxsheet,(-16,-16),(8,8))
				elif [x,y]==[0,self.rsize[1]-8]:
					s=get_surf_from_sheet(self.rboxsheet,(0,-16),(8,8))
				elif [x,y]==[self.rsize[0]-8,0]:
					s=get_surf_from_sheet(self.rboxsheet,(-16,0),(8,8))
				elif x==0:
					s=get_surf_from_sheet(self.rboxsheet,(0,-8),(8,8))
				elif y==0:
					s=get_surf_from_sheet(self.rboxsheet,(-8,0),(8,8))
				elif x==self.rsize[0]-8:
					s=get_surf_from_sheet(self.rboxsheet,(-16,-8),(8,8))
				elif y==self.rsize[1]-8:
					s=get_surf_from_sheet(self.rboxsheet,(-8,-16),(8,8))
				else:
					s=get_surf_from_sheet(self.rboxsheet,(-8,-8),(8,8))
				self.rbox.blit(s,(x,y))
	def update(self):
		#self.hover_surf={"surf":pygame.Surface((1,1),pygame.SRCALPHA).convert_alpha(),"pos":[0,0]}
		m=(mouse_get_pos(),pygame.mouse.get_pressed())
		self.mpressed[1]=self.mpressed[0]
		self.mpressed[0]=m[1][0]
		for i in self.rtext:
			a=i[1].collidepoint(m[0])
			if a==True:
				self.hover_surf={"surf":make_surf(i[1].size,(64,64,64,64),pygame.SRCALPHA),"pos":i[1].topleft}
				self.mdownrect=i[1]
				break
			else:
				self.hover_surf={"surf":pygame.Surface((0,0)).convert(),"pos":(0,0)}
		if self.mpressed==[True,False]:
			for r in self.rtext:
				if r[1].collidepoint(m[0]):
					
					if self.mdownrect==r[1]:
						for take in r[2][1]:
							if r[2][1][take]>game.player.inventory[take]:
								Notice("insufficient resources")
								return None
						for take in r[2][1]:
							if type(r[2][1][take])==str:
								pass
							else:
								game.player.inventory[take]-=r[2][1][take]

						for give in r[2][0]:
							if give == "golf_cart":
								game.golf_cart.pos=list(game.player.pos)
								game.tutorial.delay_change(["enter and exit the golf cart by pressing [e]"],"using golf_cart")
							elif give == "golf_cart_stat_up":
								game.golf_cart.levelup()
							elif give == "golf cart return":
								game.golf_cart.respawn()
							elif give == "speed boost":
								game.player.speed_boost(2,4*60*60)
							else:
								game.player.add_inventory(give,r[2][0][give])
						try:
							if give=="placebridge":
								Notice(f"placebridge +3",pygame.transform.scale(get_surf_from_sheet(image.placebridge,(0,0),(32,32)),(16,16)))
							else:
								Notice(f"{give} +{r[2][0][give]}",getattr(image,give))
						except UnboundLocalError:
							pass
						except AttributeError:
							Notice(f"{give} +{r[2][0][give]}")
						if "exit" in str(r[2][2]):
							game.in_dialogue=False
							game.npc_in_dialogue.state=r[2][2]
							game.npc_in_dialogue=None
						game.set_diamessage(r[2][2])

						return r[2][2]
	def draw(self):
		screen.blit(self.box,(0,90))
		screen.blit(self.speech,(4,94))
		screen.blit(self.rbox,(0,(screen_height-self.rsize[1])-self.box.get_height()-2))
		screen.blit(self.hover_surf["surf"],self.hover_surf["pos"])
		for i in range(len(self.rtext)):
			#pygame.draw.rect(screen,(255,0,255),self.rtext[i][1])
			screen.blit(self.rtext[i][0],self.rtext[i][1])	
class frontdecr():
	def __init__(self,img,pos,init=None,method=None,draw_method=None,parent=None,appendtolist=True):
		self.img=img
		self.pos=pos
		
		self.method=method
		if draw_method==None:
			self.draw_method=frontdecr.standard_draw
		else:
			self.draw_method=draw_method
		self.show=False
		self.parent=parent
		try:
			init(self)
		except TypeError:
			pass
		game.frontdecrlist.append(self) if appendtolist==True else None
	def init_golf_cart_bar(self):
		self.bar_back=pygame.Rect((3,game.current_screen_size[1]-3-30),(30,30))
		self.bar=self.bar_back.copy()
		self.max_fuel=self.parent.max_fuel
	def golf_cart_bar_update(self):
		self.bar.size=(self.parent.fuel/self.max_fuel*30,self.parent.fuel/self.max_fuel*30)
		self.bar_back.topleft=(3,game.current_screen_size[1]-3-30)
		self.bar.bottomleft=self.bar_back.bottomleft
	def update(self):
		self.method(self)
	def make_show(self,bool_:bool):
		self.show=bool_
	def golf_cart_bar_draw(self):
		if self.show:
			pygame.draw.rect(screen,(100,100,100),self.bar_back)
			pygame.draw.rect(screen,(200,200,100),self.bar)
	def standard_draw(self):
		if self.show:
			screen.blit(self.img,withscroll(self.pos))
	def draw(self):
		self.draw_method(self)
	def pop(self):
		try:
			game.frontdecrlist.remove(self)
		except ValueError:
			pass
		del self

class Daynight():
	def __init__(self):
		self.timer=timer(60*120)
		self.img=make_surf((screen_width*1.5,screen_height*1.5),(55,45,40))
		self.disimg=self.img.copy()
		#circle_size=40
		#self.player_light=make_circle_surf(circle_size,(20,20,5))
		#self.light_pos=(screen_width/2-circle_size,screen_height/2-circle_size-5)
		#self.disimg=make_hole(self.disimg,self.player_light,self.light_pos)
	def update(self):
		self.timer.update()
	def draw(self):
		if self.timer.timer<2*self.timer.interval/3:
			return
		screen.blit(self.disimg,(0,0),special_flags=pygame.BLEND_RGB_SUB)

	#	screen.blit(self.player_light,self.light_pos,special_flags=pygame.BLEND_RGB_ADD)
class Map:
	def __init__(self,data,bg_colour=(50,100,200),scale=7):
		self.data=data
		self.size=[len(self.data[0]),len(self.data)]
		self.bg_colour=bg_colour
		self.player_ani=animation(image.player_icon_sheet,[11,11],6)
		self.set_palette()
		self.offset=[0,0]
		self.scale=scale
		self.render()
		
	def set_palette(self):
		self.palette={
		0:[(50,100,200)],
		1:[(225,132,39),(234,142,60),(211,117,28)],
		2:[(9,191,76),(8,175,75),(26,204,88),(13,216,79)],
		6:[(255,227,160),(255,245,190),(255,207,92)],
		3:[(51,51,62),(40,54,48),(47,47,56)],
		5:[(230,240,255),(180,220,236),(180,220,200)]
		}
	def render(self):
		
		self.map=pygame.Surface(self.size).convert()
		self.map.fill(self.bg_colour)
		for y,row in enumerate(self.data):
			for x,tile in enumerate(row):
				try:
					self.map.set_at((x,y),random.choice(self.palette[tile]))
				except KeyError:
					pass
		self.map=pygame.transform.scale_by(self.map,(self.scale,self.scale))
		self.size[0]*=self.scale
		self.size[1]*=self.scale
	def update(self):
		self.player_ani.update()
		self.player_pos=[(math.floor(i/32))*7 for i in game.player.pos]
		self.player_pos=add_poses(self.player_pos,(-2,-2))
		if c.mouse[0][0]:
			self.offset=add_poses(c.mouse_speed,self.offset)
		else:
			self.offset=[clamp(self.offset[0],[0,min(-self.size[0]+screen_width,0)]),clamp(self.offset[1],[0,min(-self.size[1]+screen_height,0)])]
	def draw(self):
		screen.blit(self.map,self.offset)
		self.player_ani.draw(add_poses(self.player_pos,self.offset))
	def reshow(self):
		self.offset=[-(math.floor(i/32))*7-3 for i in game.player.pos]
		self.offset[0]+=screen_width/2
		self.offset[1]+=screen_height/2
class Game():
	def __init__(self):
		Func.set_main_game(self)
		maps.Maps.set_main_game(self)
		self.drawlist=[]
		self.nodelist=[]
		self.particles=[]
		self.npclist=[]
		self.npcdict={}
		self.frontdecrlist=[]
		self.waves=[]
		self.fishs=[]
		self.loaded_chunks=[]
		self.remove_fishs=[]
		self.loaded_decrs=[]
		self.loaded_drawlist=[]
		self.stage="play"
		self.last_stage="tutorial_menu"

		self.in_dialogue=None
		self.npc_in_dialogue=None
		self.path="jsons/dev save.json"
		self.save=file(self.path)
		self.diamessage="none"
		self.sellinfo=file("jsons/sell info.json").read()
		self.fuel_info=file("jsons/refill info.json").read()
		self.upgrade_info=file("jsons/upgrade info.json").read()
		self.map_data=file("tilemap/map 2.tmj").read()
		maps.Maps.set_map_data()
		self.current_screen_size=[screen_width,screen_height]
		self.daynight=Daynight()
		self.mapping=False
		#types
	def initother(self):
		self.tutorial=Tutorial()
		self.tutorial_menu=Tutorial_menu()

		self.world=world()
		self.world.initother()
		self.waveables=[tile.rect for tile in self.world.tilelist if tile not in self.world.waterlist]

		self.player=Player()
		self.golf_cart=Golf_cart()
		self.drawlist.append(self.player)
		self.drawlist.append(self.golf_cart)
		self.scroll=[self.player.rect.center[0],self.player.rect.center[1]]
		self.map=Map(self.world.layer1)

		self.notice_board=Notification_Center()
		self.inventory=inventory()
		self.stall_1=npc(t.stall_1,(836, 681))
		self.golf_cart_part=npc(t.golf_cart_part,[34*32,36*32])
		self.speech=Speech()
		self.nodelist=[
		fishingnode((429, 551),
			{"anchovy":9,
			"chub_mackerel":7,
			"sardine":4
			},
			7
			)
		
		,fishingnode((1000, 678),
			{
			"anchovy":150,
			"sardine":5
			},
			range_=2,fish_limit=7)
		
		,fishingnode((767, 800),
			{
			"anchovy":20,
			"sardine":2,
			},fish_limit=5)
		
		,fishingnode((1045, 452),
			{
			"anchovy":5,
			"bass":10,
			"sardine":5
			},
			3.25
			)
		
		,fishingnode((414, 960),
			{
			"pink_rockling":10,
			"rockling":10
			},
			5)
		
		,fishingnode((1437, 197),
			{
			"pink_salmon":20,
			"anchovy":10
			},
			5),fishingnode((1384, 964),
			{
			"pink_salmon":25,
			"anchovy":5
			},
			5)
		
		,fishingnode((1099, 1398),{
			"black_marlin":1
			},1,respawn_rate=60*60*5,fish_limit=1)
		,fishingnode((923, 1110),{
			"yellow_perch":10
			},3)
		,fishingnode((797, 1127),{
			"yellow_perch":10
			},3),fishingnode((379, 1214),{"duckfish":3},range_=0.5,regen=1200)]
		
		try:
			a=self.save.read()["node densities"]
			for i,node in enumerate(self.nodelist):
				node.initother(a[i])
			

		except KeyError:
			pass
		except IndexError:
			pass
	def set_diamessage(self,message:str):
		self.diamessage=message
	def change_stage(self,stage):
		if self.stage== stage:
			return
		self.last_stage=self.stage
		self.stage=stage
	def sell_tutorial(self):
		self.tutorial.delay_change(["nice work on your first fish!","sell fish by pressing the"," inventory button[t] and choose the","amount of fish to sell"],"sell fish")
	def buy_tutorial(self):
		game.tutorial.delay_change(["   nice work on your fisrt coppers!","you can use this coppers"," to buy 'placebridges' at the stall"],"buy placebridge")
def get_save():
	return {
		"inventory":game.player.inventory,
		"total":game.player.total,
		"placebridge":[tile.pos for tile in game.world.placebridgelist],
		"pos":game.player.pos,
		"node densities":[node.get_all_fish() for node in game.nodelist],
		"golf cart":{
		"pos":game.golf_cart.pos,
		"fuel":game.golf_cart.fuel,
		"rate":game.golf_cart.rate,
		"accel":game.golf_cart.accel,
		"level":game.golf_cart.level
		},
		"npcs_not_popped":{key:val.popped for key,val in game.npcdict.items()},
		"tutorials_shown":game.tutorial_menu.tutorials_shown
			}
def make_item(name:str,place_after:str,catergory:str,cost:int,refill:int=0,para:list=[]):
	f=file("jsons/new.json")
	f1=file("jsons/fishopedia.json")
	f2=file("jsons/sell info.json")
	f3=file("jsons/dev save.json")
	f4=file("jsons/refill info.json")

	d=f.read()
	d1=f1.read()
	d2=f2.read()
	d3=f3.read()
	d4=f4.read()
	d["inventory"]=dict_insert(d["inventory"],(name,0),place_after)
	d["total"].update({name:0})
	d3["inventory"]=dict_insert(d3["inventory"],(name,0),place_after)
	d3["total"].update({name:0})
	d1.update({name:para})

	d2[catergory].update({name:cost})
	d4.update({name:refill})

	f.overwrite(d)
	f1.overwrite(d1)
	f2.overwrite(d2)
	f3.overwrite(d3)
	f4.overwrite(d4)
	raise Exception(f"item, {name}, made")
def do_chunks():
	pass
#make_item("yellow_perch","pink_salmon","fish",3,2000,["this fish is so full","itself. always trying to","look the flashlist"])

"""
,size:float or int
,angle: float or int 
,pos:list
,totalspeed=10
,colour=(255,255,255)
,gravity=0.5
,lifeloss=0.5
,staticspeed=[0,0]
,alphaloss=0
,alpha=255
,blendflag=pygame.BLENDMODE_NONE
"""
game=Game()
game.initother()
#make_item("duckfish","pink_salmon","fish",x:=-(2**64),x,[ "so you've found me","[insert lore text]"])
testnotice=Notice("welcome!",image.bigfish)
coco=decr(image.coconut_tree,[31*32+10,15*32])
#game.tutorial.change(["welcome to the","world of duckfish!","cast your rod to fish","fish where the fish are"],"fishing")
chunk_loader=threading.Thread(target=do_chunks)
run= True
while run==True:
	#game.scroll=[0,0]
	#game.drawlist=sorted(game.drawlist,key=lambda thing : thing.y_order)

	screen=pygame.Surface(game.current_screen_size).convert()
	screen.fill((50,100,200))
	scrolling=False
	pfasd=[0,0]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type ==pygame.KEYDOWN:
			if event.key==pygame.K_t:
				if game.stage!="inventory":
					game.stage="inventory"
					game.inventory.refresh()
				else:
					game.change_stage('play')
				
			elif event.key==pygame.K_f:
				game.save.overwrite(get_save())
				Notice("saved!",image.bigfish)
			elif event.key==pygame.K_q:
				game.inventory.hold_item(game.inventory.last_held)
			elif event.key==pygame.K_ESCAPE:
				if game.stage=="tutorial":
					pass
				elif game.stage=="tutorial_menu":
					game.change_stage("play")
				else:
					game.change_stage("tutorial_menu")
			elif event.key==pygame.K_r:
				game.change_stage("map") if not game.stage=="map" else game.change_stage("play")
				game.map.reshow()
		elif event.type == pygame.MOUSEWHEEL:
			scrolling=True

			pfasd=  [-event.precise_y*4,event.precise_x*4] if c.pkey["LSHIFT"] else [-event.precise_x*4,event.precise_y*4]
			print(pfasd)
	if scrolling:
		c.mouse_scroll=pfasd
	else:
		c.mouse_scroll=[0,0]
	c.update()
	game.tutorial.always_update()
	if game.stage== "play":
		game.daynight.update()
		if random.random()>0.93 and len(game.waves)<5:
			pos=withoutscroll([random.random()*screen_width*3-screen_width ,random.random()*screen_height*3-screen_height])
			rect=pygame.Rect(pos,(25,5))
			Wave(pos) if rect.collidelist(game.waveables)==-1 else None
		for node in game.nodelist:
			node.update()
			node.draw2()
			#if random.random()<1/1200:
		#		node.add_fish()
		for node in game.nodelist:
			node.draw()	
		for node in game.nodelist:
			node.draw_fish()
		for wave in game.waves:
			wave.draw()


		key=game.player.chunkpos
		game.loaded_chunks=[]
		game.loaded_decrs=[]
		game.loaded_drawlist=[]
		for y in range(key[1]-2,key[1]+3):
			for x in range(key[0]-2,key[0]+3):
				try:
					chunk=game.world.chunks[y][x]
					game.loaded_chunks.append(chunk)
				except IndexError:
					pass
		for chunk in game.loaded_chunks:
			game.loaded_decrs+=chunk.decrlist
			chunk.draw_tiles()
		game.loaded_drawlist+=game.loaded_decrs
		game.loaded_drawlist.append(game.player)
		game.loaded_drawlist.append(game.golf_cart)
		game.loaded_drawlist=sorted(game.loaded_drawlist,key=lambda thing : thing.y_order)

		if game.in_dialogue:
			game.speech.update()
			game.speech.draw()
		for n in game.npclist:
			n.update()
		for w in game.waves:
			w.update()
		for	rgsfbe in game.loaded_drawlist:
			rgsfbe.draw()
		for particle in game.particles:
			particle.update()
			particle.draw()
		for d in game.frontdecrlist:
			d.draw()
		#screen.blit(image.lampsheet,withscroll((game.player.pos[0],game.player.pos[1]-10)),special_flags= pygame.BLEND_RGB_ADD)
		#screen.blit(image.mold)
		game.player.update()
		game.golf_cart.update()
		game.scroll=[-math.floor(game.player.rect.center[0] if not game.player.golfcarting else game.golf_cart.rect.midtop[0])+math.floor(game.current_screen_size[0]/2),
				 -math.floor(game.player.rect.center[1] if not game.player.golfcarting else game.golf_cart.rect.midtop[1])+math.floor(game.current_screen_size[1]/2)]
		#game.scroll=[0, 0]
		game.daynight.draw()
		game.notice_board.update()
		game.notice_board.draw()
		if game.in_dialogue==True:
			game.speech.draw()
			game.speech.update()

		game.fishs=[fish for fish in game.fishs if fish not in game.remove_fishs]
		game.remove_fishs=[]
		
	elif game.stage=="inventory":
		game.current_screen_size=[screen_width,screen_height]
		game.inventory.update()
		game.inventory.draw()
	elif game.stage=="map":
		game.map.update()
		game.map.draw()
	elif game.stage=="tutorial":
		game.tutorial.update()
		game.tutorial.draw()
		game.current_screen_size=[screen_width,screen_height]
	elif game.stage=="tutorial_menu":
		game.tutorial_menu.update()
		game.tutorial_menu.draw()
		game.current_screen_size=[screen_width,screen_height]

	#c=pygame.Surface((500,500))

#	c.fill((70,70,50))
#	screen.blit(c,special_flags=pygame.BLEND_RGB_SUB)
	clock.tick(60)
	pygame.display.set_caption(f"{game.player.pos},{clock.get_fps()}")
	screen= pygame.transform.scale(screen,(window.get_width(),window.get_height()))
	window.blit(screen)
	pygame.display.update()
print(game.player.rect.midbottom)
game.save.overwrite(get_save())
pygame.quit()
