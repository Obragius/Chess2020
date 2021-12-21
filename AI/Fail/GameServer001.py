import multiprocessing
import time
import wx
import os
import sys
import threading

import ChessControllerAI001 as Chess

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
			if Piece[0] == "W":
				Eval = Eval - ABSValue
			else:
				Eval = Eval + ABSValue
	return Eval


def AIControl():
	import ChessControllerAI001 as Chess
	time.sleep(1)
	LocalTime = 0
	Index = 0
	while True:
		StartTime = time.time()
		Player = Chess.Players().GetPlayer()
		if Player == 1:
			P1_Move = True
		else:
			P1_Move = False
		# if P1_Move == False:
		BoardEval = BoardEvaluationMod(Chess.Board().BoardConfig)
		SpentTime = time.time() - StartTime
		LocalTime = LocalTime + SpentTime
		Index += 1
		if (Index % 100) == 0:
			print("waiting")
		if LocalTime > 1:
			print(Index)
			LocalTime = 0
			Index = 0



t1 = threading.Thread(target=AIControl)
t1.start()

app = Chess.App()
app.MainLoop()