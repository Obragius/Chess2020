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
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER- len(send_length))
	client.send(send_length)
	client.send(message)

def ChessFunc():
	import ChessControllerClient138 as Chess
	app = Chess.App()
	app.MainLoop()

def ListenForBoard():
	import ChessControllerClient138 as Chess
	while True:
		time.sleep(0.08)
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

		
		
		

t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=ListenForBoard)
t1.start()
t2.start()

import ChessControllerClient138 as Chess
local_Send_Press = False
while True:
	time.sleep(0.1)
	if Chess.Send_Status_Press != "":
		send(Chess.Send_Status_Press)
		Chess.Send_Status_Press = ""
	
		
	