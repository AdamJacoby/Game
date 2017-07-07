import pygame as pg
White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Blue=(51,51,255)
Grey=(96,96,96)

pg.font.init()

def draw_piece_base(color):
	surface = pg.Surface([71,71])
	surface.fill(White)
	pg.draw.circle(surface, color, [36,36], 30)
	surface.set_colorkey(White)
	return surface

def draw_rook(color):
	surface = draw_piece_base(color)
	pg.draw.line(surface, Black, [36,66], [36,6],3)
	pg.draw.line(surface, Black, [6,36], [66,36],3)
	return surface

def draw_pawn(color):
	surface = draw_piece_base(color)
	pg.draw.line(surface, Black, [36,51], [36,21],3)
	pg.draw.line(surface, Black, [21,36], [51,36],3)
	pg.draw.line(surface, Black, [36+11,36+11], [36-11,36-11],3)
	pg.draw.line(surface, Black, [36-11,36+11], [36+11,36-11],3)
	return surface

def draw_bishop(color):
	surface = draw_piece_base(color)
	pg.draw.line(surface, Black, [36+21,36+21], [36-21,36-21],3)
	pg.draw.line(surface, Black, [36-21,36+21], [36+21,36-21],3)
	return surface

def draw_knight(color):
	surface = draw_piece_base(color)
	pg.draw.line(surface, Black, [36+24,36], [36-24,36],3)
	pg.draw.line(surface, Black, [36,36+24], [36,36-24],3)
	pg.draw.line(surface, Black, [36+24,36+14], [36+24,36-14],3)
	pg.draw.line(surface, Black, [36-24,36+14], [36-24,36-14],3)
	pg.draw.line(surface, Black, [36+14,36+24], [36-14,36+24],3)
	pg.draw.line(surface, Black, [36+14,36-24], [36-14,36-24],3)
	return surface

def draw_queen(color):
	surface = draw_piece_base(color)
	pg.draw.line(surface, Black, [36+21,36+21], [36-21,36-21],3)
	pg.draw.line(surface, Black, [36-21,36+21], [36+21,36-21],3)
	pg.draw.line(surface, Black, [36,66], [36,6],3)
	pg.draw.line(surface, Black, [6,36], [66,36],3)
	return surface

def draw_text_piece(text,color):
	surface = draw_piece_base(color)
	text = pg.font.SysFont('Comic Sans MS', 30).render(text,False,(0,0,0),(255,255,255))
	text.set_colorkey((255,255,255))
	surface.blit(text,[round(float((71-text.get_width()))/2),round(float(72-(text.get_height()))/2)])
	return surface