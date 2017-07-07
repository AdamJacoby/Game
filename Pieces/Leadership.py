import pygame as pg

from Functions.Piece_Class import Piece,bishop_move
from Functions.Game_Functions import Draft_To_Pix,Is_Adjacent,move_ability_action,Get_Current_Piece
from Images.Piece_images import draw_text_piece

class Leadership(Piece):
	def legal_ability(self,Pieces,Turn_Indicator):
		legal=False
		for piece in Pieces:
			if piece.controller ==self.controller and not piece.loc_type in ['hand','draft']:
				legal=True
		if not legal:
			return False
		return Piece.legal_ability(self,Pieces,Turn_Indicator)

	def ability(self,Pieces,Turn_Indicator,pop_up):
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
leadership_move = 'Movement: Two spaces in any diagonal direction'
leadership_ability = 'Ability: Can give its turn to any allied piece'
Leadership = Leadership('Leadership',draw_text_piece('Ldr',(96,96,96)),Draft_To_Pix([1,2]),bishop_move,True,'a',leadership_move,leadership_ability)