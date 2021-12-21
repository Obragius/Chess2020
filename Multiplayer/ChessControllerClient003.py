import threading
import time
import wx
import socket



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

def Chess():
	import ChessControllerClient135 as Chess
	app = Chess.App()
	app.MainLoop()
		
		
		

t1 = threading.Thread(target=Chess)
t1.start()

import ChessControllerClient135 as Chess
local_Send_Press = False
while True:
	time.sleep(0.1)
	if Chess.Send_Status_Press != "":
		send(Chess.Send_Status_Press)
		Chess.Send_Status_Press = ""
	
		
	