import pygame as pg

from Functions.Piece_Class import Piece
from Functions.Game_Functions import Is_Adjacent,move_ability_action,Get_Current_Piece

class Leadership(Piece):
	def legal_ability(self,Pieces,Board):
		legal=False
		for piece in Pieces:
			if piece.controller ==self.controller and not piece.loc_type in ['hand','draft']:
				legal=True
		if not legal:
			return False
		return Piece.legal_ability(self,Pieces,Turn_Indicator)

	def ability(self,Pieces,Board):
		self.active = True
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
						if current_piece.controller ==self.controller:
							if move_ability_action(current_piece,self.controller,Pieces,Turn_Indicator,pop_up):
								self.unselect(Pieces)
								return True