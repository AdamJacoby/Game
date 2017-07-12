import pygame as pg

from Functions.Piece_Class import Piece
from Functions.Game_Functions import Cell_To_Pix,Loc_To_Cell


class White_Lotus(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board):
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board)
		self.boundry = None

	def remove(self):
		Piece.remove(self)
		self.boundry = None

	def update(self):
		if self.loc_type in ['place_zone','t1','t2','t3','t4','t5','t6','t7','t8','nutral_zone','goal']:
			x=max(1,self.pos[0]-3)
			y=min(11,self.pos[1]+3)
			UL=[int(self.board_start+(self.cell_dim+1)*(x-1)),int(self.board_height-(self.cell_dim+1)*y)]
			x = min(11,self.pos[0]+3)
			y = max(1,self.pos[1]-3)
			LR = [int(self.board_start+(self.cell_dim+1)*x),int(self.board_height-(self.cell_dim+1)*(y-1))]
			width = LR[0]-UL[0]
			height = LR[1]-UL[1]
			boarder = pg.Surface([width,height])
			boarder.fill((255,255,255))
			pg.draw.rect(boarder,(204,0,204),[0,0,width,height],10)
			boarder.set_colorkey((255,255,255))
			self.boundry = pg.display.get_surface().blit(boarder,UL)
		self.rect = pg.display.get_surface().blit(self.surface,self.loc)