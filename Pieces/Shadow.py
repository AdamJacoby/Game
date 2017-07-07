import pygame as pg

from Functions.Piece_Class import Piece
from Functions.Game_Functions import Find_Zone,Draft_To_Pix,White_Lotus_Check,Gaurded,Loc_To_Cell,Loc_To_UL,Frozen,Is_Adjacent
from Images.Piece_images import draw_text_piece

class Shadow(Piece):
	def legal_ability(self,Pieces,Turn_Indicator):
		other_pieces = False
		for piece in Pieces:
			if piece.controller == self.controller and not piece.loc_type in ['hand','draft']:
				other_pieces = True
		if not other_pieces:
			return False
		return Piece.legal_ability(self,Pieces,Turn_Indicator)

	def ability(self,Pieces,Turn_Indicator,*args):
		while True:
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
						forward = False
						for piece in Pieces:
							if (piece.controller == self.controller and Is_Adjacent(Loc_To_Cell(loc),Loc_To_Cell(piece.loc)) and
								White_Lotus_Check(Pieces,self,self.loc,loc)):
								forward = True
						for piece in Pieces:
							if piece.controller == self.controller and piece.loc==loc:
								forward=False
						if forward:
							self.move(loc,Pieces)
							return True

shadow_movement = 'Movement: None'
shadow_ability = 'Ability: Can move next to any allied piece as if it were a normal move'
Shadow = Shadow('Shadow',draw_text_piece('Shdw',(96,96,96)),Draft_To_Pix([1,1]),[[0,0]],False,'a',shadow_movement,shadow_ability)