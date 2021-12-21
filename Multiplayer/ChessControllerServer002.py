import threading
import time
import wx
import socket

HEADER = 64
PORT = 1238
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '&USEROUT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# This will show us which player is player one, and which player is player two
P1_Status = False:
P2_Status = False:

class Server():
	def handle_client(conn, addr):
		global P1_Status, P2_Status
		print(f"New Connection: {addr} connected\n")
		if P1_Status == False:
			P1_Status = addr
		if P2_Status == False:
			P2_Status = addr
		connected = True
		while connected:
			msg_len = conn.recv(HEADER).decode(FORMAT)
			# If message_len is not none
			if msg_len:
				msg_len = int(msg_len)
				msg = conn.recv(msg_len).decode(FORMAT)
				if msg == DISCONNECT_MESSAGE:
					connected = False
				print(f"({addr}) : {msg}")

		print(f"User {addr} have disconected")
		conn.close()


	@staticmethod
	def start():
		server.listen()
		while True:
			conn, addr = server.accept()
			playert = threading.Thread(target=Server.handle_client, args=(conn,addr))
			playert.start()
			print(f"Users Conected: {threading.activeCount() - 1}")


def Chess():
	import ChessController135 as Chess
	app = Chess.App()
	app.MainLoop()

def Prompt():
	import ChessController135 as Chess
	while True:
		move = input("Do a Move\n")
		Chess.OnlineMove = move
		
		
		

t1 = threading.Thread(target=Chess)
t2 = threading.Thread(target=Server().start)
print(SERVER)
print("Initilising Server...")
# Server().start()


t2.start()
t1.start()
