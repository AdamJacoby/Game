import pygame as pg

from Functions.Piece_Class import Piece,pawn_move
from Functions.Game_Functions import Find_Zone,Is_Adjacent,Loc_To_UL,Loc_To_Cell
White = (255,255,255)
Red=(255,0,0)
Blue = (0,0,255)
Grey=(96,96,96)

class Mirror(Piece):

	def place(self,loc, Pieces,Board):
		for piece in Pieces:
			if piece.name == 'Mirror Dupe':
				dupe = piece
		self.loc = loc
		self.pos = Loc_To_Cell(loc,Board)
		self.loc_type = Find_Zone(self.pos)
		Board.update()
		Pieces.update()
		pg.display.flip()
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						current_piece.unselect(Pieces,Board)
						return False
				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					mouse_pos = pg.mouse.get_pos()
					loc = Loc_To_UL(mouse_pos,Board)
					pos = Loc_To_Cell(loc,Board)
					unoccupied = True
					for piece in Pieces:
						if piece.loc==loc:
							unoccupied=False
					if unoccupied and Is_Adjacent(pos,self.pos):
						dupe.place(loc,Pieces,Board)
						self.unselect(Pieces,Board)
						return None

	def remove(self,Pieces):
		dupe_exists = False
		for piece in Pieces:
			if piece.name == 'Mirror Dupe':
				Dupe = piece
		if not Dupe.loc_type in ['draft','hand']:
			loc = Dupe.loc
			Dupe.remove(Pieces)
			self.move(loc,Pieces,Board)
		else:
			temp = pg.PixelArray(self.surface)
			temp.replace((255-255*self.controller,0,255*self.controller),Grey)
			self.surface = temp.make_surface()
			self.surface.set_colorkey(White)
			self.loc = self.draft_loc
			self.loc_type = 'draft'
			self.controller=None

class Mirror_dupe(Piece):

	def place(self,loc, Pieces,Board):
		for piece in Pieces:
			if piece.name =='Mirror':
				self.controller = piece.controller
		temp = pg.PixelArray(self.surface)
		temp.replace(Grey,(255-255*self.controller,0,255*self.controller))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.loc = loc
		self.pos = Loc_To_Cell(self.loc,Board)
		self.loc_type = Find_Zone(self.pos)
		self.unselect(Pieces,Board)

	def update(self):
		if self.loc_type == 'draft':
			self.rect = pg.Rect(0,0,0,0)
		else:
			self.rect = pg.display.get_surface().blit(self.surface,self.loc)