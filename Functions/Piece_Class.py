from pygame.sprite import Sprite
import pygame as pg
from itertools import product

#Custom scripts
from Images.Piece_images import *
from Functions.text_functions import multiline_text
from Functions.Game_Functions import (Hand_To_Pix, Draft_To_Pix, Pix_To_Hand,Check_If_Blocked,Find_Zone,Get_Current_Piece,Cell_To_Pix,
	White_Lotus_Check,Straight_Line_Intersection,All_Straight_Line_Intersections,Loc_To_Cell,Gaurded,Frozen,By_Portal)

pg.font.init()

#Create the piece class
class Piece(Sprite):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text,Board):
		Sprite.__init__(self)
		self.name=name
		self.loc_type = 'draft'
		self.draft_loc = draft_loc
		self.loc = draft_loc
		self.surface = surface
		self.move_range=move_range
		self.rect = pg.Rect(draft_loc[0],draft_loc[1],71,71)
		self.controller = None
		self.blockable=bloackable
		self.ability_type=ability_type
		self.move_text=move_text
		self.ability_text=ability_text
		self.pos = None
		self.cell_dim = Board.cell_dim
		self.board_height = Board.height
		self.board_start = Board.board_start
		self.font=Board.font


	def display_info(self,Board):
		height = pg.display.get_surface().copy().get_height()
		width = pg.display.get_surface().copy().get_width()
		saved_surface = pg.display.get_surface().copy()
		pg.display.get_surface().fill((255,255,255))
		total_hegith = multiline_text(Board.font,self.move_text, pg.display.get_surface(),[int(round(float(width)/10)),int(round(float(height)/10))])
		multiline_text(Board.font,self.ability_text, pg.display.get_surface(),[int(round(width/10))
			,int(round(float(height)/10+total_hegith+float(height)/10))])
		pg.display.flip()
		done = False
		while not done:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						pg.display.get_surface().blit(saved_surface,[0,0])
						pg.display.flip()
						done = True


	def update(self):
		self.rect = pg.display.get_surface().blit(self.surface,self.loc)

	def select(self):
		temp = pg.PixelArray(self.surface)
		temp.replace((255,255,255),(255,255,0))
		self.surface = temp.make_surface()
		self.update()
		pg.display.flip()


	def unselect(self,Pieces,Board): 
		temp = pg.PixelArray(self.surface)
		temp.replace((255,255,0),(255,255,255))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		Board.update()
		Pieces.update()
		pg.display.flip()

	def legal_move(self,loc,Board,Pieces):
		if loc == None:
			return False
		if White_Lotus_Check(Pieces,self,self.loc,loc)== False:
			return False
		target_pos = Loc_To_Cell(loc,Board)
		if not([self.pos[0]-target_pos[0],self.pos[1]-target_pos[1]] in self.move_range):
			return False
		if self.blockable:
			if Check_If_Blocked(self,target_pos,Pieces):
				print 'The path is blocked.'
				return False
		if Board.turn_name !=self.controller and Board.turn_name!=self.loc_type:
			print 'It is not the right turn to move that piece. THis should never go off.'
			return False
		if Gaurded(target_pos,Pieces,self.controller):
			return False
		if target_pos== [6,6]:
			return True
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def legal_to_move(self,Board,current_player,Pieces):
		if self.controller !=current_player:
			return False
		if Board.turn_name != self.controller and Board.turn_name !=self.loc_type:
			return False
		if self.loc_type == 'hand':
			return False
		if Frozen(self,Pieces):
			return False
		return True


	def move(self,loc,Pieces,Board):
		for piece in Pieces:
			if piece.loc == loc and piece.controller!=self.controller:
				piece.remove(Pieces)
		self.loc=loc
		self.loc_type = Find_Zone(self.pos)
		self.pos = Loc_To_Cell(loc,Board)
		self.unselect(Pieces,Board)

	def remove(self,Pieces):
		temp = pg.PixelArray(self.surface)
		temp.replace((255-255*self.controller,0,255*self.controller),Grey)
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.loc = self.draft_loc
		self.loc_type = 'draft'
		self.place=None
		self.controller=None

	def legal_place(self,loc,Board,Pieces):
		if loc == None:
			return False
		pos = Loc_To_Cell(loc,Board)
		print 'You have selected position: '+str(pos)
		for piece in Pieces:
			if piece.loc == loc:
				print 'Illegal position since there is already a piece there.'
				return False
		if Find_Zone(pos) in ['nutral_zone','goal']:
			print 'Illegal position since in nutral zone or goal'
			return False
		if By_Portal(pos,self,Pieces):
			return True
		if Board.turn_name == self.controller and Find_Zone(pos)!='place_zone':
			print 'Illegal position because that is not in the place zone'
			return False
		if Board.turn_name != self.controller and Find_Zone(pos)!=Board.turn_name:
			print 'Illegal position because that is not in: ' +str(Board.turn_name)
			return False
		return True

	def place(self,loc,Pieces,Board):
		self.loc = loc
		self.pos = Loc_To_Cell(loc,Board)
		self.loc_type = Find_Zone(self.pos)
		self.unselect(Pieces,Board)

	def legal_draft(self,current_player,pieces_to_draft,Pieces,Board):
		hand = []
		for piece in Pieces:
			if piece.controller==current_player and piece.loc_type=='hand':
				hand.append(Pix_To_Hand(piece.loc,Board.cell_dim))
		if len(hand)==7:
			return False
		elif self.controller != None:
			return False
		elif self.loc_type!='draft':
			return False
		elif self in pieces_to_draft:
			return False
		else:
			return True

	def draft(self,current_player,Pieces,Board):
		hand = []
		for piece in Pieces:
			if piece.controller==current_player and piece.loc_type=='hand':
				hand.append(Pix_To_Hand(piece.loc,Board.cell_dim))
		self.controller=current_player
		self.loc_type='hand'
		temp = pg.PixelArray(self.surface)
		temp.replace(Grey,(255-255*current_player,0,255*current_player))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.unselect(Pieces,Board)
		for i in range(1,8):
			if not(i in hand):
				self.loc = Hand_To_Pix(self.controller,i,Board)

	def legal_ability(self,Pieces,Board):
		if Frozen(self,Pieces):
			return False
		return True

	def load(self,piece_info):
		self.loc=piece_info[self.name+'_loc']
		self.pos=piece_info[self.name+'_pos']
		self.loc_type = piece_info[self.name+'_loc_type']
		self.controller = piece_info[self.name+'_controller']
		if self.controller!=None:
			temp = pg.PixelArray(self.surface)
			temp.replace((96,96,96),(255-255*self.controller,0,255*self.controller))
			self.surface = temp.make_surface()
			self.surface.set_colorkey(White)

#Create rooks
rook_move =[]
for i in range(-2,3):
	rook_move=rook_move+[[i,0],[0,i]]

#Create Pawns
pawn_move = []
for i,j in product([-1,0,1],[-1,0,1]):
	pawn_move.append([i,j])

#Create Bishops
bishop_move = []
for i in range(-2,3):
	bishop_move=bishop_move+[[i,i],[i,-i]]

#Create Knights
knight_move = []
for i,j in product([2,-2],[1,-1]):
	knight_move=knight_move+[[i,j],[j,i]]


#Create Queens
queen_move =rook_move+bishop_move

small_bishop_move = [[0,0]]
for i,i in product([1,-1],[1,-1]):
	small_bishop_move.append([i,j])

small_rook_move = [[1,0],[0,1],[-1,0],[0.-1]]
large_rook_move = rook_move +[[3,0],[-3,0],[0,3],[0,-3]]