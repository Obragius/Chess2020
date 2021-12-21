import wx
import os, os.path
import time
import wx.grid as gridlib
import sys


# This class will deal with
# -Switching between players
# -Creating and storing player names
User1Ram = None
User2Ram = None
ServerRun = True
User1 = ""
User2 = ""
User1Recieve = True
User2Recieve = True
PauseEvent = False
PawnWhiteClient = False
PawnBlackClient = False
UpdateTimeD = False
UpdateTimeDC = 0
GaveUpWhite = False
GaveUpBlack = False
CurrentStatusMsg = ""
moves = 2
logmoves = 0
attack = 0
W_Kingmoves = 0
B_Kingmoves = 0
White_King_Check = False
Black_King_Check = False
ButtonList = []
LastPress = 0
PawnHandler = [False,0,0]
GreenSpaces = False
CustomBoardValue = False
QueenK = False
MessageList = []
MessageListLast = ""
MessageListNumLow = 0
Refresh = False
labelUpdate = False
PlayersToSwitch = [1,2]
TwoKingRule = True
OnlineMove = ""
GreenBoardToSend = (
		[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
EmptyBoard = (
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
Dis = 0
ChooseAnyPiece = False
ChooseAnyRule = False
class Players():
	def GetPlayer(self):
		global moves, PlayersToSwitch
		if (moves % 2) == 0:
			player = PlayersToSwitch[0]
			return player
		else:
			player = PlayersToSwitch[1]
			return player

	def AttackCheck(self):
		global attack
		if attack == 0:
			return False
		else:
			return True

	def AttackSet(self, Moves, Piece):
		global attack, ActiveMoves, ActivePiece
		# This is the setup for allowing something to move
		ActivePiece = Piece
		ActiveMoves = Moves
		attack = 1



# This class will store the position of the pieces on the board
# The changes in this class will change the board state
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
	BoardLogLastMove = [0,0,"",0]

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

	def KingDeadZoneLog(self, king, king_position):
		# This method will log the new deadzones for kings, 
		# so that they are not able to move next to each other
		# This is basically a copy of kings basic moves
		DeadZone = []
		Row = int(str(king_position)[0])
		Column = int(str(king_position)[1])
		DeadZone.append(int((str(Row+1))+str(Column+1)))
		DeadZone.append(int((str(Row+1))+str(Column)))
		DeadZone.append(int((str(Row+1))+str(Column-1)))
		DeadZone.append(int((str(Row))+str(Column+1)))
		DeadZone.append(int((str(Row-1))+str(Column-1)))
		DeadZone.append(int((str(Row-1))+str(Column)))
		DeadZone.append(int((str(Row-1))+str(Column+1)))
		DeadZone.append(int((str(Row))+str(Column-1)))
		if king == 1:
			# then we set these values to the variable in this class
			Board.WhiteKingDZ = DeadZone
		else:
			Board.BlackKingDZ = DeadZone



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

	def BoardMovement(self, Initial, Last):
		global attack, ActiveMoves, ActivePiece
		# For this to work with different methods i need to add board boject
		# This method handles movement
		DoubleInt = Initial
		Destination = Last
		NewPiece = Board().GetPosition(DoubleInt)
		DestinationY = int(str(Destination)[0])
		DestinationX = int(str(Destination)[1])
		Board().BoardConfig[DestinationY-1][DestinationX-1] = NewPiece
		DoubleIntY = int(str(DoubleInt)[0])
		DoubleIntX = int(str(DoubleInt)[1])
		Board().BoardConfig[DoubleIntY-1][DoubleIntX-1] = "  "
		attack = 0
		ActivePiece = None
		ActiveMoves = None
		Stop = 1
		return Stop, DoubleInt

	def CheckMovementBoard(self, Initial, Last, BoardToMove):
		# This method deals with manipulating virtual board
		# To check for king to be attacked
		DoubleInt = Initial
		Destination = Last
		StrDoubleInt = str(DoubleInt)
		StrRow = StrDoubleInt[0]
		StrColumn = StrDoubleInt[1]
		Row = int(StrRow) - 1
		Column = int(StrColumn) - 1 
		NewPiece = BoardToMove[Row][Column]
		DestinationY = int(str(Destination)[0])
		DestinationX = int(str(Destination)[1])
		BoardToMove[DestinationY-1][DestinationX-1] = NewPiece
		DoubleIntY = int(str(DoubleInt)[0])
		DoubleIntX = int(str(DoubleInt)[1])
		BoardToMove[DoubleIntY-1][DoubleIntX-1] = "  "
		return BoardToMove

	def LogOfMovement(self, Piece, From, To, Player):
		# This will log the last movement action which was done, and will be used for
		# Pawn catch method
		Board().BoardLogLastMove[0] = From
		Board().BoardLogLastMove[1] = To
		Board().BoardLogLastMove[2] = Piece
		Board().BoardLogLastMove[3] = Player




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
			if MoveSpots[Moves] < 10:
				MoveSpots.remove(MoveSpots[Moves])
			else:
				Moves +=1
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
	def DirectionDistanceCollision(self, BoundMoves, Row, Column, Player, BoardC):
		# Checking for Straight Colision
		# I really tried to condense it in 0.235, but it didn't work
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
				if StartingRow[i]-1 == 8 or StartingRow[i] == -1:
					break
				CheckPos = BoardC[StartingRow[i]-1][Column-1]
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
			# Getting the longest horizontal distances the piece can move
			# And getting the postion which is the furhest
			TempPosition = str(BoundMoves[Moves])
			TempColumn = int(str(TempPosition[1]))
			TempColumnDistance = TempRow - Row
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
				if StartingColumn[i]-1 == 8 or StartingColumn[i] == -1:
					break
				CheckPos = BoardC[Row-1][StartingColumn[i]-1]
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

			

		# Checking for Diagonal Colision
		# Setting up the for directions to check in
		for i in range(4):
			# Setting the maximum distance we may check in
			for j in range(8):
				DiagDirection = [[+j+1,+j+1],[+j+1,-j-1],[-j-1,-j-1],[-j-1,+j+1]]
				# To check that this position exists within our Board
				if Column+DiagDirection[i][1] > 0 and Column+DiagDirection[i][1] < 9 and Row+DiagDirection[i][0] > 0 and Row+DiagDirection[i][0] < 9:
					Moves = 0
					while Moves < len(BoundMoves):
						# We check every direction and space starting from the piece itself
						ActualPosition = str(Row) + str(Column)
						NextPositionY = str(int(ActualPosition[0])+int(DiagDirection[i][0]))
						NextPositionX = str(int(ActualPosition[1])+int(DiagDirection[i][1]))
						# We develop a space which is next in line to check it
						NextPosition = NextPositionY + NextPositionX
						CheckPos = BoardC[int(NextPositionY)-1][int(NextPositionX)-1]
						# We get the piece from there and check it for certain values
						# We need to check the Player, because we need to check what space to start delete position from
						if Player == 1:
							if CheckPos == "  ":
								# if the value is empty just continue seraching
								Moves +=1
							elif CheckPos[0] == "B":
								# if the value has an enemy, delete all positions starting from the next one
								for k in range(8):
									# This is why the direction key has added parameters
									DiagDirectionK = [[+k+1,+k+1],[+k+1,-k-1],[-k-1,-k-1],[-k-1,+k+1]]
									NextPositionYK = str(int(NextPosition[0])+DiagDirectionK[i][0])
									NextPositionXK = str(int(NextPosition[1])+DiagDirectionK[i][1])
									NextPositionK = NextPositionYK + NextPositionXK
									if Moves ==  len(BoundMoves):
										pass
									else:
										if NextPositionK == str(BoundMoves[Moves]):
											BoundMoves.remove(BoundMoves[Moves])
								Moves +=1
							else:
								# if the value has an allie, delete all positions starting this one
								for k in range(8):
									# Direction key shows how much to goin each direction
									DiagDirectionK = [[+k,+k],[+k,-k],[-k,-k],[-k,+k]]
									NextPositionYK = str(int(NextPosition[0])+DiagDirectionK[i][0])
									NextPositionXK = str(int(NextPosition[1])+DiagDirectionK[i][1])
									NextPositionK = NextPositionYK + NextPositionXK
									if Moves ==  len(BoundMoves):
										pass
									else:
										if NextPositionK == str(BoundMoves[Moves]):
											BoundMoves.remove(BoundMoves[Moves])
								Moves +=1
						else:
							if CheckPos == "  ":
								Moves +=1
							elif CheckPos[0] == "W":
								for k in range(8):
									DiagDirectionK = [[+k+1,+k+1],[+k+1,-k-1],[-k-1,-k-1],[-k-1,+k+1]]
									NextPositionYK = str(int(NextPosition[0])+DiagDirectionK[i][0])
									NextPositionXK = str(int(NextPosition[1])+DiagDirectionK[i][1])
									NextPositionK = NextPositionYK + NextPositionXK
									if Moves ==  len(BoundMoves):
										pass
									else:
										if NextPositionK == str(BoundMoves[Moves]):
											BoundMoves.remove(BoundMoves[Moves])
								Moves +=1
							else:
								for k in range(8):
									DiagDirectionK = [[+k,+k],[+k,-k],[-k,-k],[-k,+k]]
									NextPositionYK = str(int(NextPosition[0])+DiagDirectionK[i][0])
									NextPositionXK = str(int(NextPosition[1])+DiagDirectionK[i][1])
									NextPositionK = NextPositionYK + NextPositionXK
									if Moves ==  len(BoundMoves):
										pass
									else:
										if NextPositionK == str(BoundMoves[Moves]):
											BoundMoves.remove(BoundMoves[Moves])
								Moves +=1

		# When all colisions have been accounted for, we can return the certain moves value
		return BoundMoves




		# This code will be split into two parts, to check if the way is obstructed or taken by an allie
	def TakenSpace(self, Position, Player, BoundMoves, BoardC):
		Moves = 0
		# Getting the Piece
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		Piece = BoardC[Row-1][Column-1]
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
					TempPiece = BoardC[TempRow-1][TempColumn-1]
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
			else:
				while Moves < len(BoundMoves):
					# Setting temporary postions for all posible moves
					TempPosition = str(BoundMoves[Moves])
					TempRow = int(str(TempPosition[0]))
					TempColumn = int(str(TempPosition[1]))
					TempPiece = BoardC[TempRow-1][TempColumn-1]
					if TempPiece[0] == "W":
						BoundMoves.remove(BoundMoves[Moves])
					else:
						Moves +=1

			# Now we need to disable jumping for all pieces
			PossibleMoves = Logic().DirectionDistanceCollision(BoundMoves, Row, Column, Player, BoardC)
			return PossibleMoves
		if Player == 2:
			if Piece[1] == "P":
				# Check the potential move spots for pieces
				while Moves < len(BoundMoves):
					# Setting temporary postions for all posible moves
					TempPosition = str(BoundMoves[Moves])
					TempRow = int(str(TempPosition[0]))
					TempColumn = int(str(TempPosition[1]))
					TempPiece = BoardC[TempRow-1][TempColumn-1]
					# getting rid of allie taken spaces and simple taken moves
					if TempPiece[0] == "B":
						BoundMoves.remove(BoundMoves[Moves])
					elif TempPiece[0] == "W":
						if Column == TempColumn:
							BoundMoves.remove(BoundMoves[Moves])
						else:
							Moves +=1
					else:
						if Column == TempColumn:
							Moves +=1
						else:
							BoundMoves.remove(BoundMoves[Moves])
			else:
				while Moves < len(BoundMoves):
					# Setting temporary postions for all posible moves
					TempPosition = str(BoundMoves[Moves])
					TempRow = int(str(TempPosition[0]))
					TempColumn = int(str(TempPosition[1]))
					TempPiece = BoardC[TempRow-1][TempColumn-1]
					if TempPiece[0] == "B":
						BoundMoves.remove(BoundMoves[Moves])
					else:
						Moves +=1
			# Now we need to disable jumping for all pieces
			PossibleMoves = Logic().DirectionDistanceCollision(BoundMoves, Row, Column, Player, BoardC)
			return PossibleMoves


			

	def PawnLogic(self, Position, Player, BoardC):
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
				CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
				return CertainMoves
			else:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row-1))+str(Column)))
				MoveSpots.append(int((str(Row-1))+str(Column+1)))
				MoveSpots.append(int((str(Row-1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
				CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
				# After all the normal logic we want to try pawn catching
				if Board().BoardLogLastMove[2] == "BP":
					# If it was a black pawn we can check for this
					DistanceHigh = int(str(Board().BoardLogLastMove[1])[0])
					DistanceLow = int(str(Board().BoardLogLastMove[0])[0])
					DistanceMiddle = int(str(Board().BoardLogLastMove[0])[0])+1
					# Here we get the position which we might want to add
					PositionMiddle = int(str(DistanceMiddle)+str(Board().BoardLogLastMove[0])[1])
					PositionColumn = int(str(Board().BoardLogLastMove[0])[1])
					DistanceResult = DistanceHigh - DistanceLow
					if DistanceResult == 2:
						RightColumn = Column+1
						LeftColumn = Column-1
						# If Our pawn is the one next to it, it will have this move added but we also need
						# additional functionality to change the bitmap objects
						if RightColumn == PositionColumn or LeftColumn == PositionColumn:
							if Row == 4:
								CertainMoves.append(PositionMiddle)
								Board().PawnAtribute[0] = True
								Board().PawnAtribute[1] = Board().BoardLogLastMove[1]
								Board().PawnAtribute[2] = PositionMiddle
				return CertainMoves
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
				CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
				return CertainMoves
			else:
				# Give a list of possible moves to go
				MoveSpots.append(int((str(Row+1))+str(Column)))
				MoveSpots.append(int((str(Row+1))+str(Column+1)))
				MoveSpots.append(int((str(Row+1))+str(Column-1)))
				BoundMoves = Logic().OutOfBounds(MoveSpots)
				CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
				if Board().BoardLogLastMove[2] == "WP":
					# If it was a black pawn we can check for this
					DistanceHigh = int(str(Board().BoardLogLastMove[1])[0])
					DistanceLow = int(str(Board().BoardLogLastMove[0])[0])
					DistanceMiddle = int(str(Board().BoardLogLastMove[0])[0])-1
					# Here we get the position which we might want to add
					PositionMiddle = int(str(DistanceMiddle)+str(Board().BoardLogLastMove[0])[1])
					PositionColumn = int(str(Board().BoardLogLastMove[0])[1])
					DistanceResult = DistanceLow - DistanceHigh
					if DistanceResult == 2:
						RightColumn = Column+1
						LeftColumn = Column-1
						# If Our pawn is the one next to it, it will have this move added but we also need
						# additional functionality to change the bitmap objects
						if RightColumn == PositionColumn or LeftColumn == PositionColumn:
							if Row == 5:
								CertainMoves.append(PositionMiddle)
								Board().PawnAtribute[0] = True
								Board().PawnAtribute[1] = Board().BoardLogLastMove[1]
								Board().PawnAtribute[2] = PositionMiddle
				return CertainMoves


	def QueenLogic(self, Position, Player, BoardC):
		global QueenK
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		# Logical postions to go
		ID = -1
		for j in range(8):
			for i in range(4):
				DiagDirection = [[+j,+j],[+j,-j],[-j,-j],[-j,+j]]
				if Column+DiagDirection[i][1] > 0 and Column+DiagDirection[i][1] < 9 and Row+DiagDirection[i][0] > 0 and Row+DiagDirection[i][0] < 9:
					MoveSpots.append(int((str(Row+DiagDirection[i][0]))+str(Column+DiagDirection[i][1])))
					ID +=1
				if ID > -1:
					if int(MoveSpots[ID]) == int(Position):
						MoveSpots.remove(MoveSpots[ID])
						ID -= 1
		# Give a list of possible moves to go
		i = 1
		while i < 8:
			if Row-i > 0:
				MoveSpots.append(int((str(Row-i))+str(Column)))
			if Row+i < 9:
				MoveSpots.append(int((str(Row+i))+str(Column)))
			if Column-i > 0:
				MoveSpots.append(int((str(Row))+str((Column-i))))
			if Column+i < 9:
				MoveSpots.append(int((str(Row))+str((Column+i))))
			i +=1
		BoundMoves = Logic().OutOfBounds(MoveSpots)
		CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
		if QueenK:
			AdditionalMethod = Logic().GetPieceMethod("N")
			AdditionalCertainMoves = AdditionalMethod(Position, Player, BoardC)
			if AdditionalCertainMoves != None:
				for Move in AdditionalCertainMoves:
					CertainMoves.append(Move)
		return CertainMoves


	def BishopLogic(self, Position, Player, BoardC):
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		# Logical postions to go
		ID = -1
		for j in range(8):
			for i in range(4):
				DiagDirection = [[+j,+j],[+j,-j],[-j,-j],[-j,+j]]
				if Column+DiagDirection[i][1] > 0 and Column+DiagDirection[i][1] < 9 and Row+DiagDirection[i][0] > 0 and Row+DiagDirection[i][0] < 9:
					MoveSpots.append(int((str(Row+DiagDirection[i][0]))+str(Column+DiagDirection[i][1])))
					ID +=1
				if ID > -1:
					if int(MoveSpots[ID]) == int(Position):
						MoveSpots.remove(MoveSpots[ID])
						ID -= 1
		BoundMoves = Logic().OutOfBounds(MoveSpots)
		CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
		return CertainMoves


	def KnightLogic(self, Position, Player, BoardC):
		# For the knoghts there is no point of sending them to the regular method, since they can jump and no collision 
		# is requred, this method provides all the certain moves itself
		# Setting up the list to get the moves to
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		# Logical postions to go
		MoveSpots.append(int((str(Row+2))+str(Column+1)))
		if Column - 1 > 0:
			MoveSpots.append(int((str(Row+2))+str(Column-1)))
		MoveSpots.append(int((str(Row+1))+str(Column+2)))
		if Column - 2 > 0:
			MoveSpots.append(int((str(Row+1))+str(Column-2)))
		MoveSpots.append(int((str(Row-2))+str(Column+1)))
		if Column - 1 > 0:
			MoveSpots.append(int((str(Row-2))+str(Column-1)))
		MoveSpots.append(int((str(Row-1))+str(Column+2)))
		if Column - 2 > 0:
			MoveSpots.append(int((str(Row-1))+str(Column-2)))
		# Get rid of high and low values not on the board
		Moves = 0
		while Moves < len(MoveSpots):
			if int(MoveSpots[Moves]) > 88 or int(MoveSpots[Moves]) < 11:
				MoveSpots.remove(MoveSpots[Moves])
			else:
				Moves +=1
		# Get rid of the values which the board cannot read
		for i in range(2):
			Moves = 0
			while Moves < len(MoveSpots):
				if int(str(MoveSpots[Moves])[i]) > 8 or int(str(MoveSpots[Moves])[i]) < 1:
					MoveSpots.remove(MoveSpots[Moves])
				else:
					Moves +=1
		# Checking for player to get rid of spaces with allie pieces
		if Player == 1:
			Moves = 0
			while Moves < len(MoveSpots):
				TempPosition = str(MoveSpots[Moves])
				TempRow = int(str(TempPosition[0]))
				TempColumn = int(str(TempPosition[1]))
				TempPiece = BoardC[TempRow-1][TempColumn-1]
				if TempPiece[0] == "W":
					MoveSpots.remove(MoveSpots[Moves])
				else:
					Moves +=1		
		else: 
			Moves = 0
			while Moves < len(MoveSpots):
				TempPosition = str(MoveSpots[Moves])
				TempRow = int(str(TempPosition[0]))
				TempColumn = int(str(TempPosition[1]))
				TempPiece = BoardC[TempRow-1][TempColumn-1]
				if TempPiece[0] == "B":
					MoveSpots.remove(MoveSpots[Moves])
				else:
					Moves +=1
		# Creating a certain move list for convention
		CertainMoves = MoveSpots
		return CertainMoves

	def KingDeadZoneDeleter(self, CertainMoves, Player):
		# This method will delete the ability of the king to move to a spot
		# If this spot is close to another king
		# First wee need to check which dead zone is associated with this player
		if Player == 1:
			CheckDZ = Board().BlackKingDZ
		else:
			CheckDZ = Board().WhiteKingDZ
		# We check thta the list isn't empty
		if CertainMoves != None:
			Moves = 0
			# Setting up a while loop to sort the moves
			while Moves < len(CertainMoves):
				# Flag will be a value to record that we need to delete this move
				Flag = 0
				# This will got through the list of zones which are not allowed
				Zones = 0
				while Zones < len(CheckDZ):
					if CertainMoves[Moves] == CheckDZ[Zones]:
						# If we find that the move of the king match the dead zone we mark it
						Flag = 1
					Zones +=1
				# If the move has been marked we delete it
				if Flag == 1:
					CertainMoves.remove(CertainMoves[Moves])
					# We do not increase the value of moves if we delete a value
				else:
					Moves+=1
					# If the flag has not been raised this move is ok to make
		# After all the moves have been checked against the correct deadzone we can return it
		return CertainMoves




	def KingLogic(self, Position, Player, BoardC):
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		MoveSpots.append(int((str(Row+1))+str(Column+1)))
		MoveSpots.append(int((str(Row+1))+str(Column)))
		MoveSpots.append(int((str(Row+1))+str(Column-1)))
		MoveSpots.append(int((str(Row))+str(Column+1)))
		MoveSpots.append(int((str(Row-1))+str(Column-1)))
		MoveSpots.append(int((str(Row-1))+str(Column)))
		MoveSpots.append(int((str(Row-1))+str(Column+1)))
		MoveSpots.append(int((str(Row))+str(Column-1)))
		BoundMoves = Logic().OutOfBounds(MoveSpots)
		TakenMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
		CertainMoves = Logic().castling(Position, Player, TakenMoves)
		NCertainMoves = Logic().KingDeadZoneDeleter(CertainMoves, Player)
		return NCertainMoves

	def KingLogicForCheck(self, Position, Player, BoardC):
		global W_Kingmoves, B_Kingmoves
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		MoveSpots.append(int((str(Row+1))+str(Column+1)))
		MoveSpots.append(int((str(Row+1))+str(Column)))
		MoveSpots.append(int((str(Row+1))+str(Column-1)))
		MoveSpots.append(int((str(Row))+str(Column+1)))
		MoveSpots.append(int((str(Row-1))+str(Column-1)))
		MoveSpots.append(int((str(Row-1))+str(Column)))
		MoveSpots.append(int((str(Row-1))+str(Column+1)))
		MoveSpots.append(int((str(Row))+str(Column-1)))
		BoundMoves = Logic().OutOfBounds(MoveSpots)
		TakenMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
		NCertainMoves = Logic().KingDeadZoneDeleter(TakenMoves, Player)
		return NCertainMoves


	def RookLogic(self, Position, Player, BoardC):
		MoveSpots = []
		Row = int(str(Position)[0])
		Column = int(str(Position)[1])
		# Give a list of possible moves to go
		i = 1
		while i < 8:
			if Row-i > 0:
				MoveSpots.append(int((str(Row-i))+str(Column)))
			if Row+i < 9:
				MoveSpots.append(int((str(Row+i))+str(Column)))
			if Column-i > 0:
				MoveSpots.append(int((str(Row))+str((Column-i))))
			if Column+i < 9:
				MoveSpots.append(int((str(Row))+str((Column+i))))
			i +=1
		BoundMoves = Logic().OutOfBounds(MoveSpots)
		CertainMoves = Logic().TakenSpace(Position, Player, BoundMoves, BoardC)
		return CertainMoves


	def castling(self, Position, Player, TakenMoves):
		global W_Kingmoves, B_Kingmoves, White_King_Check, Black_King_Check
		White_King_Check = Check().KingUnderCheck(Board.BoardConfig, 1)
		Black_King_Check = Check().KingUnderCheck(Board.BoardConfig, 2)
		# Checking for the player to set the right moves
		if Player == 1:
			# If the king Moved already, the moves will not be added
			if W_Kingmoves == 0:
				# If the king is under check
				if White_King_Check == False:
					# Checking conditions for castling
					if Board().BoardConfig[7][3] == "  " and Board().BoardConfig[7][2] == "  " and Board().BoardConfig[7][1] == "  " and Board().BoardConfig[7][0] == "WR" and Board().RookAtribute[2] == False:
						# We need to check if the postions are attacked by an enemy piece
						PositionsReturns = [None,None,None]
						# This will allow the castling
						TakenMovesApproved = True
						for i in range(3):
							PositionsReturns[i] = Check().AttackOnSpotCastling(Player, int(str(8)+str(i+2)))
							# Using our attackcehck method we return values if any return true we cancel castling
							if PositionsReturns[i] == True:
								TakenMovesApproved = False
						if TakenMovesApproved == True:
							TakenMoves.append(83)
					if Board().BoardConfig[7][5] == "  " and Board().BoardConfig[7][6] == "  " and Board().BoardConfig[7][7] == "WR" and Board().RookAtribute[3] == False:
						# We need to check if the postions are attacked by an enemy piece
						PositionsReturns = [None,None,None]
						# This will allow the castling
						TakenMovesApproved = True
						for i in range(2):
							PositionsReturns[i] = Check().AttackOnSpotCastling(Player, int(str(8)+str(i+6)))
							# Using our attackcehck method we return values if any return true we cancel castling
							if PositionsReturns[i] == True:
								TakenMovesApproved = False
						if TakenMovesApproved == True:
							TakenMoves.append(87)
			return TakenMoves
		else:
			if B_Kingmoves == 0:
				if Black_King_Check == False:
					if Board().BoardConfig[0][3] == "  " and Board().BoardConfig[0][2] == "  " and Board().BoardConfig[0][1] == "  " and Board().BoardConfig[0][0] == "BR" and Board().RookAtribute[0] == False:
						# We need to check if the postions are attacked by an enemy piece
						PositionsReturns = [None,None,None]
						# This will allow the castling
						TakenMovesApproved = True
						for i in range(3):
							PositionsReturns[i] = Check().AttackOnSpotCastling(Player, int(str(1)+str(i+2)))
							# Using our attackcehck method we return values if any return true we cancel castling
							if PositionsReturns[i] == True:
								TakenMovesApproved = False
						if TakenMovesApproved == True:
							TakenMoves.append(13)
					if Board().BoardConfig[0][5] == "  " and Board().BoardConfig[0][6] == "  " and Board().BoardConfig[0][7] == "BR" and Board().RookAtribute[1] == False:
						# We need to check if the postions are attacked by an enemy piece
						PositionsReturns = [None,None,None]
						# This will allow the castling
						TakenMovesApproved = True
						for i in range(2):
							PositionsReturns[i] = Check().AttackOnSpotCastling(Player, int(str(1)+str(i+6)))
							# Using our attackcehck method we return values if any return true we cancel castling
							if PositionsReturns[i] == True:
								TakenMovesApproved = False
						if TakenMovesApproved == True:
							TakenMoves.append(17)
			return TakenMoves
		




# This class will deal with position attacking
class Check():
	# Version 1.02 Has the begining for a big change to the check class
	def AttackOnSpotCastling(self, Player, PositionX):
		Parametr = False
		ListOfMoves = []
		# Checking for the player, because allies cannot attack
		if Player == 1:
			player = "B"
		else:
			player = "W"
		# Creating a nested loop to access all the positions on the board
		for i in range(8):
			for j in range(8):
				# I will name the position which we will be cheking PositionX
				# Attacker will be the piece we are checking
				Attacker = Board().BoardConfig[i][j]
				# if attacker mathces the correct team
				if Attacker[0] == player:
					# Preventing infinite loop
					# King moves are linked with castling and when the logic was checking that it got to an infinite loop of cheking king moves, this is a temporary work around
					Prevent = player + "K"
					if Attacker[1] == "K":
						if PositionX == 82 | PositionX == 83:
							if Board().BoardConfig[6][1] == Prevent:
								Parametr = True
						if PositionX == 82 | PositionX == 83 | PositionX == 84:
							if Board().BoardConfig[6][2] == Prevent:
								Parametr = True
						if PositionX == 86 | PositionX == 87:
							if Board().BoardConfig[6][6] == Prevent:
								Parametr = True
						if PositionX == 12 | PositionX == 13:
							if Board().BoardConfig[1][1] == Prevent:
								Parametr = True
						if PositionX == 12 | PositionX == 13 | PositionX == 14:
							if Board().BoardConfig[1][2] == Prevent:
								Parametr = True
						if PositionX == 16 | PositionX == 17:
							if Board().BoardConfig[1][6] == Prevent:
								Parametr = True
					else:
						# Getting the method for this piece
						Method = Logic().GetPieceMethod(Attacker[1])
						# Creating a string of the position id
						ID = str(i+1)+str(j+1)
						# Geeting the possible moves for that piece
						PossibleMoves = Method(ID, Player, Board().BoardConfig)
						# Typical error, sometimes posible moves return as none
						if PossibleMoves != None:
							Moves = 0
							while Moves < len(PossibleMoves):
								# Getting all the positions which enemies can move to
								ListOfMoves.append(PossibleMoves[Moves])
								Moves +=1
		Moves = 0
		while Moves < len(ListOfMoves):
			# If any of the move positions can attack a space we return a true value
			if PositionX == ListOfMoves[Moves]:
				Parametr = True
			Moves +=1
		return Parametr

	# 1.02 Change
	def KingUnderCheck(self, BoardToCheck, GivenKing):
		global White_King_Check, Black_King_Check
		# This is the set up to return the value of the check
		LocalCheck = False
		# This method will determine if the king is under attack in the board specified
		# First we need to find the king
		# We will be looking for the king that is given
		if GivenKing == 1:
			Local_King_Color = "W"
		else:
			Local_King_Color = "B"
		# Now that we found the king we need to find it on the board
		Local_King = Local_King_Color+"K"
		for i in range(8):
			for j in range (8):
				if BoardToCheck[i][j] == Local_King:
					# If we found the king then we give it's position as a variable contaning str
					Local_King_Position = str(i+1)+str(j+1)
		try:
			if int(Local_King_Position) == 1:
				pass 
		except:
			LocalCheck = "Break"
			return LocalCheck
		# Now we need to check if any of the Pieces of the other side can attack this spot
		if GivenKing == 1:
			Local_Piece_Color = "B"
		else:
			Local_Piece_Color = "W"
		# Now wee need to check all the pieces which can attack this king and if they do
		# we need to store their position and the spaces between this piece and the king
		# To do this we need to check the pieces that match the attacking color
		for i in range(8):
			for j in range(8):
				if BoardToCheck[i][j][0] == Local_Piece_Color:
					# This means that this piece is the color of the attackers
					# We can ignore the enemy king, because it cannot set check
					if BoardToCheck[i][j][1] == "K":
						pass
					else:
						# This is a piece which is able to set check and is the right color 
						# This part is going to take this piece and do manipulations to see if it can set check
						# by moving in the position of the king
						# First we want ot find out which type of piece
						PieceID = BoardToCheck[i][j][1]
						# Now we now the piece type
						PiecePosition = str(i+1)+str(j+1)
						# Now we know the piece position
						Local_Method = Logic().GetPieceMethod(PieceID)
						# We got the method for this piece
						# Now we will use the method for this piece
						# to see where it can move and return the values

						# To use this method we should declare the player as the second argument
						if BoardToCheck[i][j][0] == "W":
							GivePlayer = 1
						else:
							GivePlayer = 2
						LocalMoves = Local_Method(PiecePosition, GivePlayer , BoardToCheck)
						# We return the moves for this piece, so now we need to compare them to 
						# the position of the king and handle the matches, if match will be true store 
						# that king is under check
						Moves = 0
						# Sometimes the piece cannot move and it will throw error, so we will ask
						# if the list has a length
						if LocalMoves != None:
							while Moves < len(LocalMoves):
								if LocalMoves[Moves] == int(Local_King_Position):
									print("Player " + str(GivenKing)+ " is under check")
									LocalCheck = True
								Moves +=1
		return LocalCheck
						


	# 1.02 Change
	def CheckBeforeMove(self, Position, Player , CertainMoves):
		# This method will allow us to check the moves of the player in 
		# The logic of if the player is allowed to move
		# Sometimes players are not allowed to move some pieces due to 
		# it causing mate
		# In this method we will simulate a situation that the piece have moved to a new location and
		# Run a king undercheck method to see if this move should be deleted

		# These are the basics of the the things that we need to simulate a piece moving
		LocalPiece = Position
		LocalPlayer = Player
		ListOfUncheckedMoves = CertainMoves
		# Again we need to check that we have values in our list
		if ListOfUncheckedMoves != None:
			# Now we can do an while loop for each move in this list we can check it
			Moves = 0
			while Moves < len(ListOfUncheckedMoves):
				# Now we send information to reiceve a board where this piece have moved to these postions
				# We also need to create a virtual board
				VirtualBoard = (
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
						VirtualBoard[i][j] = Board().BoardConfig[i][j]

				N_VirtualBoard = Board().CheckMovementBoard(LocalPiece, ListOfUncheckedMoves[Moves], VirtualBoard)

				# This will return us a new virtual board which has the piece already moved

				# Now we want to check this New virtual board for a check
				MoveDeleter = Check().KingUnderCheck(N_VirtualBoard, LocalPlayer)
				# It will return either true or false and if it returns true, we delete the move
				if MoveDeleter == True:
					ListOfUncheckedMoves.remove(ListOfUncheckedMoves[Moves])
					# We dont want to increase the Moves counter if this happens, because all moves will be shifted
				else:
					# this means that this move is safe to make and we can allow player to move there
					# so we need to add 1 to the moves index
					Moves +=1
		# At the end we have checked all the moves we were given and can now display and allow them
		return ListOfUncheckedMoves




	# 1.02 Change
	def CheckMate(self, King):
		# This method will be able to return if the game has come to a
		# check, checkmate or draw

		# This should be split into two seperate processes which will give two outputs
		# Comparing those outputs will show us the situation the board is in right now

		# First: Check if the king is under check in the current board position
		CheckResult = Check().KingUnderCheck( Board().BoardConfig, King )
		MovesResult = False

		# Second to check if the player has any moves he can take
		# To check this we need to get the color of this king
		if King == 1:
			Piece_Color = "W"
		else:
			Piece_Color = "B"
		# This gives us the piece which we should look for
		# Now we need to create a nested loop to check all the pieces on the board
		for i in range(8):
			# We want to check that we did not find any moves yet
			if MovesResult == False:
				for j in range(8):
					# We want to check that we did not find any moves yet
					if MovesResult == False:
						# This will give is the piece and ij will be the position
						OurPiece = Board().BoardConfig[i][j]
						# Now we check that the piece is the right color
						if OurPiece[0] == Piece_Color:
							# This is the right color piece, now we want to see if it can move
							# If the piece can move we can return that moves are true straight away
							# First let's get the method for this piece
							Method = Logic().GetPieceMethod(OurPiece[1])
							# Now we can use this method to see if this piece can move
							# First we need the position of this piece
							PiecePosition = str(i+1)+str(j+1)
							# Now we want the number of the player, in our case it is the King argument
							# And the board to check will be Board().BoardConfig
							# Lets get all the posible moves for this piece
							ThisPieceMoves = Method(PiecePosition, King, Board().BoardConfig)
							# UPDATE I forgot to include the check before move method
							ThisPieceNewMoves = Check().CheckBeforeMove(PiecePosition, King, ThisPieceMoves)
							# Now we get a list and it will either be empty or not
							# If the list is empty we want to continue
							# If the list is not empty we want to set moves bool to True
							if ThisPieceNewMoves == []:
								# This will continue to the next space, so the next loop
								continue
							else:
								# This should crash all the loops, because if there is one 
								# move that can be made, we don't care about more moves
								print(PiecePosition)
								MovesResult = True
					else:
						# This means we found a move and can break out of the loop
						break
			else:
				# This means we found a move and can break out of the loop
				break
		# Now we have two results which can be returned, the combination
		# if which will determine the state of the game
		return CheckResult, MovesResult





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

		self.BasicGUI()
		self.panel = MyPanel(self)
		self.panel.SetBackgroundColour(wx.Colour( 123, 96, 68))



	def BasicGUI(self):
		FirstMethod = wx.Menu()
		# This is a Cosmetic addition which toggles the green spaces on the board
		GreenSpaces = FirstMethod.Append(wx.ID_OPEN, "Toggle GreenSpaces")
		self.Bind(wx.EVT_MENU, self.OnGreenSpacesActivate, GreenSpaces)
		SecondMethod = wx.Menu()
		RevertMove = SecondMethod.Append(wx.ID_CLOSE, "Revert Move")
		self.Bind(wx.EVT_MENU, self.OnRevertOneMove, RevertMove)
		Restart = SecondMethod.Append(wx.ID_SAVE, "Restart Game")
		self.Bind(wx.EVT_MENU, self.OnRestart, Restart)
		ChangePlayer = SecondMethod.Append(wx.ID_ABOUT, "Change Player")
		self.Bind(wx.EVT_MENU, self.OnChangePlayer, ChangePlayer)
		ChooseAny = SecondMethod.Append(wx.ID_HOME, "Choose Any Piece")
		self.Bind(wx.EVT_MENU, self.OnChooseAny, ChooseAny)
		ThirdMethod = wx.Menu()
		StartRevert = ThirdMethod.Append(wx.ID_COPY, "Revert to Start")
		self.Bind(wx.EVT_MENU, self.OnStartRevert, StartRevert)
		King2Rule = ThirdMethod.Append(wx.ID_FIND, "2 King Rule Toggle")
		self.Bind(wx.EVT_MENU, self.OnTwoKingRule, King2Rule)
		QK = ThirdMethod.Append(wx.ID_SPELL_CHECK, "QueenKnight Rule")
		self.Bind(wx.EVT_MENU, self.OnQK, QK)
		FourthMethod = wx.Menu()
		CustomBoard = FourthMethod.Append(wx.ID_OK, "Toggle Custom Board")
		self.Bind(wx.EVT_MENU, self.OnCustomBoard, CustomBoard)
		EmptyBoard = FourthMethod.Append(wx.ID_PRINT, "Create An Empty Board")
		self.Bind(wx.EVT_MENU, self.OnEmptyBoard, EmptyBoard)
		menuBar = wx.MenuBar()
		menuBar.Append(FirstMethod, "&Cosmetic")
		menuBar.Append(SecondMethod, "&Moves")
		menuBar.Append(ThirdMethod, "&Experimental")
		menuBar.Append(FourthMethod, "&Custom")
		self.SetMenuBar(menuBar)

	def _when_closed(self, event):
		sys.exit(1)

	def OnQK(self,event):
		global QueenK
		if QueenK == True:
			QueenK = False
		elif QueenK == False:
			QueenK = True

	def OnChooseAny(self, event):
		global ChooseAnyPiece, ChooseAnyRule
		if ChooseAnyPiece == True:
			ChooseAnyPiece = False
		elif ChooseAnyPiece == False:
			ChooseAnyPiece = True
			ChooseAnyRule = False

	def OnGreenSpacesActivate(self, Event):
		global GreenSpaces
		if GreenSpaces == True:
			GreenSpaces = False
		elif GreenSpaces == False:
			GreenSpaces = True
			
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()


		for i in range(8):
			for j in range(8):
				Piece = Board().BoardConfig[i][j]
				Row = i
				Column = j
				ImageID = ImageToLoadDict[Piece]
				self.panel.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])

	def OnRevertOneMove(self, Event):
		global MessageListNumLow, MessageList, MessageListLast, GreenBoardToSend
		self.panel.Status.SetLabelText("")
		Board().RevertMove()
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

		MessageListLast = "-"+MessageList[-1]
		for i in range(8):
			for j in range(8):
				Piece = Board().BoardConfig[i][j]
				Row = i
				Column = j
				ImageID = ImageToLoadDict[Piece]
				self.panel.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
		if len(MessageList) > 0:
			MessageList.remove(MessageList[-1])
		if MessageListNumLow > 0:
			MessageListNumLow -=1
		MsgToDis = ""
		Message = 0 + MessageListNumLow
		if Message != 0:
			Message -= 1
		MessageMax = len(MessageList)
		while Message < MessageMax:
			MsgToDis += MessageList[Message]
			Message +=1
		self.panel.Logs.SetLabelText(MsgToDis)

		GreenBoardToSend = (
		[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])

	def OnRestart(self, Event):
		global moves, LogOfMoves,UpdateTimeD,GreenBoardToSend,MessageListLast ,CurrentStatusMsg, logmoves,GaveUpWhite, GaveUpBlack, B_Kingmoves, W_Kingmoves, MessageListNumLow, MessageList
		self.panel.Status.SetLabelText("")
		for i in range(8):
			for j in range(8):
				Board().BoardConfig[i][j] = LogOfMoves[0][i][j]
		print(Board().BoardConfig)
		moves = 2
		W_Kingmoves = 0
		B_Kingmoves = 0
		GaveUpWhite = False
		GaveUpBlack = False
		UpdateTimeD = True
		CurrentStatusMsg = ""
		Board().RookAtribute = [False,False,False,False]
		LogOfMoves = ([[['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR',],
						['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP',],
						['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
						['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
						['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
						['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
						['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP',],
						['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR',]]])
		logmoves = 0
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()


		for i in range(8):
			for j in range(8):
				Piece = Board().BoardConfig[i][j]
				Row = i
				Column = j
				ImageID = ImageToLoadDict[Piece]
				self.panel.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
		MessageList = []
		MessageListLast = "&RESET"
		MsgToDis = ""
		Message = 0 + MessageListNumLow
		if Message != 0:
			Message -= 1
		MessageMax = len(MessageList)
		while Message < MessageMax:
			MsgToDis += MessageList[Message]
			Message +=1
		self.panel.Logs.SetLabelText(MsgToDis)
		self.panel.slider.SetMax(2)
		self.panel.slider.SetValue(0)

		GreenBoardToSend = (
		[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])



	def OnStartRevert(self, Event):
		global moves, LogOfMoves, logmoves, B_Kingmoves, W_Kingmoves, MessageListNumLow, MessageList
		self.panel.Status.SetLabelText("")
		Board().RevertMove()
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		Board().RookAtribute = [False,False,False,False]
		for i in range(8):
			for j in range(8):
				Piece = Board().BoardConfig[i][j]
				Row = i
				Column = j
				ImageID = ImageToLoadDict[Piece]
				self.panel.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
		if moves > 2:
			time.sleep(0.2)
			self.Update()
			self.OnStartRevert(None)
		else:
			self.OnRestart(Event)

	def OnCustomBoard(self, Event):
		# This will turn on the ability to create custom board to play
		global CustomBoardValue
		if CustomBoardValue == True:
			CustomBoardValue = False
			self.panel.RefreshCustomBoard(0,0)
			player = Players().GetPlayer()
			if player == 1:
				Reverse_Player = 2
			else:
				Reverse_Player = 1
			self.panel.UserCheckDisplay(0,Reverse_Player)
		elif CustomBoardValue == False:
			CustomBoardValue = True
			self.panel.CustomBoard(100000,0)

	def OnEmptyBoard(self, Event):
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		# Allows the player to set the board to empty
		for i in range(8):
			for j in range(8):
				Board().BoardConfig[i][j] = "  "
				Piece = Board().BoardConfig[i][j]
				Row = i
				Column = j
				ImageID = ImageToLoadDict[Piece]
				self.panel.button[Row][Column].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row][Column]])
		Board().BoardLog()

	def OnChangePlayer(self, Event):
		global PlayersToSwitch, attack
		# Changed to switch the assignment of players to not mess with moves count
		if PlayersToSwitch[0] == 1:
			PlayersToSwitch[0] = 2
			PlayersToSwitch[1] = 1
		else:
			PlayersToSwitch[0] = 1
			PlayersToSwitch[1] = 2
		# We Should drop the attack set
		attack = 0

	def OnTwoKingRule(self, Event):
		global TwoKingRule, OnlineMove
		if TwoKingRule == True:
			TwoKingRule = False
		else:
			TwoKingRule = True
		self.panel.MoveParsed(OnlineMove)



class MyPanel(wx.Panel):
	button = []
	hbox = []
	def __init__(self, parent):
		super(MyPanel,self).__init__(parent,pos = (0,0),size = (800, 750))

		self.OnInit()

	def OnInit(self):

		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

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
		hbox[8] = wx.BoxSizer(wx.HORIZONTAL)
		hbox[9] = wx.BoxSizer(wx.HORIZONTAL)
		hbox9 = wx.BoxSizer(wx.HORIZONTAL)

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
			hbox.append([])
			for j in range(10):
				if DisplayCase[i][j] == 1:
					# Getting the piece from board
					Piece = Board().GetPieceFromBoard((i-1),(j-1))
					# Getting the coresponding image to that piece
					ImageID = ImageToLoadDict[Piece]
					self.button[i-1].append([])
					self.button[i-1][j-1] = wx.BitmapButton(self, id =int(str(i)+str(j)), bitmap = ImageToLoad[ImageID][GreyAttribute[i-1][j-1]],  size = (55,55))
					hbox[i].Add(self.button[i-1][j-1], 0 , wx.ALIGN_CENTER)
				else:
					if ListForNumLet[GetTheNumLet] == 0:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (45,45))
						hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1
					elif ListForNumLet[GetTheNumLet] > 8:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (45,55))
						hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1
					else:
						self.image[GetTheNumLet] = wx.StaticBitmap(self, id=GetTheNumLet, bitmap = NumLetToLoad[ListForNumLet[GetTheNumLet]], size = (55,45))
						hbox[i].Add(self.image[GetTheNumLet], 0 , wx.ALIGN_CENTER)
						GetTheNumLet +=1


					

			

		self.Status = wx.StaticText(self, label = "", pos=(390,540), id = 1505)
		font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.Status.SetFont(font)
		self.SetBackgroundColour(wx.Colour( 123, 96, 68))

		self.Timer = wx.Timer(self, id= 999)
		self.Timer.Start(100)
		self.Bind(wx.EVT_TIMER, self.MakeMove)

		self.User1 = wx.StaticText(self, label = "User 1: ", pos=(10,640), id = 1705)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.User1.SetFont(font)

		self.User2 = wx.StaticText(self, label = "User 2: ", pos=(10,660), id = 1706)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.User2.SetFont(font)

		vbox.Add(hbox[0], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[1], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[2], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[3], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[4], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[5], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[6], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[7], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[8], 0, wx.ALIGN_CENTER)
		vbox.Add(hbox[9], 0, wx.ALIGN_CENTER)
		self.SetSizer(vbox)

		# We want to set the log of text where the moves will be displayed
		self.Logs = wx.StaticText(self, id = 500,label = "", pos = (670,60), size=(60,480))
		font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.Logs.SetFont(font)
		self.slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2, style = wx.SL_VERTICAL, pos = (760,60), size =(20,390) )
		self.Bind(wx.EVT_SLIDER, self.OnScroll)


		self.Bind(wx.EVT_BUTTON, self.OnClick)

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
	
	def MakeMove(self, event):
		global OnlineMove, ConfirmMove, GaveUpWhite, GaveUpBlack, UpdateTimeD, UpdateTimeDC, User1, User2
		user1 = self.User1.GetLabel()
		user2 = self.User2.GetLabel()
		Constant = "User 1: "
		if user1 != User1:
			self.User1.SetLabelText(Constant+User1)
		Constant = "User 2: "
		if user2 != User2:
			self.User2.SetLabelText(Constant+User2)
		if UpdateTimeD == True:
			if UpdateTimeDC < 1:
				UpdateTimeDC +=1
			else:
				UpdateTimeD = False
				UpdateTimeDC = 0
		if GaveUpWhite == False and GaveUpBlack == False:
			try:
				move = OnlineMove
				self.MoveParsed(move)
				OnlineMove = ""
			except:
				pass

	def MoveParsed(self, Move):
		global PawnHandler
		# This will allow us to parse moves as comands to the script
		if PawnHandler[0] == True:
			NewMove = int(Move)
			if NewMove == 101:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonWN.GetId())
				evt.SetEventObject(self.buttonWN)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonWN, evt)
			elif NewMove == 102:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonWR.GetId())
				evt.SetEventObject(self.buttonWR)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonWR, evt)
			elif NewMove == 103:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonWB.GetId())
				evt.SetEventObject(self.buttonWB)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonWB, evt)
			elif NewMove == 104:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonWQ.GetId())
				evt.SetEventObject(self.buttonWQ)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonWQ, evt)
			elif NewMove == 105:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonBN.GetId())
				evt.SetEventObject(self.buttonBN)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonBN, evt)
			elif NewMove == 106:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonBR.GetId())
				evt.SetEventObject(self.buttonBR)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonBR, evt)
			elif NewMove == 107:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonBB.GetId())
				evt.SetEventObject(self.buttonBB)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonBB, evt)
			elif NewMove == 108:
				evt = wx.CommandEvent(wx.wxEVT_BUTTON, self.buttonBQ.GetId())
				evt.SetEventObject(self.buttonBQ)
				evt.SetId(NewMove)
				wx.PostEvent(self.buttonBQ, evt)
		else:
			NumberLetterDict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
			NumberDict = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
			Piece = Move
			ButtonID0 = list(NumberLetterDict.keys())[list(NumberLetterDict.values()).index(Piece[0])]
			ButtonID1 = list(NumberDict.keys())[list(NumberDict.values()).index(Piece[1])]
			PieceButtonID = int(str(ButtonID1)+str(ButtonID0))
			button = self.button[int(str(ButtonID1))-1][int(str(ButtonID0))-1]
			evt =  wx.CommandEvent(wx.wxEVT_BUTTON, button.GetId())
			evt.SetEventObject(button)
			evt.SetId(PieceButtonID)
			wx.PostEvent(button, evt)
# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________


		# OnClick we take the event and identify the button pressed
	def OnClick(self, event):
		global attack, ActiveMoves, ChooseAnyRule , MessageListLast , QueenK ,PauseEvent,ChooseAnyPiece,PawnWhiteClient, PawnBlackClient, ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate, TwoKingRule, GreenBoardToSend
		startTime = time.time()
		Status_Pressed = str(event.GetEventObject().GetId())
		print(f"{Status_Pressed} StatusPressed")


		# From this we get the piece selected, so we need to ckeck wether it is the correct piece for this player
		player = Players().GetPlayer()

		Black_King_Check = False
		White_King_Check = False

		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()

		# Here we will check if we want to setup a cusotm board
		if CustomBoardValue == True:
			self.CustomBoard(Status_Pressed, player)

		else:
			if Refresh == True:
				self.RefreshCustomBoard(Status_Pressed, player)
			# This is the pawn handler segment
			# It's purpose is to handle the conversion when the pawn reaches the end of the board
			# and converts to another piece, we update the board and the display 
			if PawnHandler[0] == True:
				if len(Status_Pressed) == 3:
					self.PawnHandler(Status_Pressed, player)
				else:
					pass
			else:
				# Creating an update to get rid of green spaces 
				if ButtonList != None and ChooseAnyRule == False:
					if Status_Pressed != LastPress:
						Spaces = 0
						while Spaces < len(ButtonList):
							Piece = Board().BoardConfig[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])]
							ImageID = ImageToLoadDict[Piece]
							self.button[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])].SetBitmap(ImageToLoad[ImageID][GreyAttribute[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])]])
							Spaces +=1
				if ChooseAnyRule == False and ChooseAnyPiece == True:
					ButtonList = []



				# Now we need to send the button pressed to the Board to return the position which was selected
				Piece = Board().GetPosition(event.GetEventObject().GetId())
				# Now we need to confirm that this is his first press and not the attack move
				attackCheck = Players().AttackCheck()

				VirtualBoard = (
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
						VirtualBoard[i][j] = Board().BoardConfig[i][j]
				Bug = ["","",""]
				for i in range(1,3):
					if TwoKingRule == True:
						Bug[i] = Check().KingUnderCheck(VirtualBoard, i)
				print(Bug)
				if Bug[1] != "Break" and Bug[2] != "Break":
					if attackCheck == False:
						# We want to see if the player have selected his own piece
						Match = Pieces().PlayerPieceMatch(player, Piece[0])
						if Match == True:
							# This will return the right method for this piece
							Method = Logic().GetPieceMethod(Piece[1])
							# Get a list of positions where the piece can move
							CertainMoves = Method(Status_Pressed, player, Board().BoardConfig)
							PossibleMoves = Check().CheckBeforeMove(Status_Pressed, player, CertainMoves)
							if PossibleMoves != None:
									print(PossibleMoves)
									Players().AttackSet(PossibleMoves, Status_Pressed)
									# Printing the green background for possible moves to go to
									# If green spaces are selected
									if GreenSpaces == True:
										Moves = 0
										BoardToChange = Board().BoardToDisplay(PossibleMoves)
										for i in range(8):
											for j in range(8):
												GreenBoardToSend[i][j] = BoardToChange[i][j]
										for i in range(8):
											for j in range(8):
												Piece = BoardToChange[i][j]
												if len(Piece) > 2:
													ImageID = ImageToLoadGreenDict[Piece]
													self.button[i][j].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[i][j]])
													# Creating a list to later remove the green spaces
													ButtonList.append(str(i)+str(j))
													# Creating a variable to igonore removing the green spaces
													LastPress = Status_Pressed
									if PossibleMoves != [] and ChooseAnyPiece == False:
										ChooseAnyRule = True
							print("--- %s seconds ---" % (time.time() - startTime))
					else:
						Match = Pieces().PlayerPieceMatch(player, Piece[0])
						if (Match == True and ChooseAnyPiece == True) or (Match == True and ChooseAnyPiece == False and ChooseAnyRule == False):
							# This will return the right method for this piece
							Method = Logic().GetPieceMethod(Piece[1])
							# Get a list of positions where the piece can move
							CertainMoves= Method(Status_Pressed, player, Board().BoardConfig)
							PossibleMoves = Check().CheckBeforeMove(Status_Pressed, player, CertainMoves)
							if PossibleMoves != None:
									print(PossibleMoves)
									Players().AttackSet(PossibleMoves, Status_Pressed)
									# Printing the green background for possible moves to go to
									# If green spaces are selected
									if ChooseAnyRule == False:
										if GreenSpaces == True:
											Moves = 0
											BoardToChange = Board().BoardToDisplay(PossibleMoves)
											for i in range(8):
												for j in range(8):
													GreenBoardToSend[i][j] = BoardToChange[i][j]
											BoardToChange = Board().BoardToDisplay(PossibleMoves)
											for i in range(8):
												for j in range(8):
													Piece = BoardToChange[i][j]
													if len(Piece) > 2:
														ImageID = ImageToLoadGreenDict[Piece]
														self.button[i][j].SetBitmap(ImageToLoadGreen[ImageID][GreyAttribute[i][j]])
														# Creating a list to later remove the green spaces
														ButtonList.append(str(i)+str(j))
														# Creating a variable to igonore removing the green spaces
														LastPress = Status_Pressed
									if PossibleMoves != [] and ChooseAnyPiece == False:
										ChooseAnyRule = True
							print("--- %s seconds ---" % (time.time() - startTime))
						else:
							print("Match")
							Stop = 0
							Moves = 0
							if ActiveMoves != None:
								while Moves < len(ActiveMoves):
									if int(Status_Pressed) == ActiveMoves[Moves]:
										Stop, InitialUpdate = Board().BoardMovement(ActivePiece, Status_Pressed)
									if Stop == 1:
										# This will remove green spaces if chooseanyrule is on
										print(ChooseAnyRule)
										print(ButtonList)
										if ChooseAnyPiece == False:
											if ButtonList != None and ChooseAnyRule == True:
												Spaces = 0
												while Spaces < len(ButtonList):
													Piece = Board().BoardConfig[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])]
													ImageID = ImageToLoadDict[Piece]
													self.button[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])].SetBitmap(ImageToLoad[ImageID][GreyAttribute[int(ButtonList[Spaces][0])][int(ButtonList[Spaces][1])]])
													Spaces +=1
											ButtonList = []
										# Adding aditional functionality for the pawn cathing
										if Board().PawnAtribute[0] == True:
											if int(Status_Pressed) == int(Board().PawnAtribute[2]):
												print(Board().PawnAtribute)
												Row = int(str(Board().PawnAtribute[1])[0])
												Column = int(str(Board().PawnAtribute[1])[1])
												print(Row)
												print(Column)
												Board().BoardConfig[Row-1][Column-1] = "  "
												ImageID = ImageToLoadDict["  "]
												self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
										# Getting the piece from board
										Row = int(str(Status_Pressed)[0])
										Column = int(str(Status_Pressed)[1])
										Piece = Board().GetPieceFromBoard(Row-1,Column-1)
										# This is to catch rook moving to not allow castling if it did
										if Piece[1] == "R":
											if Piece[0] == "W":
												# If it is bottom left
												if Board().BoardConfig[7][0] != "WR":
													Board().RookAtribute[2] = True
												# If it is bottom right
												if Board().BoardConfig[7][7] != "WR":
													Board().RookAtribute[3] = True
											else:
												# If it is top left
												if Board().BoardConfig[0][0] != "BR":
													Board().RookAtribute[0] = True
												# If it is top right
												if Board().BoardConfig[0][7] != "BR":
													Board().RookAtribute[1] = True

										# This is to log the moevement we did
										Board().LogOfMovement(Piece, InitialUpdate, Status_Pressed, player)
										# After we log the movement we can use this information to display the moves log on the right
										# ___________________________________________________________________________________________
										NumberLetterDict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
										NumberDict = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
										PieceConvert = {"WP":"WPawn", "WN":"WKnight", "WB":"WBishop", "WR":"WRook", 
														"WK":"WKing", "WQ":"WQueen", "BP":"BPawn", "BN":"BKnight", 
														"BB":"BBishop", "BR":"BRook", "BK":"BKing", "BQ":"BQueen", }
										LastLabel = self.Logs.GetLabel()
										NameForPiece = PieceConvert[Piece]
										InitialPos = int(InitialUpdate)
										InitialPosLet = NumberLetterDict[int(str(InitialPos)[1])]
										InitialPosNum = NumberDict[int(str(InitialPos)[0])]
										FinalPos = int(Status_Pressed)
										FinalPosLet = NumberLetterDict[int(str(FinalPos)[1])]
										FinalPosNum = NumberDict[int(str(FinalPos)[0])]
										NewMsgToDis = "{NameForPiece}: {InitialPosLet}{InitialPosNum}:{FinalPosLet}{FinalPosNum}\n".format(NameForPiece=NameForPiece,InitialPosLet=InitialPosLet,
										InitialPosNum=InitialPosNum, FinalPosLet=FinalPosLet,FinalPosNum=FinalPosNum)
										MessageList.append(NewMsgToDis)
										MessageListLast = NewMsgToDis
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
										print(MessageList)
										# ___________________________________________________________________________________________
										# Getting the coresponding image to that piece
										ImageID = ImageToLoadDict[Piece]
										self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
										# Getting the logic for castling
										# ______________________________
										# Checking if the piece is the king
										if Piece[1] == "K":
											# Checking for player
											if player == 1:
												# We want to update the deadzone here
												Board().KingDeadZoneLog(1, Status_Pressed)
												if W_Kingmoves == 0:
													# Loading the four possible castling positions and getting bitmap update to the buttons
													if Board().BoardConfig[7][2] == "WK":
														Board().BoardConfig[7][3] = "WR"
														Board().BoardConfig[7][0] = "  "
														self.button[7][3].SetBitmap(ImageToLoad[ImageToLoadDict["WR"]][GreyAttribute[7][3]])
														self.button[7][0].SetBitmap(ImageToLoad[ImageToLoadDict["  "]][GreyAttribute[7][0]])
													# Updating the global varibale
													W_Kingmoves +=1
													print(Board().BoardConfig[7][6])
													if Board().BoardConfig[7][6] == "WK":
														Board().BoardConfig[7][5] = "WR"
														Board().BoardConfig[7][7] = "  "
														self.button[7][5].SetBitmap(ImageToLoad[ImageToLoadDict["WR"]][GreyAttribute[7][5]])
														self.button[7][7].SetBitmap(ImageToLoad[ImageToLoadDict["  "]][GreyAttribute[7][7]])
													W_Kingmoves +=1
											else:
												# We want to update the deadzone here
												Board().KingDeadZoneLog(2, Status_Pressed)
												if B_Kingmoves == 0:
													if Board().BoardConfig[0][2] == "BK":
														Board().BoardConfig[0][3] = "BR"
														Board().BoardConfig[0][0] = "  "
														self.button[0][3].SetBitmap(ImageToLoad[ImageToLoadDict["BR"]][GreyAttribute[0][3]])
														self.button[0][0].SetBitmap(ImageToLoad[ImageToLoadDict["  "]][GreyAttribute[0][0]])
													B_Kingmoves +=1
													if Board().BoardConfig[0][6] == "BK":
														Board().BoardConfig[0][5] = "BR"
														Board().BoardConfig[0][7] = "  "
														self.button[0][5].SetBitmap(ImageToLoad[ImageToLoadDict["BR"]][GreyAttribute[0][5]])
														self.button[0][7].SetBitmap(ImageToLoad[ImageToLoadDict["  "]][GreyAttribute[0][7]])
													B_Kingmoves +=1
										# ____________________________
										# Getting the piece from board
										Row = int(str(InitialUpdate)[0])
										Column = int(str(InitialUpdate)[1])
										Piece = Board().GetPieceFromBoard(Row-1,Column-1)
										# Getting the coresponding image to that piece
										ImageID = ImageToLoadDict[Piece]
										self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
										# here is the pawn conversion logic
										Board().PawnAtribute = [False, 0, 0]
										print(Board().BoardLogLastMove)
										if Board().BoardLogLastMove[2][1] == "P":
											if Board().BoardLogLastMove[2][0] == "W":
												if str(Board().BoardLogLastMove[1])[0] == "1":
													self.PieceToPick = wx.StaticText(self, label = "Pick One", pos=(400,890))
													font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
													self.PieceToPick.SetFont(font)
													self.buttonWN = wx.BitmapButton(self, id =101, bitmap = ImageToLoad[ImageToLoadDict["WN"]][0],  size = (55,55), pos=(170,560) )
													self.buttonWR = wx.BitmapButton(self, id =102, bitmap = ImageToLoad[ImageToLoadDict["WR"]][1],  size = (55,55), pos=(225,560) )
													self.buttonWB = wx.BitmapButton(self, id =103, bitmap = ImageToLoad[ImageToLoadDict["WB"]][0],  size = (55,55), pos=(280,560) )
													self.buttonWQ = wx.BitmapButton(self, id =104, bitmap = ImageToLoad[ImageToLoadDict["WQ"]][1],  size = (55,55), pos=(335,560) )
													PawnHandler = [True, Status_Pressed, 1]
													PawnWhiteClient = True
											else:
												if str(Board().BoardLogLastMove[1])[0] == "8":
													self.PieceToPick = wx.StaticText(self, label = "Pick One", pos=(400,890))
													font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
													self.PieceToPick.SetFont(font)
													self.buttonBN = wx.BitmapButton(self, id =105, bitmap = ImageToLoad[ImageToLoadDict["BN"]][0],  size = (55,55), pos=(170,560) )
													self.buttonBR = wx.BitmapButton(self, id =106, bitmap = ImageToLoad[ImageToLoadDict["BR"]][1],  size = (55,55), pos=(225,560) )
													self.buttonBB = wx.BitmapButton(self, id =107, bitmap = ImageToLoad[ImageToLoadDict["BB"]][0],  size = (55,55), pos=(280,560) )
													self.buttonBQ = wx.BitmapButton(self, id =108, bitmap = ImageToLoad[ImageToLoadDict["BQ"]][1],  size = (55,55), pos=(335,560) )
													PawnHandler = [True, Status_Pressed, 2]
													PawnBlackClient = True
										self.UserCheckDisplay(Status_Pressed, player)
										Board().BoardLog()
										GreenBoardToSend = (
										[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
								        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
										moves +=1
										ChooseAnyRule = False
										print("--- %s seconds ---" % (time.time() - startTime))
										break
									Moves +=1
				else:
					PauseEvent = False
					print("King Bug")

	# 1.18 Big Cleanup
	# I've decided to make code a bit cleaner by making more functions which will divide 
	# on click function, as it is very hard to understand and scroll through
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def UserCheckDisplay(self, Status_Pressed, player):
		global attack, ActiveMoves, ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate, CurrentStatusMsg
		# here I will display if the player is under check if custom board is off
		# Here we will be cheking for the game conditions and 
		# Displaying the correct information to the user
		if player == 1:
			Reverse_Player = 2
		else:
			Reverse_Player = 1
		CheckResult, MovesResult = Check().CheckMate(Reverse_Player)
		self.Status.SetLabelText("")
		CurrentStatusMsg = ""
		if Reverse_Player == 1:
			if CheckResult == False and MovesResult == False:
				self.Status.SetLabelText("Draw")
				CurrentStatusMsg = "Draw"
			elif CheckResult == True and MovesResult == True:
				self.Status.SetLabelText("White Under \n Check")
				CurrentStatusMsg = "White Under \n Check"
			elif CheckResult == True and MovesResult == False:
				self.Status.SetLabelText("Check Mate \n " + "White Lost")
				CurrentStatusMsg = "Check Mate \n " + "White Lost"
		if Reverse_Player == 2:
			if CheckResult == False and MovesResult == False:
				self.Status.SetLabelText("Draw")
				CurrentStatusMsg = "Draw"
			elif CheckResult == True and MovesResult == True:
				self.Status.SetLabelText("Black Under \n Check")
				CurrentStatusMsg = "Black Under \n Check"
			elif CheckResult == True and MovesResult == False:
				self.Status.SetLabelText("Check Mate \n " + "Black Lost")
				CurrentStatusMsg = "Check Mate \n " + "Black Lost"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	def CustomBoard(self, Status_Pressed, player):
		global attack, ActiveMoves, ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate
		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		# This will get rid of the large label when we turn on the custom board and will
		# and will give the correct label to the program when we go back
		label = self.Status.GetLabel()
		if label != "":
			self.Status.SetLabelText("")
		labelUpdate = True
		if Refresh == True:
			# Destroying the buttons if the player chose another spot
			self.buttonWN.Destroy()
			self.buttonWR.Destroy()
			self.buttonWB.Destroy()
			self.buttonWQ.Destroy()
			self.buttonWK.Destroy()
			self.buttonWP.Destroy()
			self.buttonBN.Destroy()
			self.buttonBR.Destroy()
			self.buttonBB.Destroy()
			self.buttonBQ.Destroy()
			self.buttonBK.Destroy()
			self.buttonBP.Destroy()
			self.buttonES1.Destroy()
			self.buttonES2.Destroy()
			self.PieceToPick.Destroy()
			Refresh = False
		# First the player must select the position on the board
		# Setting up the dictionary which will provide the string of the piece
		PieceIdentDict = {101:"WN", 102:"WR", 103:"WB",
						104:"WQ", 105:"WK", 106:"WP",
						107:"BN", 108:"BR", 109:"BB",
						110:"BQ", 111:"BK", 112:"BP",
						113:"  ", 114:"  "}
		# If the id fits the purpose get that id
		if int(Status_Pressed) < 89:
			# If the player clicks on the board it will display the possible pieces which he can set
			# The position to update variable will have the corrdinates of the space to update
			ThePositionToUpdate = int(Status_Pressed)
			self.PieceToPick = wx.StaticText(self, label = "Pick One", pos=(250,535))
			font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			self.PieceToPick.SetFont(font)
			self.buttonWN = wx.BitmapButton(self, id =101, bitmap = ImageToLoad[ImageToLoadDict["WN"]][0],  size = (55,55), pos=(80,560) )
			self.buttonWR = wx.BitmapButton(self, id =102, bitmap = ImageToLoad[ImageToLoadDict["WR"]][1],  size = (55,55), pos=(135,560) )
			self.buttonWB = wx.BitmapButton(self, id =103, bitmap = ImageToLoad[ImageToLoadDict["WB"]][0],  size = (55,55), pos=(190,560) )
			self.buttonWQ = wx.BitmapButton(self, id =104, bitmap = ImageToLoad[ImageToLoadDict["WQ"]][1],  size = (55,55), pos=(80,610) )
			self.buttonWK = wx.BitmapButton(self, id =105, bitmap = ImageToLoad[ImageToLoadDict["WK"]][0],  size = (55,55), pos=(135,610) )
			self.buttonWP = wx.BitmapButton(self, id =106, bitmap = ImageToLoad[ImageToLoadDict["WP"]][1],  size = (55,55), pos=(190,610) )
			self.buttonBN = wx.BitmapButton(self, id =107, bitmap = ImageToLoad[ImageToLoadDict["BN"]][0],  size = (55,55), pos=(345,560) )
			self.buttonBR = wx.BitmapButton(self, id =108, bitmap = ImageToLoad[ImageToLoadDict["BR"]][1],  size = (55,55), pos=(400,560) )
			self.buttonBB = wx.BitmapButton(self, id =109, bitmap = ImageToLoad[ImageToLoadDict["BB"]][0],  size = (55,55), pos=(455,560) )
			self.buttonBQ = wx.BitmapButton(self, id =110, bitmap = ImageToLoad[ImageToLoadDict["BQ"]][1],  size = (55,55), pos=(345,610) )
			self.buttonBK = wx.BitmapButton(self, id =111, bitmap = ImageToLoad[ImageToLoadDict["BK"]][0],  size = (55,55), pos=(400,610) )
			self.buttonBP = wx.BitmapButton(self, id =112, bitmap = ImageToLoad[ImageToLoadDict["BP"]][1],  size = (55,55), pos=(455,610) )
			self.buttonES1 = wx.BitmapButton(self, id =113, bitmap = ImageToLoad[ImageToLoadDict["  "]][1],  size = (55,55), pos=(265,560) )
			self.buttonES2 = wx.BitmapButton(self, id =114, bitmap = ImageToLoad[ImageToLoadDict["  "]][0],  size = (55,55), pos=(265,610) )
			Refresh = True
		elif int(Status_Pressed) > 100 and int(Status_Pressed) < 115:
			# We get the id of the piece which was selected
			PieceToDraw = int(Status_Pressed)
			# Then we get the String of the piece that was selected
			PieceStr = PieceIdentDict[PieceToDraw]
			# Then we change the piece on the board using the PieceConversion method
			Board().PieceConversionHandler(ThePositionToUpdate, PieceStr)
			# We want to log that these piece have appeared on the board
			Board().BoardLog()
			Row = int(str(ThePositionToUpdate)[0])
			Column = int(str(ThePositionToUpdate)[1])
			ImageID = ImageToLoadDict[PieceStr]
			# My friend has asked me to see if there will be a check, chemate or draw when he puts pieces on the board
			# so this will be an extension which will siplay the variants
			# -----------------------------------------------------------------------------------------------------
			# Here we will be cheking for the game conditions and 
			# Displaying the correct information to the user
			self.StatusCustom = wx.StaticText(self, label = "", pos=(560,585), size=(180,180))
			font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			self.StatusCustom.SetFont(font)

			King = ["WK","BK"]
			Local_King_Position = ["A","B"]
			KingBool = False
			for o in range(2):
				for i in range(8):
					for j in range (8):
						if Board().BoardConfig[i][j] == King[o]:
							# If we found the king then we give it's position as a variable contaning str
							Local_King_Position[o] = str(i+1)+str(j+1)
			try:
				int(Local_King_Position[0])
				int(Local_King_Position[1])
				KingBool = True
			except:
				pass
			if KingBool == True:
				CheckResultCustom = [False,False]
				MovesResultCustom = [False,False]
				# Here we have created two lists which will be using to see the condition for each king
				CheckResultCustom[0], MovesResultCustom[0] = Check().CheckMate(1)
				CheckResultCustom[1], MovesResultCustom[1] = Check().CheckMate(2)
				if CheckResultCustom[0] == False and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Draw                                                 ")
				elif CheckResultCustom[0] == True and MovesResultCustom[0] == True:
					self.StatusCustom.SetLabelText("White Under \n Check                                 ")
				elif CheckResultCustom[0] == True and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Check Mate \n " + "White Lost                        ")
				elif CheckResultCustom[1] == False and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Draw                                                 ")
				elif CheckResultCustom[1] == True and MovesResultCustom[1] == True:
					self.StatusCustom.SetLabelText("Black Under \n Check                                 ")
				elif CheckResultCustom[1] == True and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Check Mate       \n" + "Black Lost                   ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True:
					self.StatusCustom.SetLabelText("Both Kings       \n" + "Under Check                  ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Both Kings      \n" + "Under Check      \n" + "White Checkmate   ")
				elif CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Both Kings      \n" + "Under Check      \n" + "Black Checkmate   ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[0] == False and  MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Both   Kings \n" + "Under Checkmate")
			# -----------------------------------------------------------------------------------------------------


			# Update display
			self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
			try:
				self.buttonWN.Destroy()
				self.buttonWR.Destroy()
				self.buttonWB.Destroy()
				self.buttonWQ.Destroy()
				self.buttonWK.Destroy()
				self.buttonWP.Destroy()
				self.buttonBN.Destroy()
				self.buttonBR.Destroy()
				self.buttonBB.Destroy()
				self.buttonBQ.Destroy()
				self.buttonBK.Destroy()
				self.buttonBP.Destroy()
				self.buttonES1.Destroy()
				self.buttonES2.Destroy()
				self.PieceToPick.Destroy()
				Refresh = False
			except:
				pass
		elif int(Status_Pressed) == 100000:
			# This is to return the check message if the custom board was 
			# Switched on and off and on
			# Here we will be cheking for the game conditions and 
			# Displaying the correct information to the user
			self.StatusCustom = wx.StaticText(self, label = "", pos=(560,585), size=(180,180))
			font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			self.StatusCustom.SetFont(font)

			King = ["WK","BK"]
			Local_King_Position = ["A","B"]
			KingBool = False
			for o in range(2):
				for i in range(8):
					for j in range (8):
						if Board().BoardConfig[i][j] == King[o]:
							# If we found the king then we give it's position as a variable contaning str
							Local_King_Position[o] = str(i+1)+str(j+1)
			try:
				int(Local_King_Position[0])
				int(Local_King_Position[1])
				KingBool = True
			except:
				pass
			if KingBool == True:
				CheckResultCustom = [False,False]
				MovesResultCustom = [False,False]
				# Here we have created two lists which will be using to see the condition for each king
				CheckResultCustom[0], MovesResultCustom[0] = Check().CheckMate(1)
				CheckResultCustom[1], MovesResultCustom[1] = Check().CheckMate(2)
				if CheckResultCustom[0] == False and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Draw                                                 ")
				elif CheckResultCustom[0] == True and MovesResultCustom[0] == True:
					self.StatusCustom.SetLabelText("White Under \n Check                                 ")
				elif CheckResultCustom[0] == True and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Check Mate \n " + "White Lost                        ")
				elif CheckResultCustom[1] == False and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Draw                                                 ")
				elif CheckResultCustom[1] == True and MovesResultCustom[1] == True:
					self.StatusCustom.SetLabelText("Black Under \n Check                                 ")
				elif CheckResultCustom[1] == True and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Check Mate       \n" + "Black Lost                   ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True:
					self.StatusCustom.SetLabelText("Both Kings       \n" + "Under Check                  ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[0] == False:
					self.StatusCustom.SetLabelText("Both Kings      \n" + "Under Check      \n" + "White Checkmate   ")
				elif CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Both Kings      \n" + "Under Check      \n" + "Black Checkmate   ")
				if CheckResultCustom[0] == True and CheckResultCustom[1] == True and MovesResultCustom[0] == False and  MovesResultCustom[1] == False:
					self.StatusCustom.SetLabelText("Both   Kings \n" + "Under Checkmate")
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

	def PawnHandler(self,  Status_Pressed, player):
		global attack, ActiveMoves, PawnBlackClient,PawnWhiteClient ,ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, Dis, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate
		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		# This will handle pawn to another piece conversion
		# We get the side which needs this to be done
		PawnBlackClient = False
		PawnWhiteClient = False
		if PawnHandler[2] == 1:
			# We create a dictinary to know which piece is selected
			DictOfPiece = {101:"WN", 102:"WR", 103:"WB", 104:"WQ"}
			# Assign that piece
			PieceToSet = DictOfPiece[int(Status_Pressed)]
			# Get the position
			PositionToSet = PawnHandler[1]
			# Update the board
			Board().PieceConversionHandler(PositionToSet, PieceToSet)
			Row = int(str(PositionToSet)[0])
			Column = int(str(PositionToSet)[1])
			ImageID = ImageToLoadDict[PieceToSet]
			# Update display
			self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
			# Delete all values and buttons
			PawnHandler = [False,0,0]
			self.buttonWN.Destroy()
			self.buttonWR.Destroy()
			self.buttonWB.Destroy()
			self.buttonWQ.Destroy()
			self.PieceToPick.Destroy()
			AllDefendMoves = Check().CheckMate(1)
			# Setting dict to display loser or under check
			PlayerLoseDict = {1:"White",2:"Black"}
			if AllDefendMoves == []:
				self.Status.SetLabelText("Check Mate \n " + PlayerLoseDict[player] +  " Lost")
		else:
			DictOfPiece = {105:"BN", 106:"BR", 107:"BB", 108:"BQ"}
			PieceToSet = DictOfPiece[int(Status_Pressed)]
			PositionToSet = PawnHandler[1]
			Board().PieceConversionHandler(PositionToSet, PieceToSet)
			Row = int(str(PositionToSet)[0])
			Column = int(str(PositionToSet)[1])
			ImageID = ImageToLoadDict[PieceToSet]
			self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
			PawnHandler = [False,0,0]
			self.buttonBN.Destroy()
			self.buttonBR.Destroy()
			self.buttonBB.Destroy()
			self.buttonBQ.Destroy()
			self.PieceToPick.Destroy()
			AllDefendMoves = Check().CheckMate(2)
			# Setting dict to display loser or under check
			PlayerLoseDict = {1:"White",2:"Black"}
			if AllDefendMoves == []:
				self.Status.SetLabelText("Check Mate \n " + PlayerLoseDict[player] +  " Lost")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

	def RefreshCustomBoard(self, Status_Pressed, player):
		global attack, ActiveMoves, ActivePiece, moves, W_Kingmoves, B_Kingmoves, ButtonList, LastPress, PawnHandler, White_King_Check, Black_King_Check, GreenSpaces, Dis, CustomBoardValue, ThePositionToUpdate, MessageList, MessageListNumLow, Refresh, labelUpdate
		# Inserting images and converting to bitmap objects
		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict, GreyAttribute, ImageToLoadGreen ,ImageToLoadGreenDict, NumLetToLoad) = LoadingImages().initilize()
		# This will update the board if the player have switched of custom board settings
		if Refresh == True:
				# Destroying the buttons if the player chose another spot
				self.buttonWN.Destroy()
				self.buttonWR.Destroy()
				self.buttonWB.Destroy()
				self.buttonWQ.Destroy()
				self.buttonWK.Destroy()
				self.buttonWP.Destroy()
				self.buttonBN.Destroy()
				self.buttonBR.Destroy()
				self.buttonBB.Destroy()
				self.buttonBQ.Destroy()
				self.buttonBK.Destroy()
				self.buttonBP.Destroy()
				self.buttonES1.Destroy()
				self.buttonES2.Destroy()
				self.PieceToPick.Destroy()
				Refresh = False
		if labelUpdate == True:
			# If we have a board which has been updated the state of the board may have changed
			# So we need to display the correct infomation
			self.StatusCustom.SetLabelText("")
			CheckResult, MovesResult = Check().CheckMate(player)
			self.Status.SetLabelText("")
			if player == 1:
				if CheckResult == False and MovesResult == False:
					self.Status.SetLabelText("Draw")
				elif CheckResult == True and MovesResult == True:
					self.Status.SetLabelText("White Under \n Check")
				elif CheckResult == True and MovesResult == False:
					self.Status.SetLabelText("Check Mate \n " + "White Lost")
			if player == 2:
				if CheckResult == False and MovesResult == False:
					self.Status.SetLabelText("Draw")
				elif CheckResult == True and MovesResult == True:
					self.Status.SetLabelText("Black Under \n Check")
				elif CheckResult == True and MovesResult == False:
					self.Status.SetLabelText("Check Mate \n " + "Black Lost")
			labelUpdate=False

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
