import pygame as pg
from math import floor, ceil

#Only used in creating of the board
def Grid_To_Pix(x,y,width):
	cell_dim = int(ceil(2*round((float(width)/2-11)/11)+1)/2)
	height = 11*cell_dim+11
	board_start = width-height
	return [int(board_start+(cell_dim+1)*x),int(height-(cell_dim+1)*y)]

def Cell_To_Pix(loc,Board):
	return [int(Board.board_start+(Board.cell_dim+1)*(loc[0]-1)),int(Board.height-(Board.cell_dim+1)*loc[1])]

def Draft_To_Pix(pos,Board):
	gap = int(round((float(Board.height)/2-4*Board.cell_dim)/5))
	return[Board.cell_dim*(pos[0]-1),int(round(float(Board.height)/4))+gap+(gap+Board.cell_dim)*(pos[1]-1)]

def Hand_To_Pix(player,position,Board):
	if player == 1:
		return [int(Board.cell_dim*(position-1)),int(round(float(Board.height)/4))-Board.cell_dim]
	if player ==0:
		return [int(Board.cell_dim*(position-1)),int(round(3*float(Board.height)/4))]

def Pix_To_Hand(loc,cell_dim):
	return round(loc[0]/cell_dim+1)

def Get_Current_Piece(mouse_pos,Pieces):
	for piece in Pieces.sprites():
		if piece.rect.collidepoint(mouse_pos):
			return piece

def Loc_To_UL(loc,Board):
	if loc[0]<Board.board_start:
		UL=None
	else:
		x = Board.board_start+floor(float(loc[0]-Board.board_start)/(Board.cell_dim+1))*(Board.cell_dim+1)
		y = floor(float(loc[1])/(Board.cell_dim+1))*(Board.cell_dim+1)
		UL=[int(x),int(y)]
	return UL

def Loc_To_Cell(loc,Board):
	x=loc[0]
	y=loc[1]
	return [int(floor((x-Board.board_start)/(Board.cell_dim+1)+1)),int(11-floor(float(y)/(Board.cell_dim+1)))]

def Straight_Line_Intersection(pos,Pieces,direction,Board):
	i=1
	while True:
		#print 'now checking Cell: ' + str([pos[0]+direction[0]*i,pos[1]+direction[1]*i])
		temp = Cell_To_Pix([pos[0]+direction[0]*i,pos[1]+direction[1]*i],Board)
		for piece in Pieces:
			if piece.loc == temp:
				return piece
		if (pos[0]+direction[0]*i)<1 or (pos[0]+direction[0]*i)>11 or (pos[1]+direction[1]*i)<1 or (pos[1]+direction[1]*i)>11:
			return None
		i=i+1

def All_Straight_Line_Intersections(pos,Pieces,Board):
	list_of_pieces = []
	list_of_directions =[]
	possible_directions = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]
	for direction in possible_directions:
		temp = Straight_Line_Intersection(pos,Pieces,direction,Board)
		if temp!=None:
			list_of_pieces.append(temp)
			list_of_directions.append(direction)
	return [list_of_pieces,list_of_directions]

def Is_Adjacent(pos1,pos2):
	for offset in [[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]]:
		if pos2 == [pos1[0]+offset[0],pos1[1]+offset[1]]:
			return True
	return False

def Get_Direction(pos1,pos2):
	if pos2[0]-pos1[0]==0:
		x_direction = 0
	elif pos2[0]-pos1[0]<0:
		x_direction = -1
	elif pos2[0]-pos1[0]>0:
		x_direction = 1
	if pos2[1]-pos1[1]==0:
		y_direction = 0
	elif pos2[1]-pos1[1]<0:
		y_direction = -1
	elif pos2[1]-pos1[1]>0:
		y_direction = 1
	return [x_direction,y_direction]

def Check_If_Blocked(current_piece,target_pos,Pieces):
	out = False
	self_pos = current_piece.pos
	direction = Get_Direction(self_pos,target_pos)
	search=[]
	temp = [self_pos[0]+direction[0],self_pos[1]+direction[1]]
	while temp !=target_pos:
		search.append([int(temp[0]),int(temp[1])])
		temp = [temp[0]+direction[0],temp[1]+direction[1]]
	for piece in Pieces:
		if piece.pos in search:
			out = True
	return out

def Find_Zone(pos):
	place_zone = [[1,1],[1,11],[11,11],[11,1]]
	for i in range(2,11):
		place_zone=place_zone+[[1,i],[i,1],[i,11],[11,i]]
	if pos in place_zone:
		return 'place_zone'
	elif pos in [[6,6]]:
		return 'goal'
	elif pos in [[5,4],[6,4],[7,4],[4,5],[5,5],[6,5],[7,5],[8,5],[4,6],[5,6],[7,6],[8,6],[5,8],[6,8],[7,8],[4,7],[5,7],[6,7],[7,7],[8,7]]:
		return 'nutral_zone'
	elif pos in [[8,8],[8,9],[8,10],[9,8],[9,9],[9,10],[10,8],[10,9],[10,10]]:
		return 't1'
	elif pos in [[9,5],[9,6],[9,7],[10,5],[10,6],[10,7]]:
		return 't2'
	elif pos in [[5,3],[6,3],[7,3],[5,2],[6,2],[7,2]]:
		return 't3'
	elif pos in [[8,4],[9,4],[10,4],[8,3],[9,3],[10,3],[8,2],[9,2],[10,2]]:
		return 't4'
	elif pos in [[2,2],[3,2],[4,2],[2,3],[3,3],[4,3],[2,4],[3,4],[4,4]]:
		return 't5'
	elif pos in [[2,5],[2,6],[2,7],[3,5],[3,6],[3,7]]:
		return 't6'
	elif pos in [[5,10],[6,10],[7,10],[5,9],[6,9],[7,9]]:
		return 't7'
	elif pos in [[2,10],[3,10],[4,10],[2,9],[3,9],[4,9],[2,8],[3,8],[4,8]]:
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
def Gaurded(pos,Pieces,current_player):
	for piece in Pieces:
		if piece.name=='Sheild':
			if piece.loc_type in ['draft','hand']:
				return False
			sheild_pos=piece.pos
			sheild_controller=piece.controller
	gaurded_poss=[]
	for offset in [[1,1],[-1,1],[1,-1],[-1,-1]]:
		gaurded_poss.append([sheild_pos[0]+offset[0],sheild_pos[1]+offset[1]])
	for piece in Pieces:
		if piece.pos==pos and (pos in gaurded_poss) and current_player!=sheild.controller:
			return True
	return False

def Frozen(current_piece,Pieces):
	for piece in Pieces:
		if piece.name == 'Ice':
			if piece.loc_type in ['draft','hand']:
				return False
			ice_pos = piece.pos
	for offset in [[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]]:
		if current_piece.pos == [ice_pos[0]+offset[0],ice_pos[1]+offset[1]]:
			return True
	return False

def By_Portal(pos,piece,Pieces):
	for piece in Pieces:
		if piece.name =='Portal':
			if piece.loc_type in ['draft','hand']:
				return False
			if piece.controller!=piece.controller:
				print 'false returned because you dont controll the portal'
				return False
			portal_pos = piece.pos
	for offset in [[1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1],[0,1],[0,-1]]:
		if pos == [portal_pos[0]+offset[0],portal_pos[1]+offset[1]]:
			return True
	return False

#Deals with drafting
def draft_action(current_piece,current_player,Pieces,Board):
	print 'You have entered draft mode'
	current_piece.select()
	pieces_to_draft = [current_piece]
	hand = []
	for piece in Pieces:
		if piece.controller == current_player and piece.loc_type=='hand':
			hand.append(Pix_To_Hand(piece.loc,Board.cell_dim))
	while True:
		#Check to see if you are done draftting
		if len(pieces_to_draft)==min(3,7-len(hand)):
			for piece in pieces_to_draft:
				piece.draft(current_player,Pieces,Board)
			return True
		#Respond to key presses
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					for piece in pieces_to_draft:
						piece.unselect(Pieces,Board)
					return False
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				current_piece = None
				mouse_pos = pg.mouse.get_pos()
				current_piece = Get_Current_Piece(mouse_pos,Pieces)
				if current_piece!= None:
					if current_piece.legal_draft(current_player,pieces_to_draft,Pieces,Board):
						current_piece.select()
						pieces_to_draft.append(current_piece)

#Deals with placing a piece
def place_action(current_piece,current_player,Pieces,Board):
	print 'You have entered place mode'
	current_piece.select()
	while True:
		#Respond to keyboard inputs
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
				print 'You have selected loc: '+str(loc)
				if current_piece.legal_place(loc,Board,Pieces):
					current_piece.place(loc,Pieces,Board)
					return True

#enact the move/ability action after a piece has been selected
def move_ability_action(current_piece,current_player,Pieces,Board):
	print 'Now entering move mode for player ' + str(current_player)
	current_piece.select()
	if current_piece.ability_type == 'a':
		Board.configure_PU('move or use your ability?','move','ability')
		answer = Board.ask_PU()
		if 'ability'==answer:
			return ability_action(current_piece,current_player,Pieces,Board)
		elif 'move'==answer:
			return move_action(current_piece,current_player,Pieces,Board)
		else:
			current_piece.unselect(Pieces,Board)
			return False
	elif current_piece.ability_type == 'p':
		return move_action(current_piece,current_player,Pieces,Board)
	elif current_piece.ability_type =='ma':
		Board.configure_PU('Do you wish to move?','yes','no')
		answer = Board.ask_PU()
		if answer=='yes':
			if False == move_action(current_piece,current_player,Pieces,Board):
				current_piece.unselect(Pieces,Board)
				return False
			Board.update()
			current_piece.select()
			Pieces.update()
			pg.display.flip()
		Board.configure_PU('Use your ability?','yes','no')
		answer = Board.ask_PU()
		if answer == 'yes':
			ability_action(current_piece,current_player,Pieces,Board)
			return True
		else:
			current_piece.unselect(Pieces,Board)
			return True
	elif current_piece.ability_type =='am':
		Board.configure_PU('Use your ability?','yes','no')
		answer = Board.ask_PU()
		if answer == 'yes':
			if ability_action(current_piece,current_player,Pieces,Board)==False:
				current_piece.unselect(Pieces,Board)
				return False
			current_piece.select()
			Board.update()
			Pieces.update()
			pg.display.flip()
		#ask if you wish to move
		Board.configure_PU('Do you wish to move?','yes','no')
		answer = Board.ask_PU()
		if answer == 'yes':
			move_action(current_piece,current_player,Pieces,Board)
			return True
		else:
			current_piece.unselect(Pieces,Board)
			return True

def move_action(current_piece,current_player,Pieces,Board):
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
				if current_piece.legal_move(loc,Board,Pieces):
					current_piece.move(loc,Pieces,Board)
					return True

def ability_action(current_piece,current_player,Pieces,Board):
	if current_piece.legal_ability(Pieces,Board):
		return current_piece.ability(Pieces,Board)
	else:
		current_piece.unselect(Pieces,Board)
		return False