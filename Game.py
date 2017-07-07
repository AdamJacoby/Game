import os, sys
import pygame as pg

#Custom Scripts
from Functions.Game_Functions import *
from Images.Board_Display import Board
from Functions.UI_tools import *
from Functions.Piece_Class import *

#Import indivual pieces
from Pieces.Power import Power
from Pieces.Balance import Balance
from Pieces.Freedom import Freedom
from Pieces.White_Lotus import White_Loctus
from Pieces.Moon import Moon
from Pieces.Leaf import Leaf
from Pieces.Wind import Wind
from Pieces.Rock import Rock
from Pieces.Fire import Fire
from Pieces.Shadow import Shadow
from Pieces.Leadership import Leadership
from Pieces.Wood import Wood
from Pieces.Mirror import Mirror, Mirror_dupe

#Create the board
screen = pg.display.set_mode([1600,793])
Pieces = pg.sprite.Group(Power,Balance,Rook2P0,White_Loctus,Rook2P1,Leadership,Wind,Moon,Chaos,Sun,
	Pawn6P0,Pawn7P0,Wood,Rock,Leaf,Sheild,Freedom,Pawn6P1,Pawn7P1,Shadow,Portal,
	Mirror,Fire,Ice,Infinity,Water,QueenP0,QueenP1,Mirror_dupe)

screen.blit(Board,[0,0])
Pieces.update()
Turn_Indicator=Turn_Indicator()
pop_up=pop_up()
Text_Screen= Text_Screen()
pg.display.flip()

#Some needed variables
Zones = ['place_zone','t1','t2','t3','t4','t5','t6','t7','t8','nutral_zone','goal']

#Main game loop
done = True
finished = False
clock = pg.time.Clock()
current_turn = 0
current_piece = None
hand=[[],[]]

while not finished:
	clock.tick(10)
	#Find out what players turn it is
	if Turn_Indicator.turn_name==0:
		current_player=0
	elif Turn_Indicator.turn_name==1:
		current_player=1
	else:
		count=0
		for piece in Pieces:
			if piece.loc_type == Turn_Indicator.turn_name:
				count = count + 2*piece.controller-1
		if Sun.loc_type == Turn_Indicator.turn_name:
			count = count + 2*Sun.controller-1
		if Chaos.loc_type == Turn_Indicator.turn_name:
			count=0
		if count >=2:
			current_player =1
		elif count<=-2:
			current_player =0
		else:
			current_player=None
	print 'Its players '+str(current_player)+' turn. In terriroty: ' +str(Turn_Indicator.turn_name)


#Move and abality phase
	if current_player != None:#Check to see if there is a player thaat can legally make a move
		for piece in Pieces:
			if piece.controller == current_player and piece.loc_type in Zones and not piece.name in ['Ice','Shadow']:
				done = False
	if done==False:
		if Turn_Indicator.turn_name in [0,1]:
			Text_Screen.configure('Player '+str(current_player)+'\'s general move/abiliry phase')
		else:
			Text_Screen.configure('Player ' +str(current_player) +'\'s move/abiliry phase in'+ Turn_Indicator.turn_name)
		Text_Screen.update()
		pg.display.flip()
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done=True
				finished=True
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					current_piece.display_info()
					current_piece=None
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					if current_piece.legal_to_move(Turn_Indicator,current_player,Pieces):
						done = move_ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up)
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
	screen.blit(Board,[0,0])
	Pieces.update()
	Turn_Indicator.update()
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
			if Turn_Indicator.turn_name in [0,1]:
				Text_Screen.configure('Player '+str(current_player)+'\'s general place/draft phase')
			else:
				Text_Screen.configure('Player ' +str(current_player) +'\'s place/draft phase in'+ Turn_Indicator.turn_name)
		Text_Screen.update()
		pg.display.flip()
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					current_piece.display_info()
					current_piece=None
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!=None:
					if current_piece.legal_draft(current_player,[],Pieces) and len(hand)<=7:
						done = draft_action(current_piece,current_player,Pieces)
					elif current_piece.loc_type =='hand' and current_piece.controller==current_player:
						done = place_action(current_piece,current_player,Pieces,Turn_Indicator)
				else:
					print 'Please select a valid piece.'

	#Refresh screen at the end of that phase
	screen.blit(Board,[0,0])
	Pieces.update()
	Turn_Indicator.next_turn()
	Turn_Indicator.update()
	pg.display.flip()
