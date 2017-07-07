import pygame as pg
from pygame.sprite import Sprite

pg.font.init()

class Turn_Indicator(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.turn_number = 0
		self.turn_name = 0
		self.turn_order = [0,'t1',1,'t2',0,'t3',1,'t4',0,'t5',1,'t6',0,'t7',1,'t8']
		surface = pg.Surface([42,42])
		surface.fill((255,255,255))
		pg.draw.rect(surface, (0,0,0), [0,0, 42,42],6)
		surface.set_colorkey((255,255,255))
		self.surface=surface
		temp =[]
		for i in range(0,16):
			temp .append([735,7+i*49])
		self.loc_order = temp
		pg.display.get_surface().blit(self.surface,self.loc_order[self.turn_number])

	def update(self):
		pg.display.get_surface().blit(self.surface,self.loc_order[self.turn_number])

	def next_turn(self):
		self.turn_number= (self.turn_number+1)%16
		self.turn_name = self.turn_order[self.turn_number]

class pop_up(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.font = pg.font.SysFont('Comic Sans MS', 30)
		#Background surface
		self.background = pg.Surface([400,200])
		self.background.fill((255,255,255))
		pg.draw.rect(self.background,(0,0,0),[0,0,400,200],10)
		pg.draw.rect(self.background,(0,255,0),[67,100,100,50])
		pg.draw.rect(self.background,(0,255,0),[233,100,100,50])
		#button surfaces
		self.button1=pg.Surface([100,50])
		self.button1.fill((0,255,0))
		self.button2=pg.Surface([100,50])
		self.button2.fill((0,255,0))
		self.rect1=pg.Rect(667,396,100,50)
		self.rect2=pg.Rect(833,396,100,50)
		self.question=None
		self.button1=None
		self.button2=None
		self.button1_text=None
		self.button2_text=None
		#Locations to blit objects to on main screen
		self.background_loc = [600,296]

	#given a string for both possible solutions and the questions set the variables for the question and button
	def configure(self,question_text,button1_text,button2_text):
		self.button1_text=button1_text
		self.button2_text=button2_text
		self.question=self.font.render(question_text,False,(0,0,0),(255,255,255))
		self.button1 = self.font.render(button1_text,False,(0,0,0),(0,255,0))
		self.button2=self.font.render(button2_text,False,(0,0,0),(0,255,0))

	def update(self):
		pg.display.get_surface().blit(self.background,self.background_loc)
		pg.display.get_surface().blit(self.question,[600+round(float((380-self.question.get_width())/2)),296+50])
		pg.display.get_surface().blit(self.button1,[667+round(float((100-self.button1.get_width())/2)),396])
		pg.display.get_surface().blit(self.button2,[833+round(float((100-self.button2.get_width())/2)),396])

	def ask(self):
		temp = pg.display.get_surface().copy()
		self.update()
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

class Text_Screen(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.text=None
		self.font = pg.font.SysFont('Comic Sans MS', 30)
		self.surface = None
		self.background = pg.Surface([700,100])
		self.background.fill((255,255,255))
		self.loc = [3,696]

	def configure(self,text):
		self.text=text
		self.surface = self.font.render(text,False,(0,0,0),(255,255,255))

	def update(self):
		pg.display.get_surface().blit(self.background,self.loc)
		pg.display.get_surface().blit(self.surface,[self.loc[0]+round(float(700-self.surface.get_width())/2),self.loc[1]])

