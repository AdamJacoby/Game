import pygame as pg

#Blits multi line sof tex to a surface lines need to be serparated by a *
def multiline_text(font,text,surface,loc):
	temp = text.split('*')
	lines = []
	for line in temp:
		lines.append(font.render(line,False,(0,0,0),(255,255,255)))
	for i in range(0,len(lines)):
		surface.blit(lines[i],[loc[0],loc[1]+lines[i].get_height()])
	return len(lines)*lines[0].get_height()
