import pygame as pg

from Functions.Piece_Class import Piece,rook_move
from Images.Piece_images import draw_text_piece
from Functions.Game_Functions import Loc_To_Cell,Loc_To_Cell,White_Lotus_Check,All_Straight_Line_Intersections,Get_Current_Piece,Draft_To_Pix,Cell_To_Pix

Grey=(96,96,96)
class Power(Piece):
	#Given a piece in a straight line and a direction checks the white lotus condition and to see if there is a piece behind it
	def legal_target(self,target_piece,direction,Pieces,Board):
		pos = target_piece.pos
		target_pos = [pos[0]+direction[0],pos[1]+direction[1]]
		target_loc = Cell_To_Pix(target_pos,Board)
		if target_pos[0] in [0,12] or target_pos[1] in [0,12]:
			return False
		if not White_Lotus_Check(Pieces,target_piece,target_piece.loc,target_loc):
			return False
		for piece in Pieces:
			if piece.pos == target_pos:
				return False
		return True

	#Determins if there is any legal target for the ability
	def legal_ability(self,Pieces,Board):
		[targets,directions] =All_Straight_Line_Intersections(self.pos,Pieces,Board)
		targets_exist=False
		for i in range(0,len(targets)):
			if self.legal_target(targets[i],directions[i],Pieces,Board):
				targets_exist=True
		if targets_exist:
			return Piece.legal_ability(self,Pieces,Board)
		return False

	#Enacts the ability
	def ability(self,Pieces,Board,*args):
		[targets,directions] =All_Straight_Line_Intersections(self.pos,Pieces,Board)
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
					target_piece = Get_Current_Piece(mouse_pos,Pieces)
					if target_piece!=None:
						if target_piece in targets:
							direction = directions[targets.index(target_piece)]
							target_loc = Cell_To_Pix([target_piece.pos[0]+direction[0],target_piece.pos[1]+direction[1]],Board)
							if self.legal_target(target_piece,direction,Pieces,Board):
								target_piece.move(target_loc,Pieces,Board)
								self.unselect(Pieces,Board)
								return True