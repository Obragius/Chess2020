import threading
import time
import wx
import socket
import pickle

HEADER = 64
PORT = 1235
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '&USEROUT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# This will show us which player is player one, and which player is player two
P1_Status = False
P2_Status = False

# Keeping track of which player is allowed to make moves
P1_Move = True

FirstPart = ""

P1_Client = ""
P2_Client = ""

class Server():
	def handle_client(conn, addr):
		global P1_Status, P2_Status, P1_Move, FirstPart, P1_Client, P2_Client
		import ChessController135 as Chess
		print(f"New Connection: {addr} connected\n")
		if P1_Status == False:
			P1_Status = addr
			P1_Client = conn
		elif P2_Status == False:
			P2_Status = addr
			P2_Client = conn
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
				if P1_Move == True:
					if addr == P1_Status:
						if FirstPart == "":
							FirstPart = msg
						else:
							if msg == FirstPart:
								FirstPart = ""
							else:
								MoveToMake = FirstPart+' '+msg
								MakeAMove(MoveToMake)
								FirstPart = ""
								P1_Move = False
					else:
						print("Wrong Player")
				else:
					if addr == P2_Status:
						if FirstPart == "":
							FirstPart = msg
						else:
							if msg == FirstPart:
								FirstPart = ""
							else:
								MoveToMake = FirstPart+' '+msg
								MakeAMove(MoveToMake)
								FirstPart = ""
								P1_Move = True
					else:
						print("Wrong Player")

		print(f"User {addr} have disconected")
		conn.close()


	@staticmethod
	def start():
		server.listen()
		while True:
			conn, addr = server.accept()
			playert = threading.Thread(target=Server.handle_client, args=(conn,addr))
			playert.start()
			print(f"Users Conected: {threading.activeCount() - 3}")


def ChessFunc():
	import ChessController135 as Chess
	app = Chess.App()
	app.MainLoop()

def MakeAMove(Move):
	import ChessController135 as Chess
	Chess.OnlineMove = Move

def SendBoardToUser():
	import ChessController135 as Chess
	while True:
		time.sleep(2)
		if P1_Client != "":
			Something = Chess.Board().BoardConfig
			message = Something.encode(FORMAT)
			msg_length = len(message)
			send_length = str(msg_length).encode(FORMAT)
			send_length += b' ' * (HEADER- len(send_length))
			P1_Client.send()
			P1_Client.send()
		
		
		

t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=Server().start)
t3 = threading.Thread(target=SendBoardToUser)
print(SERVER)
print("Initilising Server...")
# Server().start()


t2.start()
t1.start()
t3.start()
