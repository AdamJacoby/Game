import pygame as pg

#Custom functions
from Functions.Piece_Class import Piece
from Functions.Game_Functions import Gaurded, Check_If_Blocked,Loc_To_Cell,Get_Current_Piece

class Wood(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,attack_range,move_text,ability_text,Board):
		self.attack_range = attack_range
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board)

	def legal_shot(self,target,Pieces,Board):
		loc = target.loc
		target_pos = Loc_To_Cell(loc,Board)
		if not([self.pos[0]-target_pos[0],self.pos[1]-target.pos[1]] in self.attack_range):
			return False
		if Check_If_Blocked(self.pos,target_pos,Pieces):
			print 'The shot is blocked.'
			return False
		if Gaurded(loc,Pieces,self.controller):
			return False
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def legal_ability(self,Pieces,Board):
		shots_exists = False
		for piece in Pieces:
			if self.legal_shot(piece,Pieces,Board):
				shots_exists=True
		if not shots_exists:
			return False
		return Piece.legal_ability(self,Pieces,Board)

	def ability(self,Pieces,Board,*args):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect(Pieces,Board)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					current_piece = Get_Current_Piece(mouse_pos,Pieces)
					if current_piece!=None:
						if self.legal_shot(current_piece,Pieces,Board):
							current_piece.remove(Pieces)
							self.unselect(Pieces,Board)
							return True