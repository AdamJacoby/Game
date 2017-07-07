import pygame as pg

#Custom functions
from Functions.Piece_Class import Piece,pawn_move,queen_move
from Functions.Game_Functions import Gaurded, Check_If_Blocked,Loc_To_Cell,Draft_To_Pix,Get_Current_Piece
from Images.Piece_images import draw_text_piece

class Wood(Piece):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,attack_range,move_text,ability_text):
		self.attack_range = attack_range
		Piece.__init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text)

	def legal_shot(self,target,Pieces):
		loc = target.loc
		target_pos = Loc_To_Cell(loc)
		self_pos = Loc_To_Cell(self.loc)
		if not([self_pos[0]-target_pos[0],self_pos[1]-target_pos[1]] in self.attack_range):
			return False
		if Check_If_Blocked(self,target_pos,Pieces):
			print 'The shot is blocked.'
			return False
		if Gaurded(loc,Pieces,self.controller):
			return False
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def legal_ability(self,Pieces,Turn_Indicator):
		shots_exists = False
		for piece in Pieces:
			if self.legal_shot(piece,Pieces):
				shots_exists=True
		if not shots_exists:
			return False
		return Piece.legal_ability(self,Pieces,Turn_Indicator)

	def ability(self,Pieces,Turn_Indicator,*args):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.unselect(Pieces)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					current_piece = Get_Current_Piece(mouse_pos,Pieces)
					if current_piece!=None:
						if self.legal_shot(current_piece,Pieces):
							current_piece.remove(Pieces)
							self.unselect(Pieces)
							return True

wood_move = 'Movement: Any adjacent square'
wood_ability = 'Ability: instead of moving can remove an unblocked piece two spaces alway in a straight line'
Wood = Wood('Wood',draw_text_piece('Wd',(96,96,96)),Draft_To_Pix([1,3]),pawn_move,False,'a',queen_move,wood_move,wood_ability)