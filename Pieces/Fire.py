import pygame as pg

from Functions.Piece_Class import Piece,knight_move
from Functions.Game_Functions import Find_Zone,Draft_To_Pix,White_Lotus_Check,Gaurded,Loc_To_Grid,Loc_To_UL,Frozen
from Images.Piece_images import draw_text_piece

class Fire(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text):
		self.move_range2 = [[1,1],[1,-1],[1,0],[-1,1],[-1,-1],[-1,0],[0,1],[0,-1]]
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text)

	def legal_move2(self,loc,Pieces):
		if loc == None:
			return False
		if White_Lotus_Check(Pieces,self,self.loc,loc)== False:
			return False
		target_pos = Loc_To_Grid(loc)
		self_pos = Loc_To_Grid(self.loc)
		if not([self_pos[0]-target_pos[0],self_pos[1]-target_pos[1]] in self.move_range2):
			return False
		if Gaurded(loc,Pieces,self.controller):
			return False
		if Frozen(self,Pieces):
			return False
		if target_pos== [6,6]:
			return True
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def ability(self,Pieces,Turn_Indicator,*args):
		from Board_Display import Board
		Capture = False
		done = False
		while not done:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect(Pieces)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos)
					if self.legal_move(loc,Turn_Indicator,Pieces):
						for piece in Pieces:
							if piece.loc == loc and piece.controller!=self.controller:
								Capture=True
						self.move(loc,Pieces)
						done = True
		self.select()
		while Capture:
			pg.display.get_surface().blit(Board,[0,0])
			Pieces.update()
			pg.display.flip()
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect()
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos)
					if self.legal_move2(loc,Pieces):
						self.loc=loc
						self.loc_type = Find_Zone(self.loc)
						temp = False
						for piece in Pieces:
							if piece.controller!=self.controller and piece.loc ==loc:
								piece.remove(Pieces)
								temp = True
						Capture = temp
		self.unselect(Pieces)
		return True
fire_move = 'Movement: Knight moves'
fire_ability = 'Ability: After taking a piece can move again to an adjacent square'
Fire = Fire('Fire',draw_text_piece('Fire',(96,96,96)),Draft_To_Pix([2,4]),knight_move,False,'a',fire_move,fire_ability)