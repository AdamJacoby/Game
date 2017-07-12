import pygame as pg

#Custom scripts
from Functions.Piece_Class import Piece
from Functions.Game_Functions import Get_Current_Piece,White_Lotus_Check,Draft_To_Pix,Loc_To_Cell,Loc_To_UL,Is_Adjacent


class Wind(Piece):

	def legal_ability(self,Pieces,Turn_Indicator):
		temp = False
		for piece in Pieces:
			if piece.controller == self.controller and not(piece.loc_type in ['draft','hand','goal','nutral_zone']):
				temp = True
		if temp ==False:
			return False
		return Piece.legal_ability(self,Pieces,Turn_Indicator)

	def ability2(self,Pieces,current_piece,Board):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						current_piece.unselect(Pieces)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos,Board)
					forward = True
					for piece in Pieces:
						if piece.loc==loc:
							forward == False
					pos = Loc_To_Cell(loc)
					if forward == True and White_Lotus_Check(Pieces,current_piece,current_piece.loc,loc):
						current_piece.move(loc,Pieces)
						return True

	def ability(self,Pieces,Board,*args):
		self.select()
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
						if (current_piece.controller==self.controller and not (current_piece.loc_type in ['hand','draft','goal','nutral_zone'])):
							current_piece.select()
							if self.ability2(Pieces,current_piece,Board):
								self.unselect(Pieces)
								return True