import multiprocessing
import time
import wx
import os
import sys
import threading

import ChessControllerAI002 as Chess


def BoardEvaluationMod(Board):
	# Values
	ValuePawn = 100
	ValueKnight = 300
	ValueBishop = 400
	ValueRook = 500
	ValueQueen = 750
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
							ABSValue = ABSValue + 40
						elif I <= 5:
							ABSValue = ABSValue + 20
					if Piece[1] == "P":
						if J >= 2 and J <= 5 and I <= 5:
							ABSValue = ABSValue + 40
					Eval = Eval - ABSValue
				else:
					if Piece[1] != "K":
						if I >= 5:
							ABSValue = ABSValue + 40
						elif I >= 3:
							ABSValue = ABSValue + 20
					if Piece[1] == "P":
						if J >= 2 and J <= 5 and I >= 2:
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

def BestMoves(Allmoves, BoardToMove):
	TheMoves = ["","",""]
	TheMovesScore = [0,0,0]
	for Move in Allmoves:
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
		if Score > TheMovesScore[0]:
			TheMovesScore[0] = Score
			TheMoves[0] = Move
		elif Score > TheMovesScore[1]:
			TheMovesScore[1] = Score
			TheMoves[1] = Move
		elif Score > TheMovesScore[2]:
			TheMovesScore[2] = Score
			TheMoves[2] = Move
	return TheMoves

		
	
def AIControl():
	import ChessControllerAI002 as Chess
	time.sleep(2)
	LocalTime = 0
	Index = 0
	# while True:
	StartTime = time.time()
	Player = Chess.Players().GetPlayer()
	# if P1_Move == False:
	# BoardEval = BoardEvaluationMod(Chess.Board().BoardConfig)
	Allmoves = GetAllmoves(Player, Chess.Board().BoardConfig)
	Moves = BestMoves(Allmoves, Chess.Board().BoardConfig)
	SpentTime = time.time() - StartTime
	LocalTime = LocalTime + SpentTime
	print(LocalTime)
	print(Moves)
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