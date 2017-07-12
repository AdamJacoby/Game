from pygame.sprite import Sprite
import pygame as pg
from Functions.Game_Functions import Grid_To_Pix
from math import ceil,floor

#Set Colors
White = (255,255,255)
Black = (0,0,0)
Red=(255,0,0)
Blue=(51,51,255)
Goal_color = (204,204,0)
Nogo_color = (192,192,192)
T1_color = (144,238,144)
T2_color = (153,51,255)
T3_color = (102,255,255)
T4_color = (0,255,0)
T5_color = (255,255,102)
T6_color = (255,102,178)
T7_color = (255,153,51)
T8_color = (102,102,255)

def Create_Board(width):
	cell_dim = int(ceil(2*round((float(width)/2-11)/11)+1)/2)
	height = 11*cell_dim+11
	print 'the height is: '+str(height)
	board_start = width-height
	#Create board
	board = pg.Surface([width,height])#board = pg.Surface([1600,793])
	board.fill(White)

	#Color in the territories
	pg.draw.rect(board, Nogo_color, [Grid_To_Pix(3,8,width)[0],Grid_To_Pix(3,8,width)[1],(cell_dim+1)*5+1,(cell_dim+1)*5+1])
	pg.draw.rect(board, Goal_color, [Grid_To_Pix(5,6,width)[0],Grid_To_Pix(5,6,width)[1],(cell_dim+1)*1+1,(cell_dim+1)*1+1])
	pg.draw.rect(board, T1_color, [Grid_To_Pix(7,10,width)[0],Grid_To_Pix(7,10,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T2_color, [Grid_To_Pix(8,7,width)[0],Grid_To_Pix(8,7,width)[1],(cell_dim+1)*2+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T4_color, [Grid_To_Pix(7,4,width)[0],Grid_To_Pix(7,4,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T3_color, [Grid_To_Pix(4,3,width)[0],Grid_To_Pix(4,3,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*2+1])
	pg.draw.rect(board, T5_color, [Grid_To_Pix(1,4,width)[0],Grid_To_Pix(1,4,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T6_color, [Grid_To_Pix(1,7,width)[0],Grid_To_Pix(1,7,width)[1],(cell_dim+1)*2+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T8_color, [Grid_To_Pix(1,10,width)[0],Grid_To_Pix(1,10,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*3+1])
	pg.draw.rect(board, T7_color, [Grid_To_Pix(4,10,width)[0],Grid_To_Pix(4,10,width)[1],(cell_dim+1)*3+1,(cell_dim+1)*2+1])

	pg.draw.line(board, Black, [board_start, 0], [board_start,height], 1)#Draw line on left boarder of the board
	pg.draw.line(board, Black, [board_start, 0], [width,0], 1)#Draw line on top boarder of the board
	for i in range(1,11):#Draw base grid lines
		pg.draw.line(board, Black, [board_start, (cell_dim+1)*i], [width, (cell_dim+1)*i], 1)#Draw Horizontal grid
		pg.draw.line(board, Black, [board_start+i*(cell_dim+1), 0], [board_start+i*(cell_dim+1),height], 1)#Draw Vertical grid
	#Draw lines to speratte territories
	#Outer lines
	pg.draw.line(board, Black, Grid_To_Pix(1,1,width),Grid_To_Pix(1,10,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(1,1,width),Grid_To_Pix(10,1,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(1,10,width),Grid_To_Pix(10,10,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(10,1,width),Grid_To_Pix(10,10,width),3)
	#Conner territories bountries
	pg.draw.line(board, Black, Grid_To_Pix(4,4,width),Grid_To_Pix(4,1,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,4,width),Grid_To_Pix(1,4,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,7,width),Grid_To_Pix(4,10,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,7,width),Grid_To_Pix(1,7,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,7,width),Grid_To_Pix(7,10,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,7,width),Grid_To_Pix(10,7,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,4,width),Grid_To_Pix(10,4,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,4,width),Grid_To_Pix(7,1,width),3)
	#Side territory boundries
	pg.draw.line(board, Black, Grid_To_Pix(4,3,width),Grid_To_Pix(7,3,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(3,4,width),Grid_To_Pix(3,7,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,8,width),Grid_To_Pix(7,8,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(8,7,width),Grid_To_Pix(8,4,width),3)
	#Draw sides of center box
	pg.draw.line(board, Black, Grid_To_Pix(5,5,width),Grid_To_Pix(5,6,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(5,5,width),Grid_To_Pix(6,5,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(6,6,width),Grid_To_Pix(5,6,width),3)
	pg.draw.line(board, Black, Grid_To_Pix(6,6,width),Grid_To_Pix(6,5,width),3)

	#seperate drafing sections and hand
	pg.draw.line(board, Black, [0,int(round(float(height)/4))],[int(round(float(7)/8*board_start)),int(round(float(height)/4))],3)
	pg.draw.line(board, Black, [0,int(round(3*float(height)/4))],[int(round(float(7)/8*board_start)),int(round(3*float(height)/4))],3)

	#Draw the turn identifier
	strip_width = int(board_start-round((float(7)/8)*board_start))
	box_dim = int(round(float(height)/(16+float(17)/4)))
	gap_dim = int(floor(float(height-16*box_dim)/17))
	left_side = int(round((float(7)/8)*board_start)+round(float(strip_width-box_dim)/2))
	pg.draw.line(board, Black, [int(round(float(7)/8*board_start)),0],[int(round(float(7)/8*board_start)),height],3)
	pg.draw.rect(board, Red, [left_side,gap_dim,box_dim,box_dim])
	pg.draw.rect(board, T1_color, [left_side,gap_dim+(gap_dim+box_dim)*1,box_dim,box_dim])
	pg.draw.rect(board, Blue, [left_side,gap_dim+(gap_dim+box_dim)*2,box_dim,box_dim])
	pg.draw.rect(board, T2_color, [left_side,gap_dim+(gap_dim+box_dim)*3,box_dim,box_dim])
	pg.draw.rect(board, Red, [left_side,gap_dim+(gap_dim+box_dim)*4,box_dim,box_dim])
	pg.draw.rect(board, T3_color, [left_side,gap_dim+(gap_dim+box_dim)*5,box_dim,box_dim])
	pg.draw.rect(board, Blue, [left_side,gap_dim+(gap_dim+box_dim)*6,box_dim,box_dim])
	pg.draw.rect(board, T4_color, [left_side,gap_dim+(gap_dim+box_dim)*7,box_dim,box_dim])
	pg.draw.rect(board, Red, [left_side,gap_dim+(gap_dim+box_dim)*8,box_dim,box_dim])
	pg.draw.rect(board, T5_color, [left_side,gap_dim+(gap_dim+box_dim)*9,box_dim,box_dim])
	pg.draw.rect(board, Blue, [left_side,gap_dim+(gap_dim+box_dim)*10,box_dim,box_dim])
	pg.draw.rect(board, T6_color, [left_side,gap_dim+(gap_dim+box_dim)*11,box_dim,box_dim])
	pg.draw.rect(board, Red, [left_side,gap_dim+(gap_dim+box_dim)*12,box_dim,box_dim])
	pg.draw.rect(board, T7_color, [left_side,gap_dim+(gap_dim+box_dim)*13,box_dim,box_dim])
	pg.draw.rect(board, Blue, [left_side,gap_dim+(gap_dim+box_dim)*14,box_dim,box_dim])
	pg.draw.rect(board, T8_color, [left_side,gap_dim+(gap_dim+box_dim)*15,box_dim,box_dim])
	return board