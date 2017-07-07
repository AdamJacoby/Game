import pygame as pg

from Functions.Piece_Class import Piece,pawn_move
from Functions.Game_Functions import Draft_To_Pix, Find_Zone,Is_Adjacent,Loc_To_UL,Loc_To_Cell
from Images.Piece_images import draw_text_piece
White = (255,255,255)
Red=(255,0,0)
Blue = (0,0,255)
Grey=(96,96,96)

class Mirror(Piece):

	def place(self,loc, Pieces):
		from Board_Display import Board
		for piece in Pieces:
			if piece.name == 'Mirror Dupe':
				dupe = piece
		self.loc = loc
		self.loc_type = Find_Zone(loc)
		self_pos = Loc_To_Cell(self.loc)
		pg.display.get_surface().blit(Board,[0,0])
		Pieces.update()
		pg.display.flip()
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
					loc = Loc_To_UL(mouse_pos)
					pos = Loc_To_Cell(loc)
					unoccupied = True
					for piece in Pieces:
						if piece.loc==loc:
							unoccupied=False
					if unoccupied and Is_Adjacent(pos,self_pos):
						dupe.place(loc,Pieces)
						self.unselect(Pieces)
						return None

	def remove(self,Pieces):
		dupe_exists = False
		for piece in Pieces:
			if piece.name == 'Mirror Dupe':
				Dupe = piece
		if not Dupe.loc_type in ['draft','hand']:
			loc = Dupe.loc
			Dupe.remove(Pieces)
			self.move(loc,Pieces)
		else:
			temp = pg.PixelArray(self.surface)
			temp.replace((255-255*self.controller,0,255*self.controller),Grey)
			self.surface = temp.make_surface()
			self.surface.set_colorkey(White)
			self.loc = self.draft_loc
			self.loc_type = 'draft'
			self.controller=None

class Mirror_dupe(Piece):

	def place(self,loc, Pieces):
		for piece in Pieces:
			if piece.name =='Mirror':
				self.controller = piece.controller
		temp = pg.PixelArray(self.surface)
		temp.replace(Grey,(255-255*self.controller,0,255*self.controller))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.loc = loc
		self.loc_type = Find_Zone(loc)
		self.unselect(Pieces)

	def update(self):
		if self.loc_type == 'draft':
			self.rect = pg.Rect(0,0,0,0)
		else:
			self.rect = pg.display.get_surface().blit(self.surface,self.loc)


mirror_move = 'Any Adjacent Space'
mirror_ability = 'When placed place a coppy of mirror on any adjacent square'
Mirror = Mirror('Mirror',draw_text_piece('Mir',(96,96,96)),Draft_To_Pix([1,4]),pawn_move,False,'p',mirror_move,mirror_ability)
Mirror_dupe = Mirror_dupe('Mirror Dupe',draw_text_piece('Mir',(96,96,96)),Draft_To_Pix([1,4]),pawn_move,False,'p',mirror_move,mirror_ability)