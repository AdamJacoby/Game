import pygame as pg

from Functions.Piece_Class import Piece,bishop_move
from Images.Piece_images import draw_text_piece
from Functions.Game_Functions import Cell_To_Pix,Draft_To_Pix,Loc_To_Grid


class White_Lotus(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text):
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text)
		self.boundry = None

	def remove(sefl):
		Piece.remove(self)
		self.boundry = None

	def update(self):
		if self.loc_type in ['place_zone','t1','t2','t3','t4','t5','t6','t7','t8','nutral_zone','goal']:
			grid = Loc_To_Grid(self.loc)
			print [max(1,grid[0]-4),min(11,grid[1]+4)]
			UL =  Cell_To_Pix(max(1,grid[0]-3),min(11,grid[1]+3),'ul')
			LR = Cell_To_Pix(min(11,grid[0]+3),max(1,grid[1]-3),'lr')
			width = LR[0]-UL[0]
			height = LR[1]-UL[1]
			print [width,height]
			boarder = pg.Surface([width,height])
			boarder.fill((255,255,255))
			pg.draw.rect(boarder,(204,0,204),[0,0,width,height],10)
			boarder.set_colorkey((255,255,255))
			self.boundry = pg.display.get_surface().blit(boarder,UL)
		self.rect = pg.display.get_surface().blit(self.surface,self.loc)


white_lotus_move = 'Movement: Two spaces in diagonal directions'
white_lotus_ability = 'Ability: Pieces cannot leave the 7x7 square centered on the White Lotus'
White_Loctus = White_Lotus('White Lotus',draw_text_piece('Lts',(96,96,96)),Draft_To_Pix([5,4]),bishop_move,True,'p',white_lotus_move,white_lotus_ability)