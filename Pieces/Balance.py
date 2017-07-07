import pygame as pg

#Custom scripts
from Images.Piece_images import draw_text_piece
from Functions.Piece_Class import Piece,rook_move
from Functions.Game_Functions import Get_Current_Piece,White_Lotus_Check,Draft_To_Pix


class Balance(Piece):

	def legal_ability(self,Pieces,Turn_Indicator):
		temp = False
		for piece in Pieces:
			if piece.controller != self.controller and not(piece.loc_type in ['draft','hand','goal','nutral_zone']):
				temp = True
		if temp ==False:
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
						if (current_piece.controller!=self.controller and not (current_piece.loc_type in ['hand','draft','goal','nutral_zone'])
						and White_Lotus_Check(Pieces,self,self.loc,current_piece.loc) and White_Lotus_Check(Pieces,current_piece,current_piece.loc,self.loc)):
							temp_loc = self.loc
							self.loc=current_piece.loc
							self.loc_type=current_piece.loc_type
							current_piece.move(temp_loc,Pieces)
							self.unselect(Pieces)
							return True
balance_move = 'Movement: Two paces in vertical or horizontal directions'
balance_ability = 'Ability: Instead of moving can swap places witth an enemy piece not in the goal or nutral zone'
Balance = Balance('Balance',draw_text_piece('Bal',(96,96,96)),Draft_To_Pix([5,1]),rook_move,True,'a',balance_move,balance_ability)