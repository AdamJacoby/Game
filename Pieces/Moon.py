import pygame as pg

from Functions.Piece_Class import Piece,bishop_move
from Images.Piece_images import draw_text_piece
from Functions.Game_Functions import Loc_To_Grid,Loc_To_Cell,White_Lotus_Check,All_Straight_Line_Intersections,Get_Current_Piece,Draft_To_Pix,Cell_To_Pix

Grey=(96,96,96)
class Moon(Piece):
	#Given a piece in a straight line and a direction checks the white lotus condition and to see if there is a piece behind it
	def legal_target(self,target_piece,direction,Pieces):
		pos = Loc_To_Grid(target_piece.loc)
		target_pos = [pos[0]-direction[0],pos[1]-direction[1]]
		target_loc = Loc_To_Cell(target_pos)
		if not White_Lotus_Check(Pieces,target_piece,target_piece.loc,target_loc):
			return False
		if self.loc == target_loc:
			return False
		return True

	#Determins if there is any legal target for the ability
	def legal_ability(self,Pieces,Turn_Indicator):
		[targets,directions] =All_Straight_Line_Intersections(self.loc,Pieces)
		targets_exist = False
		for i in range(0,len(targets)):
			if self.legal_target(targets[i],directions[i],Pieces):
				targets_exist=True
		if targets_exist:
			return Piece.legal_ability(self,Pieces,Turn_Indicator)
		return False

	#Enacts the ability
	def ability(self,Pieces,Turn_Indicator,*args):
		[targets,directions] =All_Straight_Line_Intersections(self.loc,Pieces)
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
					target_piece = Get_Current_Piece(mouse_pos,Pieces)
					if target_piece!=None:
						if target_piece in targets:
							target_piece_pos = Loc_To_Cell(target_piece.loc)
							direction = directions[targets.index(target_piece)]
							target_loc = Cell_To_Pix(target_piece_pos[0]-direction[0],target_piece_pos[1]-direction[1],'ul')
							if self.legal_target(target_piece,direction,Pieces):
								target_piece.move(target_loc,Pieces)
								self.unselect(Pieces)
								return True
moon_move = 'Movement: Two spaces in any diagonal direction'
mone_ability = 'Ability: Before moving can pull any unblocked piece in a straight line direction 1 space back'
Moon = Moon('Moon',draw_text_piece('Moon',Grey),Draft_To_Pix([3,2]),bishop_move,True,'am',moon_move,mone_ability)