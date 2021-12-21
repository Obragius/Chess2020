import threading
import time
import wx
import socket
import pickle



HEADER = 64
PORT = 1235
SERVER = input("Input IP\n")
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
	import ChessControllerClient135 as Chess
	app = Chess.App()
	app.MainLoop()

def ListenForBoard():
	import ChessControllerClient135 as Chess
	while True:
		time.sleep(0.1)
		msg_len = client.recv(HEADER).decode(FORMAT)
		# If message_len is not none
		if msg_len:
			msg_len = int(msg_len)
			msg = client.recv(msg_len)
			SentBoard = pickle.loads(msg)
			if SentBoard != Chess.Board().BoardConfig:
				for i in range(8):
					for j in range(8):
						Chess.Board().BoardConfig[i][j] = SentBoard[i][j]
				Chess.UpdateTime = True

		
		
		

t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=ListenForBoard)
t1.start()
t2.start()

import ChessControllerClient135 as Chess
local_Send_Press = False
while True:
	time.sleep(0.1)
	if Chess.Send_Status_Press != "":
		send(Chess.Send_Status_Press)
		Chess.Send_Status_Press = ""
	
		
	