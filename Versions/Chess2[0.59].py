import wx
import os, os.path
import time


# This class will deal with
# -Switching between players
# -Creating and storing player names
moves = 2
attack = 0
W_Kingmoves = 0
B_Kingmoves = 0
White_King_Check = False
Black_King_Check = False
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

	def AttackSet(self, Moves, Piece):
		global attack, ActiveMoves, ActivePiece
		# This is the setup for allowing something to move
		ActivePiece = Piece
		ActiveMoves = Moves
		attack = 1
		print('Attack is set')



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


	def KingLogic(self, Position, Player, BoardC):
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
		CertainMoves = Logic().castling(Position, Player, TakenMoves)
		return TakenMoves


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
		global W_Kingmoves, B_Kingmoves
		# Checking for the player to set the right moves
		if Player == 1:
			# If the king Moved already, the moves will not be added
			if W_Kingmoves == 0:
				# Checking conditions for castling
				if Board().BoardConfig[7][3] == "  " and Board().BoardConfig[7][2] == "  " and Board().BoardConfig[7][1] == "  " and Board().BoardConfig[7][0] == "WR":
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
				if Board().BoardConfig[7][5] == "  " and Board().BoardConfig[7][6] == "  " and Board().BoardConfig[7][7] == "WR":
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
				if Board().BoardConfig[0][3] == "  " and Board().BoardConfig[0][2] == "  " and Board().BoardConfig[0][1] == "  " and Board().BoardConfig[0][0] == "BR":
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
				if Board().BoardConfig[0][5] == "  " and Board().BoardConfig[0][6] == "  " and Board().BoardConfig[0][7] == "BR":
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

	def KingUnderCheck(self, BoardToCheck):
		# To use this method effectively, we have to get the board set up here as an object
		# we can copy most of this procedure from attackoncastling
		Parametr = [False,False]
		ListOfMoves = [[],[]]
		player = ["B","W"]
		King = ["WK","BK"]
		MethodAtribute = [2,1]
		PositionX = [0,0]
		for k in range(2):
			# We need to find the king for this ocasion
			Player = player[k]
			for i in range(8):
				for j in range(8):
					Position = BoardToCheck[i][j]
					if Position == King[k]:
						PositionX[k] = int(str(i+1)+str(j+1))
			# Creating a nested loop to access all the positions on the board
			for i in range(8):
				for j in range(8):
					# Attacker will be the piece we are checking
					Attacker = BoardToCheck[i][j]
					# if attacker mathces the correct team
					if Attacker[0] == player[k]:
						# King cannot do check
						if Attacker[1] == "K":
							pass
						else:
							# Getting the method for this piece
							Method = Logic().GetPieceMethod(Attacker[1])
							# Creating a string of the position id
							ID = str(i+1)+str(j+1)
							# Geeting the possible moves for that piece
							PossibleMoves = Method(ID, MethodAtribute[k], BoardToCheck)
							# Typical error, sometimes posible moves return as none
							if PossibleMoves != None:
								# print(PossibleMoves)
								Moves = 0
								while Moves < len(PossibleMoves):
									# Getting all the positions which enemies can move to
									ListOfMoves[k].append(PossibleMoves[Moves])
									Moves +=1
		# print(ListOfMoves)
		for k in range(2):
			Moves = 0
			while Moves < len(ListOfMoves[k]):
				# If any of the move positions can attack a space we return a true value
				if PositionX[k] == ListOfMoves[k][Moves]:
					Parametr[k] = True
				Moves +=1
		if Parametr[0] == True:
			# pass
			print("White king under c")
		if Parametr[1] == True:
			# pass
			print("Black king under c")

		return Parametr


	def CheckBeforeMove(self, Position, Player , CertainMoves):
		# Creating a dict for the player to assign the correct parametr
		PlayerDict = {1:0,2:1}
		# For every move in the list of moves for this piece we want to see if there is 
		# any to not return 
		# Setting up the new board
		Initial_Board = (
					[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
			        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])
		if CertainMoves != None:
			Moves = 0
			while Moves < len(CertainMoves):
				# Creating a new board from the original
				for i in range(8):
					for j in range(8):
						Initial_Board[i][j] = Board().BoardConfig[i][j]
				# Setting values to move the piece
				Initial = int(Position)
				Last = CertainMoves[Moves]
				# Creating the board where the piece moved
				CheckBoard = Board().CheckMovementBoard(Initial, Last, Initial_Board)
				# Checking if the king is now under attack
				Parametr = Check().KingUnderCheck(CheckBoard)
				# If the parametr shows True, it means that we should cancell that move
				if Parametr[PlayerDict[Player]] == True:
					CertainMoves.remove(CertainMoves[Moves])
				else:
					# Otherwise We should keep the move as an option
					Moves +=1
		#Then return the allowed values 
		return CertainMoves





# Should be called after Check returns (True) to see if the 
# game is over
class CheckMate():
	pass
		


# This class deals with players interaction inside the code
# This class will send object id to the code and will display the board to the user
# GUI
# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________

class LoadingImages():
	def initilize(self):
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

		# Returning all the images
		return (imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, 
		imageBlack_Pawn ,imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook,
		imageWhite_Knight ,imageWhite_Pawn ,ImageToLoad ,ImageToLoadDict)


# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
class Frame(wx.Frame):
	def __init__ (self, parent, title):
		super(Frame, self).__init__(parent, title=title, size = (900, 900), pos=(900,90))

		self.panel = MyPanel(self)



class MyPanel(wx.Panel):
	button = []
	hbox = []
	def __init__(self, parent):
		super(MyPanel,self).__init__(parent)

		(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
		imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
		ImageToLoad ,ImageToLoadDict) = LoadingImages().initilize()

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

# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________


		# OnClick we take the event and identify the button pressed
	def OnClick(self, event):
		global attack, ActiveMoves, ActivePiece, moves, W_Kingmoves, B_Kingmoves
		startTime = time.time()
		Status_Pressed = str(event.GetEventObject().GetId())
		# This is code for testing purposes
		self.Status.SetLabelText(Status_Pressed)


		# Now we need to send the button pressed to the Board to return the position which was selected
		Piece = Board().GetPosition(event.GetEventObject().GetId())
		# From this we get the piece selected, so we need to ckeck wether it is the correct piece for this player
		player = Players().GetPlayer()
		# Now we need to confirm that this is his first press and not the attack move
		attackCheck = Players().AttackCheck()
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
					print("--- %s seconds ---" % (time.time() - startTime))

		else:
			Match = Pieces().PlayerPieceMatch(player, Piece[0])
			if Match == True:
				# This will return the right method for this piece
				Method = Logic().GetPieceMethod(Piece[1])
				# Get a list of positions where the piece can move
				CertainMoves= Method(Status_Pressed, player, Board().BoardConfig)
				PossibleMoves = Check().CheckBeforeMove(Status_Pressed, player, CertainMoves)
				if PossibleMoves != None:
					print(PossibleMoves)
					Players().AttackSet(PossibleMoves, Status_Pressed)
					print("--- %s seconds ---" % (time.time() - startTime))
			else:
				Stop = 0
				Moves = 0
				if ActiveMoves != None:
					while Moves < len(ActiveMoves):
						if int(Status_Pressed) == ActiveMoves[Moves]:
							Stop, InitialUpdate = Board().BoardMovement(ActivePiece, Status_Pressed)
						if Stop == 1:
							# Inserting images and converting to bitmap objects
							(imageBlack_King ,imageBlack_Queen ,imageBlack_Bishop ,imageBlack_Rook ,imageBlack_Knight, imageBlack_Pawn ,
							imageWhite_King ,imageWhite_Queen ,imageWhite_Bishop ,imageWhite_Rook ,imageWhite_Knight ,imageWhite_Pawn ,
							ImageToLoad ,ImageToLoadDict) = LoadingImages().initilize()

							# Naming variable to set grey background
							GreyAttribute = ([[0, 1, 0, 1, 0, 1, 0, 1,],
									        [1, 0, 1, 0, 1, 0, 1, 0,],
									        [0, 1, 0, 1, 0, 1, 0, 1,],
									        [1, 0, 1, 0, 1, 0, 1, 0,],
									        [0, 1, 0, 1, 0, 1, 0, 1,],
									        [1, 0, 1, 0, 1, 0, 1, 0,],
									        [0, 1, 0, 1, 0, 1, 0, 1,],
									        [1, 0, 1, 0, 1, 0, 1, 0,]])
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
							print(Piece)
							# This is to log the moevement we did
							Board().LogOfMovement(Piece, InitialUpdate, Status_Pressed, player)
							# Getting the coresponding image to that piece
							ImageID = ImageToLoadDict[Piece]
							self.button[Row-1][Column-1].SetBitmap(ImageToLoad[ImageID][GreyAttribute[Row-1][Column-1]])
							# Getting the logic for castling
							# ______________________________
							# Checking if the piece is the king
							if Piece[1] == "K":
								# Checking for player
								if player == 1:
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
							Parametr = Check().KingUnderCheck(Board().BoardConfig)
							Board().PawnAtribute = [False, 0, 0]
							print(Board().BoardLogLastMove)
							moves +=1
							print("--- %s seconds ---" % (time.time() - startTime))
							break
						Moves +=1
		


		
		

class App(wx.App):
	def OnInit(self):
		self.frame = Frame(parent=None, title="Chess" )
		self.frame.Show()
		return True 


app = App()
app.MainLoop()

# ___________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________
