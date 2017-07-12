import pygame as pg

from Functions.Piece_Class import Piece
from Functions.Game_Functions import Pix_To_Hand,Hand_To_Pix

class Rock(Piece):
	def remove(self,Pieces):
		hand =[]
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc_type=='hand':
				hand.append(int(round(piece.loc[0]/self.cell_dim+1)))
		if len(hand)==7:
			Piece.remove(self,Pieces)
		else:
			self.loc_type='hand'
			for i in range(1,8):
				if not(i in hand):
					if self.controller == 1:
						self.loc = [int(self.cell_dim*(i-1)),int(round(float(self.board_height)/4))-self.cell_dim]
					if self.controller ==0:
						self.loc = [int(self.cell_dim*(i-1)),int(round(3*float(self.board_height)/4))]