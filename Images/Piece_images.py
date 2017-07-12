import pygame as pg
from math import ceil, floor
White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Blue=(51,51,255)
Grey=(96,96,96)

pg.font.init()

def draw_piece_base(color,cell_dim):
	surface = pg.Surface([cell_dim,cell_dim])
	surface.fill(White)
	pg.draw.circle(surface, color, [int(ceil(float(cell_dim)/2)),int(ceil(float(cell_dim)/2))], int(ceil(3*float(cell_dim)/7)))
	surface.set_colorkey(White)
	return surface

def draw_text_piece(text,color,cell_dim):
	surface = draw_piece_base(color,cell_dim)
	text_height=0
	i=1
	while text_height<floor(float(cell_dim)/4):
		font = pg.font.SysFont('Comic Sans MS', i)
		text_height = font.render('text',False,(0,0,0),(255,255,255)).get_height()
		i=i+1
	text = font.render(text,False,(0,0,0),(255,255,255))
	text.set_colorkey((255,255,255))
	surface.blit(text,[round(float((cell_dim-text.get_width()))/2),round(float(cell_dim-(text.get_height()))/2)])
	return surface