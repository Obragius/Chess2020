import threading
import time
import wx
import socket
import pickle



HEADER = 64
SERVER = input("Input IP: ")
PORT = int(input("Input Port: "))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '&USEROUT'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	import ChessControllerClient139 as Chess
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER- len(send_length))
	client.send(send_length)
	client.send(message)
	Structure = Chess.GiveUP
	Give = Structure.encode(FORMAT)
	msg_length2 = len(Give)
	send_length2 = str(msg_length2).encode(FORMAT)
	send_length2 += b' ' * (HEADER- len(send_length2))
	client.send(send_length2)
	client.send(Give)

def ChessFunc():
	import ChessControllerClient139 as Chess
	app = Chess.App()
	app.MainLoop()

def ListenForBoard():
	import ChessControllerClient139 as Chess
	while True:
		time.sleep(0.01)
		msg_len1 = client.recv(HEADER).decode(FORMAT)
		# If message_len is not none
		if msg_len1:
			msg_len1 = int(msg_len1)
			msg = client.recv(msg_len1)
			SentBoard = pickle.loads(msg)
			if SentBoard != Chess.Board().BoardConfig:
				for i in range(8):
					for j in range(8):
						Chess.Board().BoardConfig[i][j] = SentBoard[i][j]
				Chess.UpdateTime = True
			msg_len2 = client.recv(HEADER).decode(FORMAT)
			msg_len2 = int(msg_len2)
			msg2 = client.recv(msg_len2)
			SentBoard2 = pickle.loads(msg2)
			if SentBoard2 != Chess.LastGreenSpaceDisplay:
				for i in range(8):
					for j in range(8):
						Chess.LastGreenSpaceDisplay[i][j] = SentBoard2[i][j]
				Chess.UpdateTimeD = True
			msg_len3 = client.recv(HEADER).decode(FORMAT)
			msg_len3 = int(msg_len3)
			msg3 = client.recv(msg_len3)
			Chess.YourTurn = msg3
			msg_len4 = client.recv(HEADER).decode(FORMAT)
			msg_len4 = int(msg_len4)
			msg4 = client.recv(msg_len4)
			Chess.Board().BoardLogLastMove[1] = msg4.decode(FORMAT)
			msg_len5 = client.recv(HEADER).decode(FORMAT)
			msg_len5 = int(msg_len5)
			msg5 = client.recv(msg_len5)
			SentMessageList = pickle.loads(msg5)
			if SentMessageList != Chess.MessageList:
				Chess.MessageList = []
				for Value in SentMessageList:
					Chess.MessageList.append(Value)
			msg_len6 = client.recv(HEADER).decode(FORMAT)
			msg_len6 = int(msg_len6)
			msg6 = client.recv(msg_len6)
			Chess.CurrentStatusMsg = msg6.decode(FORMAT)
			msg_len7 = client.recv(HEADER).decode(FORMAT)
			msg_len7 = int(msg_len7)
			GiveUPBool = client.recv(msg_len7).decode(FORMAT)
			Chess.GiveUPDis = GiveUPBool
			msg_len8 = client.recv(HEADER).decode(FORMAT)
			msg_len8 = int(msg_len8)
			UpdateFromRestart = client.recv(msg_len8).decode(FORMAT)
			if UpdateFromRestart == "True":
				Chess.UpdateTimeD = True
			msg_len9 = client.recv(HEADER).decode(FORMAT)
			msg_len9 = int(msg_len9)
			PawnMessage = client.recv(msg_len9).decode(FORMAT)
			if PawnMessage == "WhiteTrue":
				Chess.WhitePawnDis = True
				Chess.PawnDelete = False
			elif PawnMessage == "BlackTrue":
				Chess.BlackPawnDis = True
				Chess.PawnDelete = False
			else:
				Chess.WhitePawnDis = False
				Chess.BlackPawnDis = False
				Chess.PawnDelete = True

		
		
		

t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=ListenForBoard)
t1.start()
t2.start()

import ChessControllerClient139 as Chess
local_Send_Press = False
while True:
	time.sleep(0.015)
	send(Chess.Send_Status_Press)
	Chess.Send_Status_Press = ""
	Chess.GiveUP = "False"
	
		
	