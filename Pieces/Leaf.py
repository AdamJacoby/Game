import pygame as pg

#Custom scripts
from Functions.Piece_Class import Piece
from Functions.Game_Functions import Get_Current_Piece,White_Lotus_Check,Draft_To_Pix


class Leaf(Piece):

	def legal_ability(self,Pieces,Board):
		temp = False
		for piece in Pieces:
			if piece.controller == self.controller and not(piece.loc_type in ['draft','hand','goal','nutral_zone']):
				temp = True
		if temp ==False:
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
						if (current_piece.controller==self.controller and not (current_piece.loc_type in ['hand','draft','goal','nutral_zone'])
						and White_Lotus_Check(Pieces,self,self.loc,current_piece.loc) and White_Lotus_Check(Pieces,current_piece,current_piece.loc,self.loc)):
							temp_loc = self.loc
							self.loc=current_piece.loc
							self.loc_type=current_piece.loc_type
							current_piece.move(temp_loc,Pieces,Board)
							self.unselect(Pieces,Board)
							return True