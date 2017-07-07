from pygame.sprite import Sprite
import pygame as pg
from itertools import product

#Custom scripts
from Images.Piece_images import *
from Functions.text_functions import multiline_text
from Functions.Game_Functions import (Hand_To_Pix, Draft_To_Pix, Pix_To_Hand,Check_If_Blocked,Find_Zone,Get_Current_Piece,Cell_To_Pix,
	Loc_To_Grid,White_Lotus_Check,Straight_Line_Intersection,All_Straight_Line_Intersections,Loc_To_Cell,Gaurded,Frozen,By_Portal)

pg.font.init()

#Create the piece class
class Piece(Sprite):
	def __init__(self,name,surface, draft_loc,move_range,bloackable,ability_type,move_text,ability_text):
		Sprite.__init__(self)
		self.name=name
		self.font = pg.font.SysFont('Comic Sans MS', 30)
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


	def display_info(self):
		height = pg.display.get_surface().copy().get_height()
		width = pg.display.get_surface().copy().get_width()
		saved_surface = pg.display.get_surface().copy()
		pg.display.get_surface().fill((255,255,255))
		total_hegith = multiline_text(self.font,self.move_text, pg.display.get_surface(),[round(width/10),round(height/10)])
		multiline_text(self.font,self.ability_text, pg.display.get_surface(),[round(width/10),round(height/10+total_hegith+height/10)])
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


	def unselect(self,Pieces): 
		from Images.Board_Display import Board
		temp = pg.PixelArray(self.surface)
		temp.replace((255,255,0),(255,255,255))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		pg.display.get_surface().blit(Board,[0,0])
		Pieces.update()
		pg.display.flip()

	def legal_move(self,loc,Turn_Indicator,Pieces):
		if loc == None:
			return False
		if White_Lotus_Check(Pieces,self,self.loc,loc)== False:
			return False
		target_pos = Loc_To_Grid(loc)
		self_pos = Loc_To_Grid(self.loc)
		if not([self_pos[0]-target_pos[0],self_pos[1]-target_pos[1]] in self.move_range):
			return False
		if self.blockable:
			if Check_If_Blocked(self,target_pos,Pieces):
				print 'The path is blocked.'
				return False
		if Turn_Indicator.turn_name !=self.controller and Turn_Indicator.turn_name!=self.loc_type:
			print 'It is not the right turn to move that piece. THis should never go off.'
			return False
		if Gaurded(loc,Pieces,self.controller):
			return False
		if target_pos== [6,6]:
			return True
		for piece in Pieces:
			if piece.controller == self.controller and piece.loc == loc:
				return False
		return True

	def legal_to_move(self,Turn_Indicator,current_player,Pieces):
		if self.controller !=current_player:
			return False
		if Turn_Indicator.turn_name != self.controller and Turn_Indicator.turn_name !=self.loc_type:
			return False
		if self.loc_type == 'hand':
			return False
		if Frozen(self,Pieces):
			return False
		return True


	def move(self,loc,Pieces):
		for piece in Pieces:
			if piece.loc == loc and piece.controller!=self.controller:
				piece.remove(Pieces)
		self.loc=loc
		self.loc_type = Find_Zone(self.loc)
		self.unselect(Pieces)

	def remove(self,Pieces):
		temp = pg.PixelArray(self.surface)
		temp.replace((255-255*self.controller,0,255*self.controller),Grey)
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.loc = self.draft_loc
		self.loc_type = 'draft'
		self.controller=None

	def legal_place(self,loc,Turn_Indicator,Pieces):
		if loc == None:
			return False
		for piece in Pieces:
			if piece.loc == loc:
				return False
		if Find_Zone(loc) in ['nutral_zone','goal']:
			return False
		if By_Portal(loc,self,Pieces):
			return True
		if Turn_Indicator.turn_name == self.controller and Find_Zone(loc)!='place_zone':
			return False
		if Turn_Indicator.turn_name != self.controller and Find_Zone(loc)!=Turn_Indicator.turn_name:
			return False
		return True

	def place(self,loc,Pieces):
		self.loc = loc
		self.loc_type = Find_Zone(loc)
		self.unselect(Pieces)

	def legal_draft(self,current_player,pieces_to_draft,Pieces):
		hand = []
		for piece in Pieces:
			if piece.controller==current_player and piece.loc_type=='hand':
				hand.append(Pix_To_Hand(piece.loc))
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

	def draft(self,current_player,Pieces):
		hand = []
		for piece in Pieces:
			if piece.controller==current_player and piece.loc_type=='hand':
				hand.append(Pix_To_Hand(piece.loc))
		self.controller=current_player
		self.loc_type='hand'
		temp = pg.PixelArray(self.surface)
		temp.replace(Grey,(255-255*current_player,0,255*current_player))
		self.surface = temp.make_surface()
		self.surface.set_colorkey(White)
		self.unselect(Pieces)
		for i in range(1,8):
			if not(i in hand):
				self.loc = Hand_To_Pix(self.controller,i)

	def legal_ability(self,Pieces,Turn_Indicator):
		if Frozen(self,Pieces):
			return False
		return True

#Create rooks
rook_move =[]
for i in range(-2,3):
	rook_move=rook_move+[[i,0],[0,i]]

Rook2P0=Piece('a',draw_rook(Grey),Draft_To_Pix([6,1]),rook_move,True,'p','stuff','stuff')
Rook2P1=Piece('a',draw_rook(Grey),Draft_To_Pix([6,4]),rook_move,True,'p','stuff','stuff')

#Create Pawns
pawn_move = []
for i,j in product([-1,0,1],[-1,0,1]):
	pawn_move.append([i,j])

Pawn6P0 = Piece('a',draw_pawn(Grey),Draft_To_Pix([6,2]),pawn_move,False,'p','stuff','stuff')
Pawn7P0 = Piece('a',draw_pawn(Grey),Draft_To_Pix([7,2]),pawn_move,False,'p','stuff','stuff')

Pawn6P1 = Piece('a',draw_pawn(Grey),Draft_To_Pix([6,3]),pawn_move,False,'p','stuff','stuff')
Pawn6P1 = Piece('a',draw_pawn(Grey),Draft_To_Pix([6,3]),pawn_move,False,'p','stuff','stuff')
Pawn7P1 = Piece('a',draw_pawn(Grey),Draft_To_Pix([7,3]),pawn_move,False,'p','stuff','stuff')

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

QueenP0=Piece('a',draw_queen(Grey),Draft_To_Pix([7,1]),queen_move,True,'p','stuff','stuff')
QueenP1=Piece('a',draw_queen(Grey),Draft_To_Pix([7,4]),queen_move,True,'p','stuff','stuff')


small_bishop_move = [[0,0]]
for i,i in product([1,-1],[1,-1]):
	small_bishop_move.append([i,j])

small_rook_move = [[1,0],[0,1],[-1,0],[0.-1]]
large_rook_move = rook_move +[[3,0],[-3,0],[0,3],[0,-3]]

#Add pieces whose basic script does not need to be changed from the piece Class

#make the sun piece
sun_move = 'Movement: 1 space in a virtical or horizontal direction'
sun_ability = 'Ability: Counts as two pieces for the purpose of controlling territory'
Sun = Piece('Sun',draw_text_piece('Sun',Grey),Draft_To_Pix([5,2]),small_rook_move,True,'p',sun_move,sun_ability)

#make the chaos piece
chaos_move = 'Movement: Knight moves'
chaos_ability = 'Ability: The territory Chaos is in can not be controller by either player'
Chaos = Piece('Chaos',draw_text_piece('Chs',Grey),Draft_To_Pix([4,2]),knight_move,False,'p',chaos_move,chaos_ability)

#Makse Sheild piece
sheild_move = 'Movement: Knight moves'
sheild_ability = 'Ability: Allied pieces diagonally adjacent to sheild cannot be captured'
Sheild = Piece('Sheild',draw_text_piece('Sld',Grey),Draft_To_Pix([4,3]),knight_move,False,'p',sheild_move,sheild_ability)

#Make Water Piece
water_move = 'Movement: Three spaces in any vertical or horizontal direction, movement cannot be blocked'
water_ability = 'Ability: None'
Water = Piece('Water',draw_text_piece('Wtr',Grey),Draft_To_Pix([4,4]),large_rook_move,False,'p',water_move,water_ability)

#Make Ice Piece
ice_move = 'Movement: None'
ice_ability = 'Ability: Adjacent pieces can move or use abilitys'
Ice = Piece('Ice',draw_text_piece('Ice',Grey),Draft_To_Pix([3,1]),[],False,'p',ice_move,ice_ability)

#Make infinity piece
infinity_move = 'Movement: Can move to all spaces in a 5x5 cube centered on Infinity'
infinity_abilitty = 'Ability: None'
Infinity = Piece('Infinity',draw_text_piece('Infy',Grey),Draft_To_Pix([3,4]),queen_move+knight_move,False,'p',infinity_move,infinity_abilitty)

#Make Portal piece
portal_move = 'Movement: Any adjacent space'
portal_ability = 'Pieces can always be placed in territory cells adjacent to portal'
Portal = Piece('Portal',draw_text_piece('Prtl',Grey),Draft_To_Pix([2,1]),pawn_move,False,'p',portal_move,portal_ability)