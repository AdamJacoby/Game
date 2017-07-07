import pygame as pg
from math import floor, ceil
from Functions.UI_tools import pop_up


def Grid_To_Pix(x,y):
	return [int(807+72*x),int(793-72*y)]

def Cell_To_Pix(x,y,*arg):
	if len(arg)==0:
		return [int(807+32+72*(x-1)),int(793-32-72*(y-1))]
	else:
		if arg[0]=='c':
			return [807+32+72*(x-1),793-32-72*(y-1)]
		if arg[0]=='ul':
			return Grid_To_Pix(int(x-1),int(y))
		if arg[0]=='ll':
			return Grid_To_Pix(x-1,y-1)
		if arg[0]=='ur':
			return Grid_To_Pix(x,y)
		if arg[0]=='lr':
			return Grid_To_Pix(x,y-1)

def Draft_To_Pix(pos):
	return[71*(pos[0]-1),793-(198+94*pos[1])]

def Hand_To_Pix(player,position):
	if player == 1:
		return [int(71*(position-1)),int(19+71)]
	if player ==0:
		return [int(71*(position-1)),198+2*199+19]

def Pix_To_Hand(loc):
	return round(loc[0]/71+1)

def Get_Current_Piece(mouse_pos,Pieces):
	for piece in Pieces.sprites():
		if piece.rect.collidepoint(mouse_pos):
			return piece

def Loc_To_UL(loc):
	if loc[0]<807:
		UL=None
	else:
		x = 807+floor((loc[0]-807)/72)*72
		y = 793-(ceil((793-loc[1])/72)+1)*72
		UL=[int(x),int(y)]
	return UL

def Loc_To_Grid(loc):
	x=loc[0]
	y=loc[1]
	return [int(floor((x-807)/72)+1),int(11-floor((y-1)/72))]

def Loc_To_Cell(loc):
	x=loc[0]
	y=loc[1]
	return [int(floor((x-807)/72)+1),int(11-floor((y-1)/72))]

def Straight_Line_Intersection(loc,Pieces,direction):
	pos = Loc_To_Cell(loc)
	i=1
	while True:
		#print 'now checking Cell: ' + str([pos[0]+direction[0]*i,pos[1]+direction[1]*i])
		temp = Cell_To_Pix(pos[0]+direction[0]*i,pos[1]+direction[1]*i,'ul')
		for piece in Pieces:
			if piece.loc == temp:
				return piece
		if (pos[0]+direction[0]*i)<1 or (pos[0]+direction[0]*i)>11 or (pos[1]+direction[1]*i)<1 or (pos[1]+direction[1]*i)>11:
			return None
		i=i+1

def All_Straight_Line_Intersections(loc,Pieces):
	list_of_pieces = []
	list_of_directions =[]
	possible_directions = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]
	for direction in possible_directions:
		temp = Straight_Line_Intersection(loc,Pieces,direction)
		#if temp == None:
		#	print 'In direction ' +str(direction)+' there are no interections'
		#else:
		#	print 'In direction ' +str(direction)+' we intersenct '+temp.name
		if temp!=None:
			list_of_pieces.append(temp)
			list_of_directions.append(direction)
	return [list_of_pieces,list_of_directions]

def Is_Adjacent(pos1,pos2):
	for offset in [[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]]:
		if pos2 == [pos1[0]+offset[0],pos1[1]+offset[1]]:
			return True
	return False


def Check_If_Blocked(current_piece,target_grid,Pieces):
	out = False
	self_grid = Loc_To_Grid(current_piece.loc)
	if target_grid[0]-self_grid[0]==0:
		x_direction = 0
	elif target_grid[0]-self_grid[0]<0:
		x_direction = -1
	elif target_grid[0]-self_grid[0]>0:
		x_direction = 1
	if target_grid[1]-self_grid[1]==0:
		y_direction = 0
	elif target_grid[1]-self_grid[1]<0:
		y_direction = -1
	elif target_grid[1]-self_grid[1]>0:
		y_direction = 1
	search=[]
	temp = [self_grid[0]+x_direction,self_grid[1]+y_direction]
	while temp !=target_grid:
		search.append([int(temp[0]),int(temp[1])])
		temp = [temp[0]+x_direction,temp[1]+y_direction]
	for piece in Pieces:
		piece_grid = Loc_To_Grid(piece.loc)
		if piece_grid in search:
			out = True
	return out

def Find_Zone(loc):
	loc_grid = Loc_To_Grid(loc)
	place_zone = [[1,1],[1,11],[11,11],[11,1]]
	for i in range(2,11):
		place_zone=place_zone+[[1,i],[i,1],[i,11],[11,i]]
	if loc_grid in place_zone:
		return 'place_zone'
	elif loc_grid in [[6,6]]:
		return 'goal'
	elif loc_grid in [[5,4],[6,4],[7,4],[4,5],[5,5],[6,5],[7,5],[8,5],[4,6],[5,6],[7,6],[8,6],[5,8],[6,8],[7,8],[4,7],[5,7],[6,7],[7,7],[8,7]]:
		return 'nutral_zone'
	elif loc_grid in [[8,8],[8,9],[8,10],[9,8],[9,9],[9,10],[10,8],[10,9],[10,10]]:
		return 't1'
	elif loc_grid in [[9,5],[9,6],[9,7],[10,5],[10,6],[10,7]]:
		return 't2'
	elif loc_grid in [[5,3],[6,3],[7,3],[5,2],[6,2],[7,2]]:
		return 't3'
	elif loc_grid in [[8,4],[9,4],[10,4],[8,3],[9,3],[10,3],[8,2],[9,2],[10,2]]:
		return 't4'
	elif loc_grid in [[2,2],[3,2],[4,2],[2,3],[3,3],[4,3],[2,4],[3,4],[4,4]]:
		return 't5'
	elif loc_grid in [[2,5],[2,6],[2,7],[3,5],[3,6],[3,7]]:
		return 't6'
	elif loc_grid in [[5,10],[6,10],[7,10],[5,9],[6,9],[7,9]]:
		return 't7'
	elif loc_grid in [[2,10],[3,10],[4,10],[2,9],[3,9],[4,9],[2,8],[3,8],[4,8]]:
		return 't8'

def White_Lotus_Check(Pieces,current_piece,start_loc,end_loc):
	for piece in Pieces:
		if piece.name == 'White Lotus':
			wl = piece
	if current_piece.name == 'White Lotus':
		return True
	if wl.boundry == None:
		return True
	if wl.boundry.collidepoint(start_loc) and not(wl.boundry.collidepoint(end_loc)):
		return False
	return True

#Checks to see if a location is gaurded by sheild
def Gaurded(loc,Pieces,current_player):
	for piece in Pieces:
		if piece.name=='Sheild':
			if piece.loc_type in ['draft','hand']:
				return False
			sheild_pos=Loc_To_Cell(piece.loc)
			sheild_controller=piece.controller
	gaurded_locs=[]
	for offset in [[1,1],[-1,1],[1,-1],[-1,-1]]:
		gaurded_locs.append(Cell_To_Pix(sheild_pos[0]+offset[0],sheild_pos[1]+offset[1],'ul'))
	for piece in Pieces:
		if piece.loc==loc and (loc in gaurded_locs) and current_player!=sheild.controller:
			return True
	return False

def Frozen(current_piece,Pieces):
	for piece in Pieces:
		if piece.name == 'Ice':
			if piece.loc_type in ['draft','hand']:
				return False
			ice_pos = Loc_To_Cell(piece.loc)
	pos = Loc_To_Cell(current_piece.loc)
	for offset in [[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]]:
		if pos == [ice_pos[0]+offset[0],ice_pos[1]+offset[1]]:
			return True
	return False

def By_Portal(loc,piece,Pieces):
	for piece in Pieces:
		if piece.name =='Portal':
			if piece.loc_type in ['draft','hand']:
				return False
			if piece.controller!=piece.controller:
				print 'false returned because you dont controll the portal'
				return False
			portal_pos = Loc_To_Cell(piece.loc)
	pos = Loc_To_Cell(loc)
	for offset in [[1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1],[0,1],[0,-1]]:
		if pos == [portal_pos[0]+offset[0],portal_pos[1]+offset[1]]:
			return True
	return False

#Deals with drafting
def draft_action(current_piece,current_player,Pieces):
	print 'You have entered draft mode'
	current_piece.select()
	pieces_to_draft = [current_piece]
	hand = []
	for piece in Pieces:
		if piece.controller == current_player and piece.loc_type=='hand':
			hand.append(Pix_To_Hand(piece.loc))
	while True:
		#Check to see if you are done draftting
		if len(pieces_to_draft)==min(3,7-len(hand)):
			for piece in pieces_to_draft:
				piece.draft(current_player,Pieces)
			return True
		#Respond to key presses
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					for piece in pieces_to_draft:
						piece.unselect(Pieces)
					return False
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				current_piece = None
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!= None:
					if current_piece.legal_draft(current_player,pieces_to_draft,Pieces):
						current_piece.select()
						pieces_to_draft.append(current_piece)

#Deals with placing a piece
def place_action(current_piece,current_player,Pieces,Turn_Indicator):
	print 'You have entered place mode'
	current_piece.select()
	while True:
		#Respond to keyboard inputs
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
				if current_piece.legal_place(loc,Turn_Indicator,Pieces):
					current_piece.place(loc,Pieces)
					return True

#enact the move/ability action after a piece has been selected
def move_ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up):
	from Images.Board_Display import Board
	print 'Now entering move mode for player ' + str(current_player)
	current_piece.select()
	if current_piece.ability_type == 'a':
		pop_up.configure('move or use your ability?','move','ability')
		answer = pop_up.ask()
		if 'ability'==answer:
			return ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up)
		elif 'move'==answer:
			return move_action(current_piece,current_player,Pieces,Turn_Indicator)
		else:
			current_piece.unselect(Pieces)
			return False
	elif current_piece.ability_type == 'p':
		return move_action(current_piece,current_player,Pieces,Turn_Indicator)
	elif current_piece.ability_type =='ma':
		pop_up.configure('Do you wish to move?','yes','no')
		answer = pop_up.ask()
		if answer=='yes':
			if False == move_action(current_piece,current_player,Pieces,Turn_Indicator):
				current_piece.unselect(Pieces)
				return False
			pg.display.get_surface().blit(Board,[0,0])
			current_piece.select()
			Pieces.update()
			pg.display.flip()
		pop_up.configure('Use your ability?','yes','no')
		answer = pop_up.ask()
		if answer == 'yes':
			ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up)
			return True
		else:
			current_piece.unselect(Pieces)
			return True
	elif current_piece.ability_type =='am':
		pop_up.configure('Use your ability?','yes','no')
		answer = pop_up.ask()
		if answer == 'yes':
			if ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up)==False:
				current_piece.unselect(Pieces)
				return False
			current_piece.select()
			pg.display.get_surface().blit(Board,[0,0])
			Pieces.update()
			pg.display.flip()
		#ask if you wish to move
		pop_up.configure('Do you wish to move?','yes','no')
		answer = pop_up.ask()
		if answer == 'yes':
			move_action(current_piece,current_player,Pieces,Turn_Indicator)
			return True
		else:
			current_piece.unselect(Pieces)
			return True

def move_action(current_piece,current_player,Pieces,Turn_Indicator):
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
				if current_piece.legal_move(loc,Turn_Indicator,Pieces):
					current_piece.move(loc,Pieces)
					return True

def ability_action(current_piece,current_player,Pieces,Turn_Indicator,pop_up):
	if current_piece.legal_ability(Pieces,Turn_Indicator):
		return current_piece.ability(Pieces,Turn_Indicator,pop_up)
	else:
		current_piece.unselect(Pieces)
		return False