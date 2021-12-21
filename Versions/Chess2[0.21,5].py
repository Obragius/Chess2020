import wx
import os, os.path


# This class will deal with
# -Switching between players
# -Creating and storing player names
moves = 2
attack = 0
class Players():
	def GetPlayer(self):
		global moves
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
		[['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR',],
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', 'WP', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP',],
        ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR',]])
	


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



# This will contain information about which pieces exist,
# how pieces can move, and their unique features
class Pieces():
	# To match player to the piece selected
	def PlayerPieceMatch(self, player, piece):
		if player == 1:
			if piece == "W":
				return True
			else:
				return False
		else:
			if piece == "B":
				return True
			else:
				return False


# This will check where the piece can move, and if the position 
# which is passed on is mathcing the possition where the piece can move
class Logic():
	# To get the right method to this exact piece
	def GetPieceMethod(self, piece):
		PieceDict = {"P":Logic().PawnLogic, "Q":Logic().QueenLogic, "B":Logic().BishopLogic, "N":Logic().KnightLogic,
					"K":Logic().KingLogic, "R":Logic().RookLogic}
		PieceLogic = PieceDict[piece]
		return PieceLogic


	# To delete all the moves which are outside of bounds
	def OutOfBounds(self, MoveSpots):
		Moves = 0
		while Moves < len(MoveSpots):
			Row = int(str(MoveSpots[Moves])[0])
			Column = int(str(MoveSpots[Moves])[1])
			if Row > 8 or Row < 1 or Column > 8 or Column < 1:
				MoveSpots.remove(MoveSpots[Moves])
			else:
				Moves +=1
		# returns only moves which are inside the Board
		BoundMoves = MoveSpots
		return BoundMoves

		# To give logical distances for Pawn, Rook, Bishop and Queen
	def DirectionDistanceCollision(self, BoundMoves, Row, Column):
		# Checking for Straight Colision
		print(Row)
		print(Column)
		for axis in range(2):
			Moves = 0
			HighestDistance = [0,0]
			HighestPos = ["",""]
			LowestDistance = [0,0]
			LowestPos = ["",""]
			TempAxis = [0,0]
			TempDistance = [0,0]
			AxisDirection = [Row, Column]
			while Moves < len(BoundMoves):
				# Getting the longest vertical distances the piece can move
				# And getting the postion which is the furhest
				TempPosition[axis] = str(BoundMoves[Moves])
				TempAxis[axis] = int(str(TempPosition[axis]))
				TempDistance[axis] = TempAxis[axis] - AxisDirection[axis]
				if TempDistance[axis] > 0:
					if TempDistance[axis] > HighestDistance[axis]:
						HighestDistance[axis] = TempDistance[axis]
						HighestPos[axis] = str(BoundMoves[Moves])
						Moves +=1
					else:
						Moves +=1
				elif TempDistance[axis] < 0:
					if TempDistance[axis] < LowestDistance[axis]:
						LowestDistance[axis] = TempDistance[axis]
						LowestPos[axis] = str(BoundMoves[Moves])
						Moves +=1
					else:
						Moves +=1
				else:
					Moves +=1
			CheckingAxis = [[0,0],[0,0]]
			StartingAxis = [[0,0],[0,0]]
			Direction = [+1,-1]
			Distance = [HighestDistance,LowestDistance]
			print(Distance[1])
			for j in range(2):
			# Setting up the loop which will do the math
				for k in range(2):
					CheckingAxis[axis][j] = AxisDirection[j] + Distance[axis][j]
					StartingAxis[axis][j] = AxisDirection[j] + Direction[j]
					print(CheckingAxis)
					while StartingAxis[axis][k] != CheckingAxis[axis][k]:
						if axis == 0:
							CheckPos = Board().BoardConfig[StartingAxis[axis][k]-1][Column-1]
							if CheckPos == "  ":
								StartingAxis[axis][k] += int(Direction[k])
							else:
								# If the space is not empty we need to delete all further moves
								Moves = 0
								while Moves < len(BoundMoves):
									# We look at all posible moves, and if they meet the criteria, they get canceled
									TempPosition = str(BoundMoves[Moves])
									if int(TempPosition[1]) == Column:
										if k == 0:
											if int(TempPosition[0]) > StartingAxis[axis][k]:
												BoundMoves.remove(BoundMoves[Moves])
											else:
												Moves +=1
										else:
											if int(TempPosition[0]) < StartingAxis[axis][k]:
												BoundMoves.remove(BoundMoves[Moves])
											else:
												Moves +=1
									else:
										Moves +=1
								StartingAxis[axis][k] = CheckingAxis[axis][k]
						else:
							CheckPos = Board().BoardConfig[Row-1][StartingAxis[axis][k]-1]
							if CheckPos == "  ":
								StartingAxis[axis][k] += int(Direction[k])
							else:
								# If the space is not empty we need to delete all further moves
								Moves = 0
								while Moves < len(BoundMoves):
									# We look at all posible moves, and if they meet the criteria, they get canceled
									TempPosition = str(BoundMoves[Moves])
									if int(TempPosition[0]) == Row:
										if k == 0:
											if int(TempPosition[1]) > StartingAxis[axis][k]:
												BoundMoves.remove(BoundMoves[Moves])
											else:
												Moves +=1
										else:
											if int(TempPosition[1]) < StartingAxis[axis][k]:
												BoundMoves.remove(BoundMoves[Moves])
											else:
												Moves +=1
									else:
										Moves +=1
								StartingAxis[axis][k] = CheckingAxis[axis][k]
		return BoundMoves
		# Vertical collision {Available in 0.21}
		# Setting temporary values to count against for the row
		Moves = 0
		HighestRowDistance = 0
		HighestRowPos = ""
		LowestRowDistance = 0
		LowestRowPos = ""
		while Moves < len(BoundMoves):
			# Getting the longest vertical distances the piece can move
			# And getting the postion which is the furhest
			TempPosition = str(BoundMoves[Moves])
			TempRow = int(str(TempPosition[0]))
			TempRowDistance = TempRow - Row
			if TempRowDistance > 0:
				if TempRowDistance > HighestRowDistance:
					HighestRowDistance = TempRowDistance
					HighestRowPos = str(BoundMoves[Moves])
					Moves +=1
				else:
					Moves +=1
			elif TempRowDistance < 0:
				if TempRowDistance < LowestRowDistance:
					LowestRowDistance = TempRowDistance
					LowestRowPos = str(BoundMoves[Moves])
					Moves +=1
				else:
					Moves +=1
			else:
				Moves +=1
		print('LowestRowDistance' + str(LowestRowDistance))
		print('HighestRowDistance' + str(HighestRowDistance))
		# New method to tidy up the high and low value loops
		# Setting up list variable to check against
		CheckingRow = ["",""]
		StartingRow = ["",""]
		Direction = [+1,-1]
		CheckingRow[0] = Row + HighestRowDistance
		StartingRow[0] = Row+1
		CheckingRow[1] = Row + LowestRowDistance
		StartingRow[1] = Row-1
		# Setting up the loop which will do the math
		for i in range(2):
			while StartingRow[i] != CheckingRow[i]:
				CheckPos = Board().BoardConfig[StartingRow[i]-1][Column-1]
				if CheckPos == "  ":
					StartingRow[i] += int(Direction[i])
				else:
					# If the space is not empty we need to delete all further moves
					Moves = 0
					while Moves < len(BoundMoves):
						# We look at all posible moves, and if they meet the criteria, they get canceled
						TempPosition = str(BoundMoves[Moves])
						if int(TempPosition[1]) == Column:
							if i == 0:
								if int(TempPosition[0]) > StartingRow[i]:
									BoundMoves.remove(BoundMoves[Moves])
								else:
									Moves +=1
							else:
								if int(TempPosition[0]) < StartingRow[i]:
									BoundMoves.remove(BoundMoves[Moves])
								else:
									Moves +=1
						else:
							Moves +=1
					StartingRow[i] = CheckingRow[i]

		# For highest value loop {Availabel in 0.19}
		# We need to check each space going up and cancel all spaces which are not empty
		# For lowest value loop {Availabel in 0.19}
		# We need to check each space going down and cancel all spaces which are not empty


		# Horizontal collision
		# Setting temporary values to count against for the column
		Moves = 0
		HighestColumnDistance = 0
		HighestColumnPos = ""
		LowestColumnDistance = 0
		LowestColumnPos = ""
		while Moves < len(BoundMoves):
			# Getting the longest vertical distances the piece can move
			# And getting the postion which is the furhest
			TempPosition = str(BoundMoves[Moves])
			TempColumn = int(str(TempPosition[1]))
			TempColumnDistance = TempColumn - Column
			if TempColumnDistance > 0:
				if TempColumnDistance > HighestColumnDistance:
					HighestColumnDistance = TempColumnDistance
					HighestColumnPos = str(BoundMoves[Moves])
					Moves +=1
				else:
					Moves +=1
			elif TempColumnDistance < 0:
				if TempColumnDistance < LowestColumnDistance:
					LowestColumnDistance = TempColumnDistance
					LowestColumnPos = str(BoundMoves[Moves])
					Moves +=1
				else:
					Moves +=1
			else:
				Moves +=1

		# New method to tidy up the high and low value loops
		# Setting up list variable to check against
		CheckingColumn = ["",""]
		StartingColumn = ["",""]
		Direction = [+1,-1]
		CheckingColumn[0] = Column + HighestColumnDistance
		StartingColumn[0] = Column+1
		CheckingColumn[1] = Column + LowestColumnDistance
		StartingColumn[1] = Column-1
		# Setting up the loop which will do the math
		for i in range(2):
			while StartingColumn[i] != CheckingColumn[i]:
				CheckPos = Board().BoardConfig[Row-1][StartingColumn[i]-1]
				if CheckPos == "  ":
					StartingColumn[i] += int(Direction[i])
				else:
					# If the space is not empty we need to delete all further moves
					Moves = 0
					while Moves < len(BoundMoves):
						# We look at all posible moves, and if they meet the criteria, they get canceled
						TempPosition = str(BoundMoves[Moves])
						if int(TempPosition[0]) == Row:
							if i == 0:
								if int(TempPosition[1]) > StartingColumn[i]:
									BoundMoves.remove(BoundMoves[Moves])
								else:
									Moves +=1
							else:
								if int(TempPosition[1]) < StartingColumn[i]:
									BoundMoves.remove(BoundMoves[Moves])
								else:
									Moves +=1
						else:
							Moves +=1
					StartingColumn[i] = CheckingColumn[i]
		return BoundMoves
			

		# Checking for Diagonal Colision

		# This code will be split into two parts, to check if the way is obstructed or taken by an allie
	def TakenSpace(self, Position, Player, BoundMoves):
		Moves = 0
		# Getting the Piece
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		Piece = Board().BoardConfig[Row-1][Column-1]
		# Check the player
		if Player == 1:
			# Check of its a pawn
			if Piece[1] == "P":
				# Check the potential move spots for pieces
				while Moves < len(BoundMoves):
					# Setting temporary postions for all posible moves
					TempPosition = str(BoundMoves[Moves])
					TempRow = int(str(TempPosition[0]))
					TempColumn = int(str(TempPosition[1]))
					TempPiece = Board().BoardConfig[TempRow-1][TempColumn-1]
					# getting rid of allie taken spaces and simple taken moves
					if TempPiece[0] == "W":
						BoundMoves.remove(BoundMoves[Moves])
					elif TempPiece[0] == "B":
						if Column == TempColumn:
							BoundMoves.remove(BoundMoves[Moves])
						else:
							Moves +=1
					else:
						if Column == TempColumn:
							Moves +=1
						else:
							BoundMoves.remove(BoundMoves[Moves])
			# Now we need to disable jumping for all pieces
			print('After removing pawn unlogical' + str(BoundMoves))
			PossibleMoves = Logic().DirectionDistanceCollision(BoundMoves, Row, Column)
			return PossibleMoves


			


	def PawnLogic(self, Position, Player):
		MoveSpots = []
		# Seperate black pieces and white pieces because going in a certain direction
		if Player == 1:
			# To see if the piece is in the starting position
			Row = int(str(Position)[0])
			Column = int(str(Position)[1])
			if Row == 7:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row-1))+str(Column)))
				MoveSpots.append(int((str(Row-2))+str(Column)))
				MoveSpots.append(int((str(Row-1))+str(Column+1)))
				MoveSpots.append(int((str(Row-1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
				print('Bound moves are' + str(BoundMoves))
				CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves)
				print('Certain Moves are' +str(CertainMoves))
			else:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row-1))+str(Column)))
				MoveSpots.append(int((str(Row-1))+str(Column+1)))
				MoveSpots.append(int((str(Row-1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
		else:
			# To see if the piece is in the starting position
			Row = int(str(Position)[0])
			Column = int(str(Position)[1])
			if Row == 2:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row+1))+str(Column)))
				MoveSpots.append(int((str(Row+2))+str(Column)))
				MoveSpots.append(int((str(Row+1))+str(Column+1)))
				MoveSpots.append(int((str(Row+1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
			else:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row+1))+str(Column)))
				MoveSpots.append(int((str(Row+1))+str(Column+1)))
				MoveSpots.append(int((str(Row+1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
	def QueenLogic(self):
		print('Queen')
	def BishopLogic(self):
		print('Bishop')
	def KnightLogic(self):
		print('Knight')
	def KingLogic(self):
		print('King')
	def RookLogic(self):
		print('Rook')




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
		imageFileBlack_King[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_King_White.png"
		imageFileBlack_Queen[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Queen_White.png"
		imageFileBlack_Bishop[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Bishop_White.png"
		imageFileBlack_Rook[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Rook_White.png"
		imageFileBlack_Knight[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Knight_White.png"
		imageFileBlack_Pawn[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Pawn_White.png"
		imageFileWhite_King[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_King_White.png"
		imageFileWhite_Queen[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Queen_White.png"
		imageFileWhite_Bishop[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Bishop_White.png"
		imageFileWhite_Rook[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Rook_White.png"
		imageFileWhite_Knight[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Knight_White.png"
		imageFileWhite_Pawn[0] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Pawn_White.png"
		imageFileBlack_King[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_King_Grey.png"
		imageFileBlack_Queen[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Queen_Grey.png"
		imageFileBlack_Bishop[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Bishop_Grey.png"
		imageFileBlack_Rook[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Rook_Grey.png"
		imageFileBlack_Knight[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Knight_Grey.png"
		imageFileBlack_Pawn[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\Black_Pawn_Grey.png"
		imageFileWhite_King[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_King_Grey.png"
		imageFileWhite_Queen[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Queen_Grey.png"
		imageFileWhite_Bishop[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Bishop_Grey.png"
		imageFileWhite_Rook[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Rook_Grey.png"
		imageFileWhite_Knight[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Knight_Grey.png"
		imageFileWhite_Pawn[1] = "C:\\Users\\lolki\\Desktop\\Python\\Chess 2.0\\Images\\White_Pawn_Grey.png"

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
		GreyAttribute = 0
		# Trying method to print all the buttons in a loop
		self.button = []
		for i in range(8):
			self.button.append([])
			hbox.append([])
			for j in range(8):
				if (i % 2) == 0:
					if (j % 2) == 0:
						GreyAttribute = 0

						# Getting the piece from board
						Piece = Board().GetPieceFromBoard(i,j)
						# Getting the coresponding image to that piece
						ImageID = ImageToLoadDict[Piece]

						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = ImageToLoad[ImageID][GreyAttribute], size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
					else:
						GreyAttribute = 1

						# Getting the piece from board
						Piece = Board().GetPieceFromBoard(i,j)
						# Getting the coresponding image to that piece
						ImageID = ImageToLoadDict[Piece]

						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = ImageToLoad[ImageID][GreyAttribute], size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
				else:
					if (j % 2) == 0:
						GreyAttribute = 1

						# Getting the piece from board
						Piece = Board().GetPieceFromBoard(i,j)
						# Getting the coresponding image to that piece
						ImageID = ImageToLoadDict[Piece]

						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = ImageToLoad[ImageID][GreyAttribute], size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)
					else:
						GreyAttribute = 0

						# Getting the piece from board
						Piece = Board().GetPieceFromBoard(i,j)
						# Getting the coresponding image to that piece
						ImageID = ImageToLoadDict[Piece]

						self.button[i].append([])
						self.button[i][j] = wx.BitmapButton(self, id =int(str(i+1)+str(j+1)), bitmap = ImageToLoad[ImageID][GreyAttribute], size = (100,100))
						hbox[i].Add(self.button[i][j], 0 , wx.ALIGN_CENTER)

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
			# We want to see if the player have selected his own piece
			Match = Pieces().PlayerPieceMatch(player, Piece[0])
			if Match == True:
				# This will return the right method for this piece
				a = Logic().GetPieceMethod(Piece[1])
				# Get a list of positions where the piece can move
				PossibleMoves = a(Status_Pressed, player)
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
