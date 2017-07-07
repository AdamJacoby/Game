from Functions.Piece_Class import Piece,rook_move
from Functions.Game_Functions import Find_Zone, Pix_To_Hand,Draft_To_Pix
from Images.Piece_images import draw_text_piece

class Freedom(Piece):
	def legal_place(self,loc,Turn_Indicator,Pieces):
		if loc == None:
			return False
		out = True
		for piece in Pieces:
			if piece.loc == loc:
				out = False
		if Find_Zone(loc) in ['nutral_zone','goal']:
			out = False
		return out
freedom_move = 'Movement: Two space in vertical and horizontal directions'
freedom_ability = 'Ability: Can be placed in territories'
Freedom = Freedom('Freedom',draw_text_piece('Fre',(96,96,96)),Draft_To_Pix([5,3]),rook_move,True,'p',freedom_move,freedom_ability)