import pygame as pg
from pygame.sprite import Sprite
from Images.Board_Display import Create_Board
from math import ceil, floor

pg.font.init()

class Board(Sprite):
	def __init__(self,width):
		Sprite.__init__(self)
		self.width=width
		self.cell_dim = int(ceil(2*round((float(width)/2-11)/11)+1)/2)
		self.height = 11*self.cell_dim+11
		self.board_start=self.width-self.height
		print 'the height is:' +str(self.height)
		self.board_surface = Create_Board(width)
		text_height=0
		i=1
		while text_height<floor(self.width/40):
			self.font = pg.font.SysFont('Comic Sans MS', i)
			text_height = self.font.render('text',False,(0,0,0),(255,255,255)).get_height()
			i=i+1
		x = int(round(float(width)/4))
		y = int(round(float(width)/8))
		self.button_x = int(round(float(width)/16))
		button_x = self.button_x
		self.button_y = int(round(float(width)/32))
		button_y = self.button_y
		self.background_PU = pg.Surface([x,y])
		self.background_PU.fill((255,255,255))
		pg.draw.rect(self.background_PU,(0,0,0),[0,0,x,y],10)
		pg.draw.rect(self.background_PU,(0,255,0),[int(round(float(x)/6)),button_x,button_x,button_y])
		pg.draw.rect(self.background_PU,(0,255,0),[int(round(7*float(x)/12)),button_x,button_x,button_y])
		#button surfaces
		self.button1=pg.Surface([button_x,button_y])
		self.button1.fill((0,255,0))
		self.button2=pg.Surface([button_x,button_y])
		self.button2.fill((0,255,0))
		self.button1_loc = [int(round(width*float(666)/1600)),int(round(float(width)*float(396)/1600))]
		self.rect1=pg.Rect(self.button1_loc[0],self.button1_loc[1],button_x,button_y)
		self.button2_loc = [int(round(width*float(833)/1600)),int(round(width*float(396)/1600))]
		self.rect2=pg.Rect(self.button2_loc[0],self.button2_loc[1],button_x,button_y)
		self.question=None
		self.button1=None
		self.button2=None
		#Locations to blit objects to on main screen
		self.background_PU_loc = [int(round(width*float(3)/8)),int(round(width*float(296)/1600))]
		#Variables that deal with the turn indicators
		self.turn_number = 0
		self.turn_name = 0
		self.turn_order = [0,'t1',1,'t2',0,'t3',1,'t4',0,'t5',1,'t6',0,'t7',1,'t8']
		strip_width = int(self.board_start-round((float(7)/8)*self.board_start))
		box_dim = int(round(float(self.height)/(16+float(17)/4)))
		gap_dim = int(floor(float(self.height-16*box_dim)/17))
		left_side = int(round((float(7)/8)*self.board_start)+round(float(strip_width-box_dim)/2))
		surface = pg.Surface([box_dim+4,box_dim+4])
		surface.fill((255,255,255))
		pg.draw.rect(surface, (0,0,0), [0,0, box_dim+4,box_dim+4],6)
		surface.set_colorkey((255,255,255))
		self.surface_TI=surface
		temp =[]
		for i in range(0,16):
			temp .append([left_side,gap_dim-2+i*(box_dim+gap_dim)])
		self.loc_order = temp
		pg.display.get_surface().blit(self.surface_TI,self.loc_order[self.turn_number])
		#Text Screen Variables
		self.text_TS=None
		self.surface_TS = None
		self.background_TS = pg.Surface([int(round(width*float(700)/1600)),int(round(float(width)/16))])
		self.background_TS.fill((255,255,255))
		self.loc_TS = [3,int(round(float(width)*696/1600))]

	def update(self):
		pg.display.get_surface().blit(self.board_surface,[0,0])
		pg.display.get_surface().blit(self.surface_TI,self.loc_order[self.turn_number])

	def configure_PU(self,question_text,button1_text,button2_text):
		self.button1_text = button1_text
		self.button2_text = button2_text
		self.question=self.font.render(question_text,False,(0,0,0),(255,255,255))
		self.button1=self.font.render(button1_text,False,(0,0,0),(0,255,0))
		self.button2=self.font.render(button2_text,False,(0,0,0),(0,255,0))

	def update_PU(self):
		pg.display.get_surface().blit(self.background_PU,[self.background_PU_loc[0],self.background_PU_loc[1]])
		pg.display.get_surface().blit(self.question,[self.background_PU_loc[0]+int(round(float(self.width)/8))-int(round(float(self.question.get_width())/2)),self.background_PU_loc[1]+int(round(float(self.button_y)/3))])
		y = self.background_PU_loc[1]+self.button_x+int(round(float(self.button_y-self.button1.get_height())/2))
		pg.display.get_surface().blit(self.button1,[self.button1_loc[0]+int(round(float(self.button_x-self.button1.get_width())/2)),y])
		pg.display.get_surface().blit(self.button2,[self.button2_loc[0]+int(round(float(self.button_x-self.button2.get_width())/2)),y])

	def ask_PU(self):
		temp = pg.display.get_surface().copy()
		self.update_PU()
		pg.display.flip()
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						pg.display.get_surface().blit(temp,[0,0])
						pg.display.flip()
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					if self.rect1.collidepoint(mouse_pos):
						pg.display.get_surface().blit(temp,[0,0])
						pg.display.flip()
						return self.button1_text
					if self.rect2.collidepoint(mouse_pos):
						pg.display.get_surface().blit(temp,[0,0])
						pg.display.flip()
						return self.button2_text

	def update_TI(self):
		pg.display.get_surface().blit(self.surface_TI,self.loc_order[self.turn_number])

	def next_turn(self):
		self.turn_number= (self.turn_number+1)%16
		self.turn_name = self.turn_order[self.turn_number]

	def configure_TS(self,text):
		self.text_TS=text
		self.surface_TS = self.font.render(text,False,(0,0,0),(255,255,255))

	def update_TS(self):
		pg.display.get_surface().blit(self.background_TS,self.loc_TS)
		pg.display.get_surface().blit(self.surface_TS,[self.loc_TS[0],self.loc_TS[1]])

