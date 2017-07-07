import pygame as pg

from Functions.Piece_Class import Piece, rook_move
from Functions.Game_Functions import Pix_To_Hand,Hand_To_Pix,Draft_To_Pix
from Images.Piece_images import draw_text_piece

class Rock(Piece):
	def remove(self,Pieces):
		hand =[]
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc_type=='hand':
				hand.append(Pix_To_Hand(piece.loc))
		if len(hand)==7:
			Piece.remove(self)
		else:
			self.loc_type='hand'
			for i in range(1,8):
				if not(i in hand):
					self.loc = Hand_To_Pix(self.controller,i)

rock_move=rook_move+[[1,1],[1,-1],[-1,1],[-1,-1]]
rock_movement = 'Movement: Any adjacent space or two spaces in a vertical or horizontal direction'
rock_ability = 'Ability: If you hand is not full Rock returns to your hand when removed'
Rock = Rock('Rock',draw_text_piece('Rck',(96,96,96)),Draft_To_Pix([2,3]),rock_move,True,'p',rock_movement,rock_ability)