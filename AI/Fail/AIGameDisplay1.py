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
	TheMoves = []
	TheMovesScore = []
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
		TheMoves.append(Move)
		TheMovesScore.append(Score)
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
	if Depth < 0:
		return None
	Allmoves = GetAllmoves(Player, Board)
	Moves, MoveScore = BestMoves(Player, Allmoves, Board)
	if Player == 1:
		NewPlayer = 2
	else:
		NewPlayer = 1
	Index = 0
	Value = []
	for Move in Moves:
		NewBoard = MakeMove(Board, Move)
		ValueL = DepthController(Depth, NewBoard, NewPlayer)
		Value.append(ValueL)
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
		print(MoveScore[Scoreindex])
		return ResultedMove
	else:
		for i in range(len(Value)):
			MoveScore[i] = Value[i][1]
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
		print(MoveScore[Scoreindex])
		return ResultedMove







		
	
def AIControl():
	import ChessControllerAI002 as Chess
	LocalPlayer = 5
	time.sleep(0.5)
	Movestodis = ['E2:E4','E7:E5','F1:B5','G8:F6','D2:D4','E5:D4','D1:D4','C7:C5','D4:E5','D8:E7','E5:E7','E8:E7','F2:F3','D7:D6','C2:C4','H7:H5','C1:G5','C8:E6','H2:H4','A7:A5','G2:G4','H5:G4','F3:G4','E6:G4','B2:B4','A5:B4','A2:A4','H8:H4','H1:H4','G4:D1','E1:D1','A8:A7','G5:F6','E7:F6','H4:H8','B8:C6','H8:F8','A7:A8','F8:A8','B7:B6','E4:E5','C6:E5','G1:F3','G7:G6','F3:E5','D6:D5','C4:D5','F6:G5','E5:F7','G5:H4','B5:E8','B6:B5','A4:B5','G6:G5','B1:D2','C5:C4','F7:G5','B4:B3','D2:C4','H4:G3','A1:A7']
	for Move in Movestodis:
		time.sleep(1)
		Chess.OnlineMove = Move[0]+Move[1]
		time.sleep(1)
		Chess.OnlineMove = Move[3]+Move[4]



t1 = threading.Thread(target=AIControl)
t1.start()

app = Chess.App()
app.MainLoop()