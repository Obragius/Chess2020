import wx
import os, os.path


# This class will deal with
# -Switching between players
# -Creating and storing player names
moves = 1
attack = 0
class Players():
	def GetPlayer(self):
		global moves
		moves += 1
		if (moves % 2) == 0:
			player = 1
			return player
		else:
			player = 2
			return player

	def AttackCheck(self):
		global attack
		if attack == 0:
			return False
		else:
			return True

	def AttackSet(self):
		global attack



# This class will store the position of the pieces on the board
# The changes in this class will change the board state
class Board():
	BoardConfig = (
		[['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br',],
        ['Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp',],
        ['Wr', 'Wn', 'Wb', 'Wq', 'Wk', 'Wb', 'Wn', 'Wr',]])
	


	# This method will allow to get the position of the selected piece
	@classmethod
	def GetPosition(self, DoubleInt):
		strDoubleInt = str(DoubleInt)
		strRow = strDoubleInt[0]
		strColumn = strDoubleInt[1]
		Row = int(strRow) - 1
		Column = int(strColumn) - 1 
		return (Board().BoardConfig[Row][Column])


# This will contain information about which pieces exist,
# how pieces can move, and their unique features
class Pieces():
	pass


# This will check where the piece can move, and if the position 
# which is passed on is mathcing the possition where the piece can move
class Logic():
	pass


# Should be called after each move to see if there is a check
class Check():
	pass


# Should be called after Check returns (True) to see if the 
# game is over
class CheckMate():
	pass
		


# This class deals with players interaction inside the code
# This class will send object id to the code and will display the board to the user
# GUI
# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
class Frame(wx.Frame):
	def __init__ (self, parent, title):
		super(Frame, self).__init__(parent, title=title, size = (900, 900))

		self.panel = MyPanel(self)



class MyPanel(wx.Panel):
	button = []
	hbox = []
	def __init__(self, parent):
		super(MyPanel,self).__init__(parent)

		# Setting up the grid
		hbox = [1,1,1,1,1,1,1,1,1,1,1]
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[4] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[5] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[6] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[7] = wx.BoxSizer(wx.HORIZONTAL)
		hbox9 = wx.BoxSizer(wx.HORIZONTAL)


		# Inserting images and converting to bitmap objects
		imageFileWhite = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White.png"
		imageFileBlack = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Grey.png"
		imageFileBlack_King = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_King_1.png"
		imageFileBlack_Queen = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Queen_1.png"
		imageFileBlack_Bishop = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Bishop_1.png"
		imageFileBlack_Rook = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Rook_1.png"
		imageFileBlack_Knight = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Knight_1.png"
		imageFileBlack_Pawn = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Pawn_1.png"
		imageFileWhite_King = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_King_1.png"
		imageFileWhite_Queen = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Queen_1.png"
		imageFileWhite_Bishop = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Bishop_1.png"
		imageFileWhite_Rook = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Rook_1.png"
		imageFileWhite_Knight = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Knight_1.png"
		imageFileWhite_Pawn = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Pawn_1.png"

		imageWhite = wx.Image(imageFileWhite, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack = wx.Image(imageFileBlack, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_King = wx.Image(imageFileBlack_King, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Queen = wx.Image(imageFileBlack_Queen, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Bishop = wx.Image(imageFileBlack_Bishop, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Rook = wx.Image(imageFileBlack_Rook, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Knight = wx.Image(imageFileBlack_Knight, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Pawn = wx.Image(imageFileBlack_Pawn, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_King = wx.Image(imageFileWhite_King, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Queen = wx.Image(imageFileWhite_Queen, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Bishop = wx.Image(imageFileWhite_Bishop, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Rook = wx.Image(imageFileWhite_Rook, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Knight = wx.Image(imageFileWhite_Knight, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Pawn = wx.Image(imageFileWhite_Pawn, wx.BITMAP_TYPE_ANY).ConvertToBitmap()


		# Trying method to print all the buttons in a loop
		self.button = []
		for i in range(8):
			self.button.append([])
			hbox.append([])
			for j in range(8):
				if (i % 2) == 0:
					if (j % 2) == 0:

						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = imageWhite_Pawn, size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
					else:
						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = imageBlack_King, size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
				else:
					if (j % 2) == 0:
						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = imageBlack, size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
					else:
						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = imageWhite, size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)


		# Iniciating buttons(First way)
		
		# self.button11 = wx.BitmapButton(self, id =11, bitmap = image1, size = (100,100))
		# hbox1.Add(self.button11, 0 , wx.ALIGN_CENTER)
		# self.button12 = wx.BitmapButton(self, id =12, bitmap = image2, size = (100,100))
		# hbox1.Add(self.button12, 0 , wx.ALIGN_CENTER)
		# self.button13 = wx.BitmapButton(self, id =13, bitmap = image1, size = (100,100))
		# hbox1.Add(self.button13, 0 , wx.ALIGN_CENTER)
		# self.button14 = wx.BitmapButton(self, id =14, bitmap = image2, size = (100,100))
		# hbox1.Add(self.button14, 0 , wx.ALIGN_CENTER)
		# self.button15 = wx.BitmapButton(self, id =15, bitmap = image1, size = (100,100))
		# hbox1.Add(self.button15, 0 , wx.ALIGN_CENTER)
		# self.button16 = wx.BitmapButton(self, id =16, bitmap = image2, size = (100,100))
		# hbox1.Add(self.button16, 0 , wx.ALIGN_CENTER)
		# self.button17 = wx.BitmapButton(self, id =17, bitmap = image1, size = (100,100))
		# hbox1.Add(self.button17, 0 , wx.ALIGN_CENTER)
		# self.button18 = wx.BitmapButton(self, id =18, bitmap = image2, size = (100,100))
		# hbox1.Add(self.button18, 0 , wx.ALIGN_CENTER)




		# self.button21 = wx.BitmapButton(self, id =21, bitmap = image2, size = (100,100))
		# hbox2.Add(self.button21, 0 , wx.ALIGN_CENTER)
		# self.button22 = wx.BitmapButton(self, id =22, bitmap = image1, size = (100,100))
		# hbox2.Add(self.button22, 0 , wx.ALIGN_CENTER)
		# self.button23 = wx.BitmapButton(self, id =23, bitmap = image2, size = (100,100))
		# hbox2.Add(self.button23, 0 , wx.ALIGN_CENTER)
		# self.button24 = wx.BitmapButton(self, id =24, bitmap = image1, size = (100,100))
		# hbox2.Add(self.button24, 0 , wx.ALIGN_CENTER)
		# self.button25 = wx.BitmapButton(self, id =25, bitmap = image2, size = (100,100))
		# hbox2.Add(self.button25, 0 , wx.ALIGN_CENTER)
		# self.button26 = wx.BitmapButton(self, id =26, bitmap = image1, size = (100,100))
		# hbox2.Add(self.button26, 0 , wx.ALIGN_CENTER)
		# self.button27 = wx.BitmapButton(self, id =27, bitmap = image2, size = (100,100))
		# hbox2.Add(self.button27, 0 , wx.ALIGN_CENTER)
		# self.button28 = wx.BitmapButton(self, id =28, bitmap = image1, size = (100,100))
		# hbox2.Add(self.button28, 0 , wx.ALIGN_CENTER)




		# self.button31 = wx.BitmapButton(self, id =31, bitmap = image1, size = (100,100))
		# hbox3.Add(self.button31, 0 , wx.ALIGN_CENTER)
		# self.button32 = wx.BitmapButton(self, id =32, bitmap = image2, size = (100,100))
		# hbox3.Add(self.button32, 0 , wx.ALIGN_CENTER)
		# self.button33 = wx.BitmapButton(self, id =33, bitmap = image1, size = (100,100))
		# hbox3.Add(self.button33, 0 , wx.ALIGN_CENTER)
		# self.button34 = wx.BitmapButton(self, id =34, bitmap = image2, size = (100,100))
		# hbox3.Add(self.button34, 0 , wx.ALIGN_CENTER)
		# self.button35 = wx.BitmapButton(self, id =35, bitmap = image1, size = (100,100))
		# hbox3.Add(self.button35, 0 , wx.ALIGN_CENTER)
		# self.button36 = wx.BitmapButton(self, id =36, bitmap = image2, size = (100,100))
		# hbox3.Add(self.button36, 0 , wx.ALIGN_CENTER)
		# self.button37 = wx.BitmapButton(self, id =37, bitmap = image1, size = (100,100))
		# hbox3.Add(self.button37, 0 , wx.ALIGN_CENTER)
		# self.button38 = wx.BitmapButton(self, id =38, bitmap = image2, size = (100,100))
		# hbox3.Add(self.button38, 0 , wx.ALIGN_CENTER)




		# self.button41 = wx.BitmapButton(self, id =41, bitmap = image2, size = (100,100))
		# hbox4.Add(self.button41, 0 , wx.ALIGN_CENTER)
		# self.button42 = wx.BitmapButton(self, id =42, bitmap = image1, size = (100,100))
		# hbox4.Add(self.button42, 0 , wx.ALIGN_CENTER)
		# self.button43 = wx.BitmapButton(self, id =43, bitmap = image2, size = (100,100))
		# hbox4.Add(self.button43, 0 , wx.ALIGN_CENTER)
		# self.button44 = wx.BitmapButton(self, id =44, bitmap = image1, size = (100,100))
		# hbox4.Add(self.button44, 0 , wx.ALIGN_CENTER)
		# self.button45 = wx.BitmapButton(self, id =45, bitmap = image2, size = (100,100))
		# hbox4.Add(self.button45, 0 , wx.ALIGN_CENTER)
		# self.button46 = wx.BitmapButton(self, id =46, bitmap = image1, size = (100,100))
		# hbox4.Add(self.button46, 0 , wx.ALIGN_CENTER)
		# self.button47 = wx.BitmapButton(self, id =47, bitmap = image2, size = (100,100))
		# hbox4.Add(self.button47, 0 , wx.ALIGN_CENTER)
		# self.button48 = wx.BitmapButton(self, id =48, bitmap = image1, size = (100,100))
		# hbox4.Add(self.button48, 0 , wx.ALIGN_CENTER)




		# self.button51 = wx.BitmapButton(self, id =51, bitmap = image1, size = (100,100))
		# hbox5.Add(self.button51, 0 , wx.ALIGN_CENTER)
		# self.button52 = wx.BitmapButton(self, id =52, bitmap = image2, size = (100,100))
		# hbox5.Add(self.button52, 0 , wx.ALIGN_CENTER)
		# self.button53 = wx.BitmapButton(self, id =53, bitmap = image1, size = (100,100))
		# hbox5.Add(self.button53, 0 , wx.ALIGN_CENTER)
		# self.button54 = wx.BitmapButton(self, id =54, bitmap = image2, size = (100,100))
		# hbox5.Add(self.button54, 0 , wx.ALIGN_CENTER)
		# self.button55 = wx.BitmapButton(self, id =55, bitmap = image1, size = (100,100))
		# hbox5.Add(self.button55, 0 , wx.ALIGN_CENTER)
		# self.button56 = wx.BitmapButton(self, id =56, bitmap = image2, size = (100,100))
		# hbox5.Add(self.button56, 0 , wx.ALIGN_CENTER)
		# self.button57 = wx.BitmapButton(self, id =57, bitmap = image1, size = (100,100))
		# hbox5.Add(self.button57, 0 , wx.ALIGN_CENTER)
		# self.button58 = wx.BitmapButton(self, id =58, bitmap = image2, size = (100,100))
		# hbox5.Add(self.button58, 0 , wx.ALIGN_CENTER)




		# self.button61 = wx.BitmapButton(self, id =61, bitmap = image2, size = (100,100))
		# hbox6.Add(self.button61, 0 , wx.ALIGN_CENTER)
		# self.button62 = wx.BitmapButton(self, id =62, bitmap = image1, size = (100,100))
		# hbox6.Add(self.button62, 0 , wx.ALIGN_CENTER)
		# self.button63 = wx.BitmapButton(self, id =63, bitmap = image2, size = (100,100))
		# hbox6.Add(self.button63, 0 , wx.ALIGN_CENTER)
		# self.button64 = wx.BitmapButton(self, id =64, bitmap = image1, size = (100,100))
		# hbox6.Add(self.button64, 0 , wx.ALIGN_CENTER)
		# self.button65 = wx.BitmapButton(self, id =65, bitmap = image2, size = (100,100))
		# hbox6.Add(self.button65, 0 , wx.ALIGN_CENTER)
		# self.button66 = wx.BitmapButton(self, id =66, bitmap = image1, size = (100,100))
		# hbox6.Add(self.button66, 0 , wx.ALIGN_CENTER)
		# self.button67 = wx.BitmapButton(self, id =67, bitmap = image2, size = (100,100))
		# hbox6.Add(self.button67, 0 , wx.ALIGN_CENTER)
		# self.button68 = wx.BitmapButton(self, id =68, bitmap = image1, size = (100,100))
		# hbox6.Add(self.button68, 0 , wx.ALIGN_CENTER)




		# self.button71 = wx.BitmapButton(self, id =71, bitmap = image1, size = (100,100))
		# hbox7.Add(self.button71, 0 , wx.ALIGN_CENTER)
		# self.button72 = wx.BitmapButton(self, id =72, bitmap = image2, size = (100,100))
		# hbox7.Add(self.button72, 0 , wx.ALIGN_CENTER)
		# self.button73 = wx.BitmapButton(self, id =73, bitmap = image1, size = (100,100))
		# hbox7.Add(self.button73, 0 , wx.ALIGN_CENTER)
		# self.button74 = wx.BitmapButton(self, id =74, bitmap = image2, size = (100,100))
		# hbox7.Add(self.button74, 0 , wx.ALIGN_CENTER)
		# self.button75 = wx.BitmapButton(self, id =75, bitmap = image1, size = (100,100))
		# hbox7.Add(self.button75, 0 , wx.ALIGN_CENTER)
		# self.button76 = wx.BitmapButton(self, id =76, bitmap = image2, size = (100,100))
		# hbox7.Add(self.button76, 0 , wx.ALIGN_CENTER)
		# self.button77 = wx.BitmapButton(self, id =77, bitmap = image1, size = (100,100))
		# hbox7.Add(self.button77, 0 , wx.ALIGN_CENTER)
		# self.button78 = wx.BitmapButton(self, id =78, bitmap = image2, size = (100,100))
		# hbox7.Add(self.button78, 0 , wx.ALIGN_CENTER)




		# self.button81 = wx.BitmapButton(self, id =81, bitmap = image2, size = (100,100))
		# hbox8.Add(self.button81, 0 , wx.ALIGN_CENTER)
		# self.button82 = wx.BitmapButton(self, id =82, bitmap = image1, size = (100,100))
		# hbox8.Add(self.button82, 0 , wx.ALIGN_CENTER)
		# self.button83 = wx.BitmapButton(self, id =83, bitmap = image2, size = (100,100))
		# hbox8.Add(self.button83, 0 , wx.ALIGN_CENTER)
		# self.button84 = wx.BitmapButton(self, id =84, bitmap = image1, size = (100,100))
		# hbox8.Add(self.button84, 0 , wx.ALIGN_CENTER)
		# self.button85 = wx.BitmapButton(self, id =85, bitmap = image2, size = (100,100))
		# hbox8.Add(self.button85, 0 , wx.ALIGN_CENTER)
		# self.button86 = wx.BitmapButton(self, id =86, bitmap = image1, size = (100,100))
		# hbox8.Add(self.button86, 0 , wx.ALIGN_CENTER)
		# self.button87 = wx.BitmapButton(self, id =87, bitmap = image2, size = (100,100))
		# hbox8.Add(self.button87, 0 , wx.ALIGN_CENTER)
		# self.button88 = wx.BitmapButton(self, id =88, bitmap = image1, size = (100,100))
		# hbox8.Add(self.button88, 0 , wx.ALIGN_CENTER)

		self.Status = wx.StaticText(self, label = "")
		font = wx.Font(40, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		self.Status.SetFont(font)
		hbox9.Add(self.Status, 0 , wx.ALIGN_CENTER)

		vbox.Add(hbox[0], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[1], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[2], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[3], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[4], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[5], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[6], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[7], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox9, 0, wx.ALIGN_CENTER)
		self.SetSizer(vbox)

		self.Bind(wx.EVT_BUTTON, self.OnClick)


		# OnClick we take the event and identify the button pressed
	def OnClick(self, event):
		Status_Pressed = str(event.GetEventObject().GetId())
		# This is code for testing purposes
		self.Status.SetLabelText(Status_Pressed)


		# Now we need to send the button pressed to the Board to return the position which was selected
		Piece = Board().GetPosition(event.GetEventObject().GetId())
		# From this we get the piece selected, so we need to ckeck wether it is the correct piece for this player
		player = Players().GetPlayer()
		# Now we need to confirm that this is his first press and not the attack move
		attack = Players().AttackCheck()
		if attack == False:
			pass
		else:
			pass
		


		
		

class App(wx.App):
	def OnInit(self):
		self.frame = Frame(parent=None, title="Chess" )
		self.frame.Show()
		return True 


app = App()
app.MainLoop()

# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
