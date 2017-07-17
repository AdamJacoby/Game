import os, sys
import pygame as pg
import pymongo

#client = pymongo.MongoClient()
client = None

from Functions.Save_Functions import *

#Set up resolution options
from Functions.UI_tools import *
width=Get_Number('Input Horizontal Resolution')
cell_dim = int(ceil(2*round((float(width)/2-11)/11)+1)/2)
height = 11*cell_dim+11
screen = pg.display.set_mode([width,height])
Board = Board(width)

#Custom Scripts
from Functions.Game_Functions import *
print 'Game Functions imported!'
from Functions.Piece_Class import *
print 'Piece class imported!'
from Images.Piece_images import draw_text_piece

#make the sun piece
sun_move = 'Movement: 1 space in a virtical or horizontal direction'
sun_ability = 'Ability: Counts as two pieces for the purpose of controlling territory'
Sun = Piece('Sun',draw_text_piece('Sun',Grey,cell_dim),Draft_To_Pix([5,2],Board),small_rook_move,True,'p',sun_move,sun_ability,Board)

#make the chaos piece
chaos_move = 'Movement: Knight moves'
chaos_ability = 'Ability: The territory Chaos is in can not be controller by either player'
Chaos = Piece('Chaos',draw_text_piece('Chs',Grey,cell_dim),Draft_To_Pix([4,2],Board),knight_move,False,'p',chaos_move,chaos_ability,Board)

#Makse Sheild piece
sheild_move = 'Movement: Knight moves'
sheild_ability = 'Ability: Allied pieces diagonally adjacent to sheild cannot be captured'
Sheild = Piece('Sheild',draw_text_piece('Sld',Grey,cell_dim),Draft_To_Pix([4,3],Board),knight_move,False,'p',sheild_move,sheild_ability,Board)

#Make Water Piece
water_move = 'Movement: Three spaces in any vertical or horizontal direction, movement cannot be blocked'
water_ability = 'Ability: None'
Water = Piece('Water',draw_text_piece('Wtr',Grey,cell_dim),Draft_To_Pix([4,4],Board),large_rook_move,False,'p',water_move,water_ability,Board)

#Make Ice Piece
ice_move = 'Movement: None'
ice_ability = 'Ability: Adjacent pieces can move or use abilitys'
Ice = Piece('Ice',draw_text_piece('Ice',Grey,cell_dim),Draft_To_Pix([3,1],Board),[],False,'p',ice_move,ice_ability,Board)

#Make infinity piece
infinity_move = 'Movement: Can move to all spaces in a 5x5 cube centered on Infinity'
infinity_abilitty = 'Ability: None'
Infinity = Piece('Infinity',draw_text_piece('Infy',Grey,cell_dim),Draft_To_Pix([3,4],Board),queen_move+knight_move,False,'p',infinity_move,infinity_abilitty,Board)

#Make Portal piece
portal_move = 'Movement: Any adjacent space'
portal_ability = 'Pieces can always be placed in territory cells adjacent to portal'
Portal = Piece('Portal',draw_text_piece('Prtl',Grey,cell_dim),Draft_To_Pix([2,1],Board),pawn_move,False,'p',portal_move,portal_ability,Board)

#Import indivual pieces
from Pieces.Power import Power
power_move = 'Movement: Two spaces in any vertical or horizontal direction'
power_ability = 'Ability: After moving can push any unblocked piece in a straight line direction 1 space back'
Power = Power('Power',draw_text_piece('Pwr',Grey,cell_dim),Draft_To_Pix([4,1],Board),rook_move,True,'ma',power_move,power_ability,Board)
from Pieces.Balance import Balance
balance_move = 'Movement: Two paces in vertical or horizontal directions'
balance_ability = 'Ability: Instead of moving can swap places witth an enemy piece not in the goal or nutral zone'
Balance = Balance('Balance',draw_text_piece('Bal',(96,96,96),cell_dim),Draft_To_Pix([5,1],Board),rook_move,True,'a',balance_move,balance_ability,Board)
from Pieces.Freedom import Freedom
freedom_move = 'Movement: Two space in vertical and horizontal directions'
freedom_ability = 'Ability: Can be placed in territories'
Freedom = Freedom('Freedom',draw_text_piece('Fre',(96,96,96),cell_dim),Draft_To_Pix([5,3],Board),rook_move,True,'p',freedom_move,freedom_ability,Board)
from Pieces.White_Lotus import White_Lotus
white_lotus_move = 'Movement: Two spaces in diagonal directions'
white_lotus_ability = 'Ability: Pieces cannot leave the 7x7 square centered on the White Lotus'
White_Loctus = White_Lotus('White Lotus',draw_text_piece('Lts',(96,96,96),cell_dim),Draft_To_Pix([5,4],Board),bishop_move,True,'p',white_lotus_move,white_lotus_ability,Board)
from Pieces.Moon import Moon
moon_move = 'Movement: Two spaces in any diagonal direction'
mone_ability = 'Ability: Before moving can pull any unblocked piece in a straight line direction 1 space back'
Moon = Moon('Moon',draw_text_piece('Moon',Grey,cell_dim),Draft_To_Pix([3,2],Board),bishop_move,True,'am',moon_move,mone_ability,Board)
from Pieces.Leaf import Leaf
leaf_move = 'Movement: Knight moves'
leaf_ability = 'Ability: Before moving can swap places with any allied piece'
Leaf = Leaf('Leaf',draw_text_piece('Lf',(96,96,96),cell_dim),Draft_To_Pix([3,3],Board),knight_move,False,'am',leaf_move,leaf_ability,Board)
from Pieces.Wind import Wind
wind_move = 'Movement: Any adjacent square'
wind_ability = 'After moving can move any allied piece to any unoccupied adjacent square'
Wind = Wind('Wnd',draw_text_piece('Wind',(96,96,96),cell_dim),Draft_To_Pix([2,2],Board),pawn_move,False,'ma',wind_move,wind_ability,Board)
from Pieces.Rock import Rock
rock_move=rook_move+[[1,1],[1,-1],[-1,1],[-1,-1]]
rock_movement = 'Movement: Any adjacent space or two spaces in a vertical or horizontal direction'
rock_ability = 'Ability: If you hand is not full Rock returns to your hand when removed'
Rock = Rock('Rock',draw_text_piece('Rck',(96,96,96),cell_dim),Draft_To_Pix([2,3],Board),rock_move,True,'p',rock_movement,rock_ability,Board)
from Pieces.Fire import Fire
fire_move = 'Movement: Knight moves'
fire_ability = 'Ability: After taking a piece can move again to an adjacent square'
Fire = Fire('Fire',draw_text_piece('Fire',(96,96,96),cell_dim),Draft_To_Pix([2,4],Board),knight_move,False,'a',fire_move,fire_ability,Board)
from Pieces.Shadow import Shadow
shadow_movement = 'Movement: None'
shadow_ability = 'Ability: Can move next to any allied piece as if it were a normal move'
Shadow = Shadow('Shadow',draw_text_piece('Shdw',(96,96,96),cell_dim),Draft_To_Pix([1,1],Board),[[0,0]],False,'a',shadow_movement,shadow_ability,Board)
from Pieces.Leadership import Leadership
leadership_move = 'Movement: Two spaces in any diagonal direction'
leadership_ability = 'Ability: Can give its turn to any allied piece'
Leadership = Leadership('Leadership',draw_text_piece('Ldr',(96,96,96),cell_dim),Draft_To_Pix([1,2],Board),bishop_move,True,'a',leadership_move,leadership_ability,Board)
from Pieces.Wood import Wood
wood_move = 'Movement: Any adjacent square'
wood_ability = 'Ability: instead of moving can remove an unblocked piece two spaces alway in a straight line'
Wood = Wood('Wood',draw_text_piece('Wd',(96,96,96),cell_dim),Draft_To_Pix([1,3],Board),pawn_move,False,'a',queen_move,wood_move,wood_ability,Board)
from Pieces.Mirror import Mirror, Mirror_dupe
mirror_move = 'Any Adjacent Space'
mirror_ability = 'When placed place a coppy of mirror on any adjacent square'
Mirror = Mirror('Mirror',draw_text_piece('Mir',(96,96,96),cell_dim),Draft_To_Pix([1,4],Board),pawn_move,False,'p',mirror_move,mirror_ability,Board)
Mirror_dupe = Mirror_dupe('Mirror Dupe',draw_text_piece('Mir',(96,96,96),cell_dim),Draft_To_Pix([1,4],Board),pawn_move,False,'p',mirror_move,mirror_ability,Board)

Pieces = pg.sprite.Group(Power,Balance,White_Loctus,Leadership,Wind,Moon,Chaos,Sun,
	Wood,Rock,Leaf,Sheild,Freedom,Shadow,Portal,Mirror,Fire,Ice,Infinity,Water,Mirror_dupe)
#Start new save file or load from save
Board.configure_PU('Load Game or New Game','Load','New')
file_type = Board.ask_PU()
if file_type =='New':
	save_dict = New_Save(client)
elif file_type == 'Load':
	game_number=Get_Number('Input game file number:')
	[piece_info,save_dict] = Load(int(game_number),client)
	for piece in Pieces:
		piece.load(piece_info)
	Board.load(save_dict['turn number'])

Board.update()
Pieces.update()
pg.display.flip()

#Some needed variables
Zones = ['place_zone','t1','t2','t3','t4','t5','t6','t7','t8','nutral_zone','goal']

#Main game loop
done = True
finished = False
clock = pg.time.Clock()
current_piece = None

while not finished:
	clock.tick(10)
	#Find out what players turn it is
	if Board.turn_name==0:
		current_player=0
	elif Board.turn_name==1:
		current_player=1
	else:
		count=0
		for piece in Pieces:
			if piece.loc_type == Board.turn_name:
				count = count + 2*piece.controller-1
		if Sun.loc_type == Board.turn_name:
			count = count + 2*Sun.controller-1
		if Chaos.loc_type == Board.turn_name:
			count=0
		if count >=2:
			current_player =1
		elif count<=-2:
			current_player =0
		else:
			current_player=None
			print 'skipping turn'+Board.turn_name
	print 'Its players '+str(current_player)+' turn. In terriroty: ' +str(Board.turn_name)


#Move and abality phase
	if current_player != None:#Check to see if there is a player thaat can legally make a move
		for piece in Pieces:
			if piece.controller == current_player and piece.loc_type in Zones and not piece.name in ['Ice','Shadow'] and not Frozen(piece,Pieces):
				done = False
	if done==False:
		if Board.turn_name in [0,1]:
			Board.configure_TS('Player '+str(current_player)+'\'s general move/abiliry phase')
		else:
			Board.configure_TS('Player ' +str(current_player) +'\'s move/abiliry phase in'+ Board.turn_name)
		Board.update_TS()
		pg.display.flip()
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					current_piece.display_info(Board)
					current_piece=None
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					if current_piece.legal_to_move(Board,current_player,Pieces):
						done = move_ability_action(current_piece,current_player,Pieces,Board)
					else:
						print ' you cant interact with that piece now.'

	#Check victory condition
	count=0
	for piece in Pieces:
		if piece.loc_type == 'goal':
			count = count + 2*piece.controller-1
	if count >=2:
		print 'Player 1 wins'
		quit()
	if count<=-2:
		print 'Player 0 wins'
		quit()
	#Refress the image att end of move phase
	Board.update()
	Pieces.update()
	pg.display.flip()

	#Draft and placement phase
	done = True
	if current_player != None:
		pieces_in_draft = 0
		for piece in Pieces:
			if piece.loc_type == 'draft':
				pieces_in_draft = pieces_in_draft+1
		hand_length=0
		for piece in Pieces:
			if piece.controller==current_player and piece.loc_type =='hand':
				hand_length = hand_length+1
		if hand_length!=0 or pieces_in_draft!=0:
			done = False
			if Board.turn_name in [0,1]:
				Board.configure_TS('Player '+str(current_player)+'\'s general place/draft phase')
			else:
				Board.configure_TS('Player ' +str(current_player) +'\'s place/draft phase in '+str(Board.turn_name))
		Board.update_TS()
		pg.display.flip()
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					current_piece.display_info(Board)
					current_piece=None
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					if current_piece.legal_draft(current_player,[],Pieces,Board) and hand_length<=7:
						done = draft_action(current_piece,current_player,Pieces,Board)
					elif current_piece.loc_type =='hand' and current_piece.controller==current_player:
						done = place_action(current_piece,current_player,Pieces,Board)
				else:
					print 'Please select a valid piece.'

	#Refresh screen at the end of that phase
	
	Board.next_turn()
	save_dict['turn number']=save_dict['turn number']+1
	Board.update()
	Pieces.update()
	pg.display.flip()

	Save(Pieces,save_dict,client)
