import pygame as pg

from Functions.Piece_Class import Piece
from Functions.Game_Functions import Find_Zone,White_Lotus_Check,Gaurded,Loc_To_Cell,Loc_To_UL,Frozen

class Fire(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board):
		self.move_range2 = [[1,1],[1,-1],[1,0],[-1,1],[-1,-1],[-1,0],[0,1],[0,-1]]
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board)

	def legal_move2(self,loc,Pieces,Board):
		if loc == None:
			return False
		if White_Lotus_Check(Pieces,self,self.loc,loc)== False:
			return False
		target_pos = Loc_To_Cell(loc,Board)
		if not([self.pos[0]-target_pos[0],self.pos[1]-target_pos[1]] in self.move_range2):
			return False
		if Gaurded(target_pos,Pieces,self.controller):
			return False
		if Frozen(self,Pieces):
			return False
		if target_pos== [6,6]:
			return True
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def ability(self,Pieces,Board,*args):
		Capture = False
		done = False
		while not done:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect(Pieces,Board)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos)
					if self.legal_move(loc,Board,Pieces):
						for piece in Pieces:
							if piece.loc == loc and piece.controller!=self.controller:
								Capture=True
						self.move(loc,Pieces,Board)
						done = True
		self.select()
		while Capture:
			Board.update()
			Pieces.update()
			pg.display.flip()
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect(Pieces,Board)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos,Board)
					if self.legal_move2(loc,Pieces,Board):
						self.loc=loc
						self.loc_type = Find_Zone(self.loc)
						temp = False
						for piece in Pieces:
							if piece.controller!=self.controller and piece.loc ==loc:
								piece.remove(Pieces)
								temp = True
						Capture = temp
		self.unselect(Pieces,Board)
		return True