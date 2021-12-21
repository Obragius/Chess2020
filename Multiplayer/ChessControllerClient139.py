import wx
import os, os.path
import time
import wx.grid as gridlib
import sys


# This class will deal with
# -Switching between players
# -Creating and storing player names
ChessRun = True
PawnDelete = False
PawnBlock = False
WhitePawnDis = False
BlackPawnDis = False
GiveUP = "False"
GiveUPDis = "False"
Blocked = False
CurrentStatusMsg = ""
logmoves = 0
White_King_Check = False
Black_King_Check = False
ButtonList = []
LastPress = 0
PawnHandler = [False,0,0]
GreenSpaces = False
CustomBoardValue = False
MessageList = []
LastMessageList = []
MessageListNumLow = 0
Refresh = False
labelUpdate = False
PlayersToSwitch = [1,2]
TwoKingRule = True
Send_Status_Press = ""
UpdateTime = False
UpdateTimeD = False
NoUpdateLast = False
LastGreenSpaceDisplay = (
		[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
LogOfMoves = [[['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR',],
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP',],
        ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR',]]]
YourTurn = False
YourTurnID = 0
BoardState = 0

class Board():

	# This is the board which shows the actual state of the game
	BoardConfig = (
		[['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR',],
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP',],
        ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR',]])

	def BoardToDisplay(self, PossibleMoves):
		# Create the list to give the values to
		BoardToChange = (
		[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
		for i in range(8):
			for j in range(8):
				BoardToChange[i][j] = Board().BoardConfig[i][j]
		if PossibleMoves != None:
			Moves = 0
			while Moves < len(PossibleMoves):
				CurrentPos = PossibleMoves[Moves]
				GreenRow = int(str(CurrentPos)[0])-1
				GreenColumn = int(str(CurrentPos)[1])-1
				BoardToChange[GreenRow][GreenColumn] = BoardToChange[GreenRow][GreenColumn] + "G"
				Moves +=1
		return BoardToChange


	# This is the log for the last move made
	BoardLogLastMove = [0,"0","",0]

	# This is the log for dealing with pawn catching
	# First value is the initiator False or True
	# Second value is the additional bitmap to update
	# Third value is the move which got allowed
	PawnAtribute = [False, 0, 0]

	# This is the value which will determine if a rook 
	# has moved to cancel out a certain castling
	# 1. LeftTopBlackRook
	# 2. RightTopBlackRook
	# 3. LeftBottomWhiteRook
	# 4. RightBottomWhiteRook
	RookAtribute = [False,False,False,False]

	# This will be two lists which will have 8 spaces around the king stored 
	# as spaces which the second king cannot go to
	WhiteKingDZ = [86,84,75,76,74]
	BlackKingDZ = [16,24,25,26,14]

	def RevertMove(self):
		global logmoves, LogOfMoves, moves, B_Kingmoves, W_Kingmoves 
		if logmoves > 0:
			moves -=1
			NewBoard = LogOfMoves[logmoves-1]
			for i in range(8):
				for j in range(8):
					Board().BoardConfig[i][j] = NewBoard[i][j]
			LogOfMoves.remove(LogOfMoves[logmoves])
			logmoves -=1

			# This is to allow players to castle again we need to check all the boards and
			# see if the piece were in diferent positions during the game, if not we allow it
			Moves = 0
			MovesMax = len(LogOfMoves)
			# 1.LeftBlackRook, 2.RightBlackRook, 3.BlackKing, 4.LeftWhiteRook, 5.RightWhiteRook, 6.WhiteKing
			CastleReturn = [True,True,True,True,True,True]
			while Moves < MovesMax:
				if LogOfMoves[Moves][0][0] != "BR":
					CastleReturn[0] = False
				if LogOfMoves[Moves][0][7] != "BR":
					CastleReturn[1] = False
				if LogOfMoves[Moves][0][4] != "BK":
					CastleReturn[2] = False
				if LogOfMoves[Moves][7][0] != "WR":
					CastleReturn[3] = False
				if LogOfMoves[Moves][7][7] != "WR":
					CastleReturn[4] = False
				if LogOfMoves[Moves][7][4] != "WK":
					CastleReturn[5] = False
				Moves+=1
			if CastleReturn[0] == True:
				Board().RookAtribute[0] = False
			if CastleReturn[1] == True:
				Board().RookAtribute[1] = False
			if CastleReturn[2] == True:
				B_Kingmoves = 0
			if CastleReturn[3] == True:
				Board().RookAtribute[2] = False
			if CastleReturn[4] == True:
				Board().RookAtribute[3] = False
			if CastleReturn[5] == True:
				W_Kingmoves = 0



	# This will update the Log of Moves done in the game
	def BoardLog(self):
		global LogOfMoves, logmoves
		NewBoard = (
					[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
		for i in range(8):
			for j in range(8):
				NewBoard[i][j] = Board().BoardConfig[i][j]
		LogOfMoves.append(NewBoard)
		logmoves +=1



	def PieceConversionHandler(self, Position, Piece):
		# This will handle the conversion of the board space
		# to a new state using the position and the piece
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		Board().BoardConfig[Row-1][Column-1] = Piece
		


	# This method will allow to get the position of the selected piece
	@classmethod
	def GetPosition(self, DoubleInt):
		StrDoubleInt = str(DoubleInt)
		StrRow = StrDoubleInt[0]
		StrColumn = StrDoubleInt[1]
		Row = int(StrRow) - 1
		Column = int(StrColumn) - 1 
		return (Board().BoardConfig[Row][Column])

	# This will return the str of piece on the board
	def GetPieceFromBoard(self, row, column):
		Piece = Board().BoardConfig[row][column]
		return Piece


# This class deals with players interaction inside the code
# This class will send object id to the code and will display the board to the user
# GUI
# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________

class LoadingImages():
	def initilize(self):
		# Inserting images and converting to bitmap objects
		imageFileWhite = "Images\\White.png"
		imageFileBlack = "Images\\Grey.png"

		# Creating empty lists to assign images to
		imageFileBlack_King = ["",""]
		imageFileBlack_Queen = ["",""]
		imageFileBlack_Bishop = ["",""]
		imageFileBlack_Rook = ["",""]
		imageFileBlack_Knight = ["",""]
		imageFileBlack_Pawn = ["",""]
		imageFileWhite_King = ["",""]
		imageFileWhite_Queen = ["",""]
		imageFileWhite_Bishop = ["",""]
		imageFileWhite_Rook = ["",""]
		imageFileWhite_Knight = ["",""]
		imageFileWhite_Pawn = ["",""]


		# Inserting images
		imageFileBlack_King[0] = "Images\\Black_King_White.png"
		imageFileBlack_Queen[0] = "Images\\Black_Queen_White.png"
		imageFileBlack_Bishop[0] = "Images\\Black_Bishop_White.png"
		imageFileBlack_Rook[0] = "Images\\Black_Rook_White.png"
		imageFileBlack_Knight[0] = "Images\\Black_Knight_White.png"
		imageFileBlack_Pawn[0] = "Images\\Black_Pawn_White.png"
		imageFileWhite_King[0] = "Images\\White_King_White.png"
		imageFileWhite_Queen[0] = "Images\\White_Queen_White.png"
		imageFileWhite_Bishop[0] = "Images\\White_Bishop_White.png"
		imageFileWhite_Rook[0] = "Images\\White_Rook_White.png"
		imageFileWhite_Knight[0] = "Images\\White_Knight_White.png"
		imageFileWhite_Pawn[0] = "Images\\White_Pawn_White.png"
		imageFileBlack_King[1] = "Images\\Black_King_Grey.png"
		imageFileBlack_Queen[1] = "Images\\Black_Queen_Grey.png"
		imageFileBlack_Bishop[1] = "Images\\Black_Bishop_Grey.png"
		imageFileBlack_Rook[1] = "Images\\Black_Rook_Grey.png"
		imageFileBlack_Knight[1] = "Images\\Black_Knight_Grey.png"
		imageFileBlack_Pawn[1] = "Images\\Black_Pawn_Grey.png"
		imageFileWhite_King[1] = "Images\\White_King_Grey.png"
		imageFileWhite_Queen[1] = "Images\\White_Queen_Grey.png"
		imageFileWhite_Bishop[1] = "Images\\White_Bishop_Grey.png"
		imageFileWhite_Rook[1] = "Images\\White_Rook_Grey.png"
		imageFileWhite_Knight[1] = "Images\\White_Knight_Grey.png"
		imageFileWhite_Pawn[1] = "Images\\White_Pawn_Grey.png"

		# Bitmaps for empty spaces
		imageColor = ["",""]
		imageColor[0] = wx.Image(imageFileWhite, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageColor[1] = wx.Image(imageFileBlack, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		# Creating empty lists to save the images to

		imageBlack_King = ["",""]
		imageBlack_Queen = ["",""]
		imageBlack_Bishop = ["",""]
		imageBlack_Rook = ["",""]
		imageBlack_Knight = ["",""]
		imageBlack_Pawn = ["",""]
		imageWhite_King = ["",""]
		imageWhite_Queen = ["",""]
		imageWhite_Bishop = ["",""]
		imageWhite_Rook = ["",""]
		imageWhite_Knight = ["",""]
		imageWhite_Pawn = ["",""]

		# Bitmaps for pieces with White background
		imageBlack_King[0] = wx.Image(imageFileBlack_King[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Queen[0] = wx.Image(imageFileBlack_Queen[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Bishop[0] = wx.Image(imageFileBlack_Bishop[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Rook[0] = wx.Image(imageFileBlack_Rook[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Knight[0] = wx.Image(imageFileBlack_Knight[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Pawn[0] = wx.Image(imageFileBlack_Pawn[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_King[0] = wx.Image(imageFileWhite_King[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Queen[0] = wx.Image(imageFileWhite_Queen[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Bishop[0] = wx.Image(imageFileWhite_Bishop[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Rook[0] = wx.Image(imageFileWhite_Rook[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Knight[0] = wx.Image(imageFileWhite_Knight[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Pawn[0] = wx.Image(imageFileWhite_Pawn[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		# Bitmaps for pieces with Grey background
		imageBlack_King[1] = wx.Image(imageFileBlack_King[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Queen[1] = wx.Image(imageFileBlack_Queen[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Bishop[1] = wx.Image(imageFileBlack_Bishop[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Rook[1] = wx.Image(imageFileBlack_Rook[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Knight[1] = wx.Image(imageFileBlack_Knight[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Pawn[1] = wx.Image(imageFileBlack_Pawn[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_King[1] = wx.Image(imageFileWhite_King[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Queen[1] = wx.Image(imageFileWhite_Queen[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Bishop[1] = wx.Image(imageFileWhite_Bishop[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Rook[1] = wx.Image(imageFileWhite_Rook[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Knight[1] = wx.Image(imageFileWhite_Knight[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Pawn[1] = wx.Image(imageFileWhite_Pawn[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		# To use these in a loop I need to give them id based on the piece

		ImageToLoad = [imageBlack_King, imageBlack_Queen, imageBlack_Bishop, imageBlack_Rook, imageBlack_Knight, imageBlack_Pawn,
						imageWhite_King, imageWhite_Queen, imageWhite_Bishop, imageWhite_Rook, imageWhite_Knight, imageWhite_Pawn, imageColor]


		# Creating a dictionary allowing to call the required image

		ImageToLoadDict = {"BK":0, "BQ":1, "BB":2, "BR":3, "BN":4, "BP":5,
							"WK":6, "WQ":7, "WB":8, "WR":9, "WN":10, "WP":11, "  ":12}

		# Naming variable to set grey background
		GreyAttribute = ([[0, 1, 0, 1, 0, 1, 0, 1,],
				        [1, 0, 1, 0, 1, 0, 1, 0,],
				        [0, 1, 0, 1, 0, 1, 0, 1,],
				        [1, 0, 1, 0, 1, 0, 1, 0,],
				        [0, 1, 0, 1, 0, 1, 0, 1,],
				        [1, 0, 1, 0, 1, 0, 1, 0,],
				        [0, 1, 0, 1, 0, 1, 0, 1,],
				        [1, 0, 1, 0, 1, 0, 1, 0,]])

		# Green images loading

		imageFileGreen = ["",""]
		imageFileGreen[0] = "Images\\Green.png"
		imageFileGreen[1] = "Images\\Green_Dark.png"

		imageGreen = ["",""]
		imageGreen[0] = wx.Image(imageFileGreen[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageGreen[1] = wx.Image(imageFileGreen[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		imageBlack_King_Green = ["",""]
		imageBlack_Queen_Green = ["",""]
		imageBlack_Bishop_Green = ["",""]
		imageBlack_Rook_Green = ["",""]
		imageBlack_Knight_Green = ["",""]
		imageBlack_Pawn_Green = ["",""]
		imageWhite_King_Green = ["",""]
		imageWhite_Queen_Green = ["",""]
		imageWhite_Bishop_Green = ["",""]
		imageWhite_Rook_Green = ["",""]
		imageWhite_Knight_Green = ["",""]
		imageWhite_Pawn_Green = ["",""]


		imageFileBlack_King_Green = "Images\\Black_King_Green.png"
		imageFileBlack_Queen_Green = "Images\\Black_Queen_Green.png"
		imageFileBlack_Bishop_Green = "Images\\Black_Bishop_Green.png"
		imageFileBlack_Rook_Green = "Images\\Black_Rook_Green.png"
		imageFileBlack_Knight_Green = "Images\\Black_Knight_Green.png"
		imageFileBlack_Pawn_Green = "Images\\Black_Pawn_Green.png"
		imageFileWhite_King_Green = "Images\\White_King_Green.png"
		imageFileWhite_Queen_Green = "Images\\White_Queen_Green.png"
		imageFileWhite_Bishop_Green = "Images\\White_Bishop_Green.png"
		imageFileWhite_Rook_Green = "Images\\White_Rook_Green.png"
		imageFileWhite_Knight_Green = "Images\\White_Knight_Green.png"
		imageFileWhite_Pawn_Green = "Images\\White_Pawn_Green.png"

		imageFileBlack_King_Green_Dark = "Images\\Black_King_Green_Dark.png"
		imageFileBlack_Queen_Green_Dark = "Images\\Black_Queen_Green_Dark.png"
		imageFileBlack_Bishop_Green_Dark = "Images\\Black_Bishop_Green_Dark.png"
		imageFileBlack_Rook_Green_Dark = "Images\\Black_Rook_Green_Dark.png"
		imageFileBlack_Knight_Green_Dark = "Images\\Black_Knight_Green_Dark.png"
		imageFileBlack_Pawn_Green_Dark = "Images\\Black_Pawn_Green_Dark.png"
		imageFileWhite_King_Green_Dark = "Images\\White_King_Green_Dark.png"
		imageFileWhite_Queen_Green_Dark = "Images\\White_Queen_Green_Dark.png"
		imageFileWhite_Bishop_Green_Dark = "Images\\White_Bishop_Green_Dark.png"
		imageFileWhite_Rook_Green_Dark = "Images\\White_Rook_Green_Dark.png"
		imageFileWhite_Knight_Green_Dark = "Images\\White_Knight_Green_Dark.png"
		imageFileWhite_Pawn_Green_Dark = "Images\\White_Pawn_Green_Dark.png"

		imageBlack_King_Green[0] = wx.Image(imageFileBlack_King_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Queen_Green[0] = wx.Image(imageFileBlack_Queen_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Bishop_Green[0] = wx.Image(imageFileBlack_Bishop_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Rook_Green[0] = wx.Image(imageFileBlack_Rook_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Knight_Green[0] = wx.Image(imageFileBlack_Knight_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Pawn_Green[0] = wx.Image(imageFileBlack_Pawn_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_King_Green[0] = wx.Image(imageFileWhite_King_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Queen_Green[0] = wx.Image(imageFileWhite_Queen_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Bishop_Green[0] = wx.Image(imageFileWhite_Bishop_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Rook_Green[0] = wx.Image(imageFileWhite_Rook_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Knight_Green[0] = wx.Image(imageFileWhite_Knight_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Pawn_Green[0] = wx.Image(imageFileWhite_Pawn_Green, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		imageBlack_King_Green[1] = wx.Image(imageFileBlack_King_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Queen_Green[1] = wx.Image(imageFileBlack_Queen_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Bishop_Green[1] = wx.Image(imageFileBlack_Bishop_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Rook_Green[1] = wx.Image(imageFileBlack_Rook_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Knight_Green[1] = wx.Image(imageFileBlack_Knight_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageBlack_Pawn_Green[1] = wx.Image(imageFileBlack_Pawn_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_King_Green[1] = wx.Image(imageFileWhite_King_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Queen_Green[1] = wx.Image(imageFileWhite_Queen_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Bishop_Green[1] = wx.Image(imageFileWhite_Bishop_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Rook_Green[1] = wx.Image(imageFileWhite_Rook_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Knight_Green[1] = wx.Image(imageFileWhite_Knight_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageWhite_Pawn_Green[1] = wx.Image(imageFileWhite_Pawn_Green_Dark, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		ImageToLoadGreen = [imageBlack_King_Green, imageBlack_Queen_Green, imageBlack_Bishop_Green, imageBlack_Rook_Green, imageBlack_Knight_Green, imageBlack_Pawn_Green,
						imageWhite_King_Green, imageWhite_Queen_Green, imageWhite_Bishop_Green, imageWhite_Rook_Green, imageWhite_Knight_Green, imageWhite_Pawn_Green, imageGreen]

		ImageToLoadGreenDict = {"BKG":0, "BQG":1, "BBG":2, "BRG":3, "BNG":4, "BPG":5,
							"WKG":6, "WQG":7, "WBG":8, "WRG":9, "WNG":10, "WPG":11, "  G":12}


		# Initilising the numbers and letters to load
		imageFileGreySmall = "Images\\GreySmall.png"
		imageFile1 = "Images\\1.png"
		imageFile2 = "Images\\2.png"
		imageFile3 = "Images\\3.png"
		imageFile4 = "Images\\4.png"
		imageFile5 = "Images\\5.png"
		imageFile6 = "Images\\6.png"
		imageFile7 = "Images\\7.png"
		imageFile8 = "Images\\8.png"
		imageFileA = "Images\\A.png"
		imageFileB = "Images\\B.png"
		imageFileC = "Images\\C.png"
		imageFileD = "Images\\D.png"
		imageFileE = "Images\\E.png"
		imageFileF = "Images\\F.png"
		imageFileG = "Images\\G.png"
		imageFileH = "Images\\H.png"

		imageg = wx.Image(imageFileGreySmall, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image1 = wx.Image(imageFile1, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image2 = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image3 = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image4 = wx.Image(imageFile4, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image5 = wx.Image(imageFile5, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image6 = wx.Image(imageFile6, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image7 = wx.Image(imageFile7, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		image8 = wx.Image(imageFile8, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageA = wx.Image(imageFileA, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageB = wx.Image(imageFileB, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageC = wx.Image(imageFileC, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageD = wx.Image(imageFileD, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageE = wx.Image(imageFileE, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageF = wx.Image(imageFileF, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageG = wx.Image(imageFileG, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imageH = wx.Image(imageFileH, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		NumLetToLoad = {0:imageg, 1:imageA, 2:imageB, 3:imageC, 4:imageD, 5:imageE, 6:imageF,
						7:imageG, 8:imageH, 9:image8, 10:image7, 11:image6, 12:image5,
						13:image4, 14:image3, 15:image2, 16:image1}


		# Returning all the images
		return (imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, 
		imageBlack_Pawn ,imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook,
		imageWhite_Knight ,imageWhite_Pawn ,ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad)


# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
class Frame(wx.Frame):
	def __init__ (self, parent, title):
		super(Frame, self).__init__(parent, title=title, size = (800, 750))
		self.panel = MyPanel(self)
		self.panel.SetBackgroundColour(wx.Colour( 123, 96, 68))
		self.Bind(wx.EVT_CLOSE, self._when_closed)
		self.BasicGUI()

	def _when_closed(self, event):
		global ChessRun, Send_Status_Press
		ChessRun = False
		Send_Status_Press = '&USEROUT'
		time.sleep(1)
		self.Destroy()
		self.Close(True)
		sys.exit(1)

	def BasicGUI(self):
		FirstMethod = wx.Menu()
		SwitchBoard = FirstMethod.Append(wx.ID_OPEN, "Switch Board")
		self.Bind(wx.EVT_MENU, self.OnSwitchBoard, SwitchBoard)
		SecondMethod = wx.Menu()
		Give = SecondMethod.Append(wx.ID_CLOSE, "Give Up")
		self.Bind(wx.EVT_MENU, self.OnGiveUP, Give)
		menuBar = wx.MenuBar()
		menuBar.Append(FirstMethod, "&Cosmetic")
		menuBar.Append(SecondMethod, "&Match")
		self.SetMenuBar(menuBar)

	def OnSwitchBoard(self, Event):
		global BoardState, UpdateTime
		if BoardState == 0:
			self.panel.ResetLetters()
			BoardState = 1
			UpdateTime = True
		else:
			self.panel.ResetLetters()
			BoardState = 0
			UpdateTime = True

	def OnGiveUP(self, Event):
		global GiveUP, GiveUPDis
		if GiveUPDis == "False":
			GiveUP = "True"


class MyPanel(wx.Panel):
	button = []
	hbox = []
	def __init__(self, parent):
		super(MyPanel,self).__init__(parent,pos = (0,0),size = (800, 750))

		self.OnInit()

	def OnInit(self):





# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________

		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

		# Setting up the grid
		self.hbox = [1,1,1,1,1,1,1,1,1,1,1]
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[4] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[5] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[6] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[7] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[8] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox[9] = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox9 = wx.BoxSizer(wx.HORIZONTAL)

		# Naming variable to set grey background
		# Trying method to print all the buttons in a loop
		# List for displaying the buttons and images
		DisplayCase = ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
				        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]])
		ListForNumLet = [0,1,2,3,4,5,6,7,8,0,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16,16,0,1,2,3,4,5,6,7,8,0]
		self.button = []
		self.image = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		GetTheNumLet = 0
		for i in range(10):
			self.button.append([])
			self.hbox.append([])
			for j in range(10):
				if DisplayCase[i][j] == 1:
					# Getting the piece from board
					Piece = Board().GetPieceFromBoard((i-1),(j-1))
					# Getting the coresponding image to that piece
					ImageID = ImageToLoadDict[Piece]
					self.button[i-1].append([])
					self.button[i-1][j-1] = wx.BitmapButton(self, id =int(str(i)+str(j)), bitmap = ImageToLoad[ImageID][GreyAttribute[i-1][j-1]],  size = (55,55))
					self.hbox[i].Add(self.button[i-1][j-1], 0 , wx.ALIGN_CENTER)
				else:
					if ListForNumLet[GetTheNumLet] == 0:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (45,45))
						self.hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1
					elif ListForNumLet[GetTheNumLet] > 8:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (45,55))
						self.hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1
					else:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (55,45))
						self.hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1


					

			

		self.Status = wx.StaticText(self, label = "", pos=(400,590), id = 1505)
		font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.Status.SetFont(font)
		self.SetBackgroundColour(wx.Colour( 123, 96, 68))

		self.Turn = wx.StaticText(self, label = "", pos=(390,540), id = 1505)
		font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.Turn.SetFont(font)

		self.Timer = wx.Timer(self, id= 999)
		self.Timer.Start(50)
		self.Bind(wx.EVT_TIMER, self.UpdateBoard)

		self.vbox.Add(self.hbox[0], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[1], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[2], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[3], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[4], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[5], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[6], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[7], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[8], 0, wx.ALIGN_CENTER)
		self.vbox.Add(self.hbox[9], 0, wx.ALIGN_CENTER)
		self.SetSizer(self.vbox)

		# We want to set the log of text where the moves will be displayed
		self.Logs = wx.StaticText(self, id = 500,label = "", pos = (670,60), size=(60,480))
		font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.Logs.SetFont(font)
		self.slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2, style = wx.SL_VERTICAL, pos = (760,60), size =(20,390) )
		self.Bind(wx.EVT_SLIDER, self.OnScroll)


		self.Bind(wx.EVT_BUTTON, self.OnClick)

	def ResetLetters(self):
		global BoardState
		if BoardState == 0:
			(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
			imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
			ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

			ListForNumLet = [0,8,7,6,5,4,3,2,1,0,16,16,15,15,14,14,13,13,12,12,11,11,10,10,9,9,0,8,7,6,5,4,3,2,1,0]
			for i in range(36):
				if i == 0 or i == 9 or i == 28 or i == 35:
					pass
				else:
					self.image[i].SetBitmap(NumLetToLoad[ListForNumLet[i]])
					time.sleep(0.05)
			self.Layout()
		else:
			(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
			imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
			ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

			ListForNumLet = [0,1,2,3,4,5,6,7,8,0,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16,16,0,1,2,3,4,5,6,7,8,0]
			for i in range(36):
				if i == 0 or i == 9 or i == 28 or i == 35:
					pass
				else:
					self.image[i].SetBitmap(NumLetToLoad[ListForNumLet[i]])
					time.sleep(0.05)
			self.Layout()

	def OnScroll(self, Event):
		global MessageListNumLow, MessageList
		obj = Event.GetEventObject()
		value = obj.GetValue()
		MessageListNumLowLocal = value
		Message = 0 + MessageListNumLowLocal
		if Message != 0:
			Message -= 1
		MessageMax = Message + 28
		MsgToDis = ""
		while Message < MessageMax:
			MsgToDis += MessageList[Message]
			Message +=1
		self.Logs.SetLabelText(MsgToDis)
# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________

	def UpdateBoard(self, Event):
		global UpdateTime,PawnDelete,PawnBlock, UpdateTimeD,WhitePawnDis, BlackPawnDis, YourTurn, YourTurnID, NoUpdateLast, MessageList, LastMessageList, Blocked
		
		if PawnDelete == True:
			try:
				self.PawnHandler(1)
			except:
				pass
			try:
				self.PawnHandler(2)
			except:
				pass

		if (WhitePawnDis == True and PawnBlock == False) or (BlackPawnDis == True and PawnBlock == False):
			(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
			imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
			ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
			if WhitePawnDis == True:
				self.buttonWN = wx.BitmapButton(self, id =101, bitmap = ImageToLoad[ImageToLoadDict["WN"]][0],  size = (55,55), pos=(170,560) )
				self.buttonWR = wx.BitmapButton(self, id =102, bitmap = ImageToLoad[ImageToLoadDict["WR"]][1],  size = (55,55), pos=(225,560) )
				self.buttonWB = wx.BitmapButton(self, id =103, bitmap = ImageToLoad[ImageToLoadDict["WB"]][0],  size = (55,55), pos=(280,560) )
				self.buttonWQ = wx.BitmapButton(self, id =104, bitmap = ImageToLoad[ImageToLoadDict["WQ"]][1],  size = (55,55), pos=(335,560) )
				PawnBlock = True
			else:
				self.buttonBN = wx.BitmapButton(self, id =105, bitmap = ImageToLoad[ImageToLoadDict["BN"]][0],  size = (55,55), pos=(170,560) )
				self.buttonBR = wx.BitmapButton(self, id =106, bitmap = ImageToLoad[ImageToLoadDict["BR"]][1],  size = (55,55), pos=(225,560) )
				self.buttonBB = wx.BitmapButton(self, id =107, bitmap = ImageToLoad[ImageToLoadDict["BB"]][0],  size = (55,55), pos=(280,560) )
				self.buttonBQ = wx.BitmapButton(self, id =108, bitmap = ImageToLoad[ImageToLoadDict["BQ"]][1],  size = (55,55), pos=(335,560) )
				PawnBlock = True

		if LastMessageList != MessageList:
			self.DoMessageList()
			Blocked = False
			LastMessageList = []
			for Value in MessageList:
				LastMessageList.append(Value)
		self.UserCheckDisplay()

		if BoardState == 0:
			if UpdateTime:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
				imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
				ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				for i in range(8):
					for j in range(8):
						Piece = Board().BoardConfig[i][j]
						Row = i
						Column = j
						ImageID = ImageToLoadDict[Piece]
						self.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
				UpdateTime = False
				NoUpdateLast = False
			if UpdateTimeD:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
				imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
				ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				for i in range(8):
					for j in range(8):
						Piece = Board().BoardConfig[i][j]
						Row = i
						Column = j
						ImageID = ImageToLoadDict[Piece]
						self.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
				for i in range(8):
					for j in range(8):
						Piece = LastGreenSpaceDisplay[i][j]
						if len(Piece) > 2:
							ImageID = ImageToLoadGreenDict[Piece]
							self.button[i][j].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[i][j]])
							# Creating a list to later remove the green spaces
							ButtonList.append(str(i)+str(j))
				UpdateTimeD = False
				Blocked = True
			if YourTurnID < 5:
				YourTurnID +=1
			else:
				YourTurnID = 0
				if YourTurn == b'True':
					self.YourTurnDisplay(True)
				else:
					self.YourTurnDisplay(False)
			if Board().BoardLogLastMove[1] != "0" and Blocked == False:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
						imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
						ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				if NoUpdateLast == False:
					I = int(Board().BoardLogLastMove[1][0])-1
					J = int(Board().BoardLogLastMove[1][1])-1
					Piece = Board().BoardConfig[I][J]
					Piece = Piece+"G"
					ImageID = ImageToLoadGreenDict[Piece]
					self.button[I][J].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[I][J]])
		else:
			if UpdateTime:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
				imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
				ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				for i in range(8):
					for j in range(8):
						Piece = Board().BoardConfig[7-i][7-j]
						Row = i
						Column = j
						ImageID = ImageToLoadDict[Piece]
						self.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
				UpdateTime = False
				NoUpdateLast = False
			if UpdateTimeD:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
				imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
				ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				for i in range(8):
					for j in range(8):
						Piece = Board().BoardConfig[7-i][7-j]
						Row = i
						Column = j
						ImageID = ImageToLoadDict[Piece]
						self.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
				for i in range(8):
					for j in range(8):
						Piece = LastGreenSpaceDisplay[7-i][7-j]
						if len(Piece) > 2:
							ImageID = ImageToLoadGreenDict[Piece]
							self.button[i][j].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[i][j]])
							# Creating a list to later remove the green spaces
							ButtonList.append(str(i)+str(j))
				UpdateTimeD = False
				Blocked = True
			if YourTurnID < 5:
				YourTurnID +=1
			else:
				YourTurnID = 0
				if YourTurn == b'True':
					self.YourTurnDisplay(True)
				else:
					self.YourTurnDisplay(False)
			if Board().BoardLogLastMove[1] != "0" and Blocked == False:
				(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
						imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
						ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
				if NoUpdateLast == False:
					I = int(Board().BoardLogLastMove[1][0])-1
					J = int(Board().BoardLogLastMove[1][1])-1
					Piece = Board().BoardConfig[I][J]
					Piece = Piece+"G"
					ImageID = ImageToLoadGreenDict[Piece]
					self.button[7-I][7-J].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[7-I][7-J]])


	def DoMessageList(self):
		global MessageList, MessageListNumLow
		if len(MessageList) > 27:
			MessageListNumLow +=1
			self.slider.SetMax(MessageListNumLow)
			self.slider.SetValue(MessageListNumLow+1)
		MsgToDis = ""
		Message = 0 + MessageListNumLow
		if Message != 0:
			Message -= 1
		MessageMax = len(MessageList)
		while Message < MessageMax:
			MsgToDis += MessageList[Message]
			Message +=1
		self.Logs.SetLabelText(MsgToDis)

# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________


		# OnClick we take the event and identify the button pressed
	def OnClick(self, event):
		global Send_Status_Press, BoardState, WhitePawnDis, BlackPawnDis


		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

		if WhitePawnDis == True or BlackPawnDis == True:
			Number = event.GetEventObject().GetId()
			if Number > 100 and Number < 109:
				if Number < 105:
					self.PawnHandler(1)
				else:
					self.PawnHandler(2)
			Send_Status_Press = str(Number)

		elif BoardState == 0:
			Status_Pressed = str(event.GetEventObject().GetId())
			NumberLetterDict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
			NumberDict = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
			Letter = NumberLetterDict[int(str(Status_Pressed)[1])]
			Number = NumberDict[int(str(Status_Pressed)[0])]
			Send_Status_Press = Letter + Number
		else:
			Status_Pressed = str(event.GetEventObject().GetId())
			NumberLetterDict = {1:"H",2:"G",3:"F",4:"E",5:"D",6:"C",7:"B",8:"A"}
			NumberDict = {1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8"}
			Letter = NumberLetterDict[int(str(Status_Pressed)[1])]
			Number = NumberDict[int(str(Status_Pressed)[0])]
			Send_Status_Press = Letter + Number

	# 1.18 Big Cleanup
	# I've decided to make code a bit cleaner by making more functions which will divide 
	# on click function, as it is very hard to understand and scroll through
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def UserCheckDisplay(self):
		global CurrentStatusMsg, GiveUPDis
		if GiveUPDis != "False":
			ShownMessage = self.Status.GetLabel()
			if ShownMessage != "You Gave Up" or ShownMessage != "Your Opponent Gave Up":
				if GiveUPDis == "You":
					self.Status.SetLabelText("You Gave Up")
				else:
					self.Status.SetLabelText("Your Opponent Gave Up")
		else:
			ShownMessage = self.Status.GetLabel()
			if ShownMessage != CurrentStatusMsg:
				self.Status.SetLabelText(CurrentStatusMsg)
		

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

	def YourTurnDisplay(self, StatusS):
		ShownMessage = self.Status.GetLabel()
		ShownMessageBool = ShownMessage == "Check Mate \n White Lost" or ShownMessage == "Check Mate \n Black Lost" or ShownMessage == "You Gave Up" or ShownMessage == "Your Opponent Gave Up"
		if StatusS == True and ShownMessageBool == False:
			self.Turn.SetLabelText("It Is Your Turn")
		else:
			if ShownMessage == "You Gave Up" or ShownMessage == "Your Opponent Gave Up":
				ShownTurn = self.Turn.GetLabel()
				if ShownTurn != "":
					self.Turn.SetLabelText("")
			self.Turn.SetLabelText("")

				


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

	def PawnHandler(self, Status):
		global attack,PawnBlock, ActiveMoves, ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, Dis, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate
		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		# This will handle pawn to another piece conversion
		# We get the side which needs this to be done
		PawnBlock = False
		if Status == 1:
			self.buttonWN.Destroy()
			self.buttonWR.Destroy()
			self.buttonWB.Destroy()
			self.buttonWQ.Destroy()
		else:
			self.buttonBN.Destroy()
			self.buttonBR.Destroy()
			self.buttonBB.Destroy()
			self.buttonBQ.Destroy()
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class App(wx.App):
	def OnInit(self):
		self.frame = Frame(parent=None, title="Chess" )
		self.frame.Centre()
		self.frame.SetMaxSize(wx.Size(800, 750))
		self.frame.SetMinSize(wx.Size(800, 750))
		self.frame.SetIcon(wx.Icon("Images/White_Pawn_Grey_Icon.ico"))
		self.frame.Show()
		return True 




# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
