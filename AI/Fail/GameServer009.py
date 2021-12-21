import multiprocessing
import time
import wx
import os
import sys
import threading

import ChessControllerAI002 as Chess


def BoardEvaluationMod(Board):
	# Values
	ValuePawn = 400
	ValueKnight = 800
	ValueBishop = 900
	ValueRook = 1200
	ValueQueen = 2000
	ValueKing = 0
	EvaluationDict = {"P":ValuePawn, "N":ValueKnight, "B":ValueBishop, "R":ValueRook, "Q":ValueQueen, "K":ValueKing}
	Eval = 0
	for I in range(8):
		for J in range(8):
			Piece = Board[I][J]
			if Piece == "  ":
				ABSValue = 0
			else:
				ABSValue = EvaluationDict[Piece[1]]
			if ABSValue != 0:
				if Piece[0] == "W":
					if Piece[1] != "K":
						if I <= 3:
							ABSValue = ABSValue + 80
						elif I <= 4:
							ABSValue = ABSValue + 40
						elif I <= 5:
							ABSValue = ABSValue + 20
					if Piece[1] == "P":
						if I == 0:
							ABSValue = ABSValue + 500
						if I <= 1:
							ABSValue = ABSValue + 10
						if I <= 2:
							ABSValue = ABSValue + 10
						if I <= 3:
							ABSValue = ABSValue + 10
						if I <= 4:
							ABSValue = ABSValue + 10
						if I <= 5:
							ABSValue = ABSValue + 10
						if J >= 3 and J <= 4 and I <= 5:
							ABSValue = ABSValue + 60
						elif J >= 2 and J <= 5 and I <= 5:
							ABSValue = ABSValue + 40
					Eval = Eval - ABSValue
				else:
					if Piece[1] != "K":
						if I >= 4:
							ABSValue = ABSValue + 80
						elif I >= 3:
							ABSValue = ABSValue + 40
						elif I >= 2:
							ABSValue = ABSValue + 20
					if Piece[1] == "P":
						if I == 7:
							ABSValue = ABSValue + 500
						if I >= 6:
							ABSValue = ABSValue + 10
						if I >= 5:
							ABSValue = ABSValue + 10
						if I >= 4:
							ABSValue = ABSValue + 10
						if I >= 3:
							ABSValue = ABSValue + 10
						if I >= 2:
							ABSValue = ABSValue + 10
						if J >= 3 and J <= 4 and I >= 2:
							ABSValue = ABSValue + 60
						elif J >= 2 and J <= 5 and I >= 2:
							ABSValue = ABSValue + 40
					Eval = Eval + ABSValue
	return Eval


def GetAllmoves(Player, Board):
	Allmoves = []
	for I in range(8):
		for J in range(8):
			Piece = Board[I][J]
			if (Chess.Pieces().PlayerPieceMatch(Player, Piece[0])):
				Status_Pressed = str(I+1)+str(J+1)
				PossibleMoves = Chess.Logic().AIGetPieceMethod(Piece[1], Status_Pressed, Player, Board)
				if PossibleMoves != None:
					for move in PossibleMoves:
						Allmoves.append((Status_Pressed , move))
	return Allmoves

def BestMoves(Player, Allmoves, Board):
	TheMoves = ["","",""]
	TheMovesScore = [0,0,0]
	for Move in Allmoves:
		BoardToMove = (
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
				BoardToMove[i][j] = Board[i][j]
		DoubleInt = Move[0]
		Destination = Move[1]
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
		Score = BoardEvaluationMod(BoardToMove)
		if Player == 1:
			if TheMovesScore[0] == 0 and TheMoves[0] == "":
				TheMovesScore[0] = Score
				TheMoves[0] = Move
			elif TheMovesScore[1] == 0 and TheMoves[1] == "":
				TheMovesScore[1] = Score
				TheMoves[1] = Move
			elif TheMovesScore[2] == 0 and TheMoves[2] == "":
				TheMovesScore[2] = Score
				TheMoves[2] = Move
			elif Score < TheMovesScore[0]:
				TheMovesScore[0] = Score
				TheMoves[0] = Move
			elif Score < TheMovesScore[1]:
				TheMovesScore[1] = Score
				TheMoves[1] = Move
			elif Score < TheMovesScore[2]:
				TheMovesScore[2] = Score
				TheMoves[2] = Move
		else:
			if TheMovesScore[0] == 0 and TheMoves[0] == "":
				TheMovesScore[0] = Score
				TheMoves[0] = Move
			elif TheMovesScore[1] == 0 and TheMoves[1] == "":
				TheMovesScore[1] = Score
				TheMoves[1] = Move
			elif TheMovesScore[2] == 0 and TheMoves[2] == "":
				TheMovesScore[2] = Score
				TheMoves[2] = Move
			if Score > TheMovesScore[0]:
				TheMovesScore[0] = Score
				TheMoves[0] = Move
			elif Score > TheMovesScore[1]:
				TheMovesScore[1] = Score
				TheMoves[1] = Move
			elif Score > TheMovesScore[2]:
				TheMovesScore[2] = Score
				TheMoves[2] = Move
	return TheMoves, TheMovesScore

def DisplayMoves(Move):
	ToDisplay = []
	NumberLetterDict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
	NumberDict = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
	Ini = str(Move[0])
	Des = str(Move[1])
	Start = NumberLetterDict[int(Ini[1])]+NumberDict[int(Ini[0])]
	Finish = NumberLetterDict[int(Des[1])]+NumberDict[int(Des[0])]
	ToDisplay.append((Start,Finish))
	return ToDisplay

def MakeMove(Board, Move):
	BoardToMove = (
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
			BoardToMove[i][j] = Board[i][j]
	if len(str(Move[0])) < 2:
		Move[0] = "0"+Move[0]
	if len(str(Move[1])) < 2:
		Move[1] = "0"+Move[1]
	DoubleInt = Move[0]
	Destination = Move[1]
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

def DepthController(Depth, Board, Player):
	Depth -=1
	print(Depth)
	print(Player)
	if Depth < 0:
		return None
	Allmoves = GetAllmoves(Player, Board)
	Moves, MoveScore = BestMoves(Player, Allmoves, Board)
	print(Moves)
	print(MoveScore)
	if Player == 1:
		NewPlayer = 2
	else:
		NewPlayer = 1
	Index = 0
	Value = [0,0,0]
	for Move in Moves:
		NewBoard = MakeMove(Board, Move)
		Value[Index] = DepthController(Depth, NewBoard, NewPlayer)
		Index +=1
	if Value[0] == None:
		Scoreindex = 0
		ScoreValue = 0
		NewI = 0
		for Score in MoveScore:
			if Player == 1:
				if Score <= ScoreValue:
					Scoreindex = NewI
					ScoreValue = Score
			else:
				if Score >= ScoreValue:
					Scoreindex = NewI
					ScoreValue = Score
			NewI +=1
		ResultedMove = (Moves[Scoreindex],MoveScore[Scoreindex])
		return ResultedMove
	else:
		for i in range(3):
			MoveScore[i] = Value[i][1]
		Scoreindex = 0
		ScoreValue = 0
		NewI = 0
		for Score in MoveScore:
			if NewPlayer == 1:
				if Score <= ScoreValue:
					Scoreindex = NewI
					ScoreValue = Score
			else:
				if Score >= ScoreValue:
					Scoreindex = NewI
					ScoreValue = Score
			NewI +=1
		ResultedMove = (Moves[Scoreindex],MoveScore[Scoreindex])
		return ResultedMove







		
	
def AIControl():
	import ChessControllerAI002 as Chess
	LocalPlayer = 5
	time.sleep(0.5)
	LocalTime = 0
	Index = 0
	while True:
		time.sleep(0.1)
		Player = Chess.Players().GetPlayer()
		if LocalPlayer != Player:
			time.sleep(1)
			StartTime = time.time()
			LocalPlayer = Player
			Depth = 3
			InitialBoard = Chess.Board().BoardConfig
			Result = DepthController(Depth, InitialBoard, Player)
			SpentTime = time.time() - StartTime
			LocalTime = LocalTime + SpentTime
			ToDisplay = DisplayMoves(Result[0])
			for _ in range(20):
				print("")
			for Move in ToDisplay:
				print(Move)
			print(Result[1])
			print(LocalTime)
			Index += 1
			# if (Index % 50) == 0:
			# 	print(".")
			# if LocalTime > 1:
			# 	print(Index)
			LocalTime = 0
			# 	Index = 0



t1 = threading.Thread(target=AIControl)
t1.start()

app = Chess.App()
app.MainLoop()