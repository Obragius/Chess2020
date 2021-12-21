import threading
import time
import wx
import socket



HEADER = 64
PORT = 1231
# SERVER = input("Input IP")
# ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '&USEROUT'


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

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


while True:
	input()
	import ChessControllerClient135 as Chess
	print(Chess.Send_Status_Press)