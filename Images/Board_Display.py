import pygame as pg
from Functions.Game_Functions import Grid_To_Pix

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

def Create_Board():
	#Create board
	board = pg.Surface([1600,793])
	board.fill(White)

	#Color in the territories
	pg.draw.rect(board, Nogo_color, [Grid_To_Pix(3,8)[0],Grid_To_Pix(3,8)[1],72*5+1,72*5+1])
	pg.draw.rect(board, Goal_color, [Grid_To_Pix(5,6)[0],Grid_To_Pix(5,6)[1],72*1+1,72*1+1])
	pg.draw.rect(board, T1_color, [Grid_To_Pix(7,10)[0],Grid_To_Pix(7,10)[1],72*3+1,72*3+1])
	pg.draw.rect(board, T2_color, [Grid_To_Pix(8,7)[0],Grid_To_Pix(8,7)[1],72*2+1,72*3+1])
	pg.draw.rect(board, T4_color, [Grid_To_Pix(7,4)[0],Grid_To_Pix(7,4)[1],72*3+1,72*3+1])
	pg.draw.rect(board, T3_color, [Grid_To_Pix(4,3)[0],Grid_To_Pix(4,3)[1],72*3+1,72*2+1])
	pg.draw.rect(board, T5_color, [Grid_To_Pix(1,4)[0],Grid_To_Pix(1,4)[1],72*3+1,72*3+1])
	pg.draw.rect(board, T6_color, [Grid_To_Pix(1,7)[0],Grid_To_Pix(1,7)[1],72*2+1,72*3+1])
	pg.draw.rect(board, T8_color, [Grid_To_Pix(1,10)[0],Grid_To_Pix(1,10)[1],72*3+1,72*3+1])
	pg.draw.rect(board, T7_color, [Grid_To_Pix(4,10)[0],Grid_To_Pix(4,10)[1],72*3+1,72*2+1])

	pg.draw.line(board, Black, [807, 0], [1600, 0], 1)
	pg.draw.line(board, Black, [807, 793], [1600, 793], 1)
	pg.draw.line(board, Black, [807, 0], [807,793], 1)
	pg.draw.line(board, Black, [1600, 0], [1600,793], 1)
	for i in range(1,11):#Draw base grid lines
		pg.draw.line(board, Black, [807, 1+72*i], [1600, 72*i+1], 1)#Draw Horizontal grid
		pg.draw.line(board, Black, [807+i*72, 0], [807+i*72,793], 1)#Draw Vertical grid
	#Draw lines to speratte territories
	#Outer lines
	pg.draw.line(board, Black, Grid_To_Pix(1,1),Grid_To_Pix(1,10),3)
	pg.draw.line(board, Black, Grid_To_Pix(1,1),Grid_To_Pix(10,1),3)
	pg.draw.line(board, Black, Grid_To_Pix(1,10),Grid_To_Pix(10,10),3)
	pg.draw.line(board, Black, Grid_To_Pix(10,1),Grid_To_Pix(10,10),3)
	#Conner territories bountries
	pg.draw.line(board, Black, Grid_To_Pix(4,4),Grid_To_Pix(4,1),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,4),Grid_To_Pix(1,4),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,7),Grid_To_Pix(4,10),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,7),Grid_To_Pix(1,7),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,7),Grid_To_Pix(7,10),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,7),Grid_To_Pix(10,7),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,4),Grid_To_Pix(10,4),3)
	pg.draw.line(board, Black, Grid_To_Pix(7,4),Grid_To_Pix(7,1),3)
	#Side territory boundries
	pg.draw.line(board, Black, Grid_To_Pix(4,3),Grid_To_Pix(7,3),3)
	pg.draw.line(board, Black, Grid_To_Pix(3,4),Grid_To_Pix(3,7),3)
	pg.draw.line(board, Black, Grid_To_Pix(4,8),Grid_To_Pix(7,8),3)
	pg.draw.line(board, Black, Grid_To_Pix(8,7),Grid_To_Pix(8,4),3)
	#Draw sides of center box
	pg.draw.line(board, Black, Grid_To_Pix(5,5),Grid_To_Pix(5,6),3)
	pg.draw.line(board, Black, Grid_To_Pix(5,5),Grid_To_Pix(6,5),3)
	pg.draw.line(board, Black, Grid_To_Pix(6,6),Grid_To_Pix(5,6),3)
	pg.draw.line(board, Black, Grid_To_Pix(6,6),Grid_To_Pix(6,5),3)

	#seperate drafing sections and hand
	pg.draw.line(board, Black, [0,198+0*199],[707,198+0*199],3)
	pg.draw.line(board, Black, [0,198+2*199],[707,198+2*199],3)

	#Draw the turn identifier
	pg.draw.line(board, Black, [707,0],[707,793],3)
	pg.draw.rect(board, Red, [738,10,39,39])
	pg.draw.rect(board, T1_color, [738,10+49*1,39,39])
	pg.draw.rect(board, Blue, [738,10+49*2,39,39])
	pg.draw.rect(board, T2_color, [738,10+49*3,39,39])
	pg.draw.rect(board, Red, [738,10+49*4,39,39])
	pg.draw.rect(board, T3_color, [738,10+49*5,39,39])
	pg.draw.rect(board, Blue, [738,10+49*6,39,39])
	pg.draw.rect(board, T4_color, [738,10+49*7,39,39])
	pg.draw.rect(board, Red, [738,10+49*8,39,39])
	pg.draw.rect(board, T5_color, [738,10+49*9,39,39])
	pg.draw.rect(board, Blue, [738,10+49*10,39,39])
	pg.draw.rect(board, T6_color, [738,10+49*11,39,39])
	pg.draw.rect(board, Red, [738,10+49*12,39,39])
	pg.draw.rect(board, T7_color, [738,10+49*13,39,39])
	pg.draw.rect(board, Blue, [738,10+49*14,39,39])
	pg.draw.rect(board, T8_color, [738,10+49*15,39,39])
	return board
Board = Create_Board()