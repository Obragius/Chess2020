import multiprocessing
import time
import wx
import os
import sys
import threading

import ChessControllerAI002 as Chess






		
	
def AIControl():
	import ChessControllerAI002 as Chess
	LocalPlayer = 5
	time.sleep(0.5)
	Movestodis = ['F2:F4', 'F7:F5', 'D2:D4', 'D7:D5', 'E2:E3', 'H7:H5', 'F1:B5', 'B8:C6', 'C2:C3', 'E8:F7', 'B5:C6', 'B7:C6', 'G1:F3', 'D8:D6', 'H2:H4', 'E7:E6', 'G2:G4', 'H5:G4', 'F3:G5', 'F7:G6', 'B2:B4', 'G4:G3', 'A2:A4', 'A7:A5', 'B4:B5', 'C6:B5', 'A4:B5', 'C7:C5', 'E1:D2', 'C5:C4', 'H4:H5', 'H8:H5', 'H1:H5', 'A5:A4', 'G5:E6', 'C8:E6', 'H5:G5', 'G6:H6', 'D1:H5']
	for Move in Movestodis:
		time.sleep(1)
		Chess.OnlineMove = Move[0]+Move[1]
		time.sleep(1)
		Chess.OnlineMove = Move[3]+Move[4]



t1 = threading.Thread(target=AIControl)
t1.start()

app = Chess.App()
app.MainLoop()