import threading
import time
import wx
import socket
import pickle
import multiprocessing

class Server():
	def handle_client(conn, addr):
		global P1_Status, P2_Status, P1_Move, FirstPart, P1_Client, P2_Client, LocalChessStore
		import ChessController137 as Chess
		print(f"New Connection: {addr} connected\n")
		if P1_Status == False:
			P1_Status = addr
			P1_Client = conn
			from ChessControllerServer016 import SendBoardToUser
			p1 = multiprocessing.Process(target=SendBoardToUser, args=[P1_Client,'utf-8',64])
			p1.start()
		elif P2_Status == False:
			P2_Status = addr
			P2_Client = conn
			from ChessControllerServer016 import SendBoardToUser
			p2 = multiprocessing.Process(target=SendBoardToUser, args=[P2_Client,'utf-8',64])
			p2.start()
		connected = True
		while connected:
			msg_len = conn.recv(HEADER).decode(FORMAT)
			# If message_len is not none
			if msg_len:
				Player = Chess.Players().GetPlayer()
				if Player == 1:
					P1_Move = True
				else:
					P1_Move = False
				msg_len = int(msg_len)
				msg = conn.recv(msg_len).decode(FORMAT)
				if msg == DISCONNECT_MESSAGE:
					connected = False
				print(f"({addr}) : {msg}")
				if P1_Move == True:
					if addr == P1_Status:
						MoveToMake = msg
						MakeAMove(MoveToMake)
						for i in range(8):
							for j in range(8):
								LocalChessStore[i][j] = Chess.Board().BoardConfig[i][j]
					else:
						print("Wrong Player")

				else:
					if addr == P2_Status:
						MoveToMake = msg
						MakeAMove(MoveToMake)
						for i in range(8):
							for j in range(8):
								LocalChessStore[i][j] = Chess.Board().BoardConfig[i][j]
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
	import ChessController137 as Chess
	app = Chess.App()
	app.MainLoop()

def MakeAMove(Move):
	import ChessController137 as Chess
	Chess.OnlineMove = Move


def SendBoardToUser(Client, FORMAT, HEADER):
	import ChessController137 as Chess
	while True:
		time.sleep(0.05)
		Player = Chess.Players().GetPlayer()
		if Player == 1:
			P1_Move = True
		else:
			P1_Move = False
		if Client != "":
			message = pickle.dumps(Chess.Board().BoardConfig)
			msg_length = len(message)
			send_length = str(msg_length).encode(FORMAT)
			send_length += b' ' * (HEADER- len(send_length))
			Client.send(send_length)
			Client.send(message)
			if P1_Move == True:
				message2 = pickle.dumps(Chess.GreenBoardToSend)
				msg_length = len(message2)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message2)
				message3 = b'True'
				msg_length = len(message3)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message3)
				message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
				msg_length = len(message4)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message4)
				message5 = pickle.dumps(Chess.MessageList)
				msg_length = len(message5)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message5)
				message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
				msg_length = len(message6)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message6)
			else:
				message2 = pickle.dumps(Chess.EmptyBoard)
				msg_length = len(message2)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message2)
				message3 = b'False'
				msg_length = len(message3)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message3)
				message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
				msg_length = len(message4)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message4)
				message5 = pickle.dumps(Chess.MessageList)
				msg_length = len(message5)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message5)
				message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
				msg_length = len(message6)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				Client.send(send_length)
				Client.send(message6)
		



if __name__ == "__main__":

	HEADER = 64
	response = input("Input your ip or leave blank for default\n")
	if response == "":
		SERVER = socket.gethostbyname(socket.gethostname())
	else:
		SERVER = response
	PORT = int(input("Input the Port\n"))
	ADDR = (SERVER, PORT)
	FORMAT = 'utf-8'
	DISCONNECT_MESSAGE = '&USEROUT'

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)

	# This will show us which player is player one, and which player is player two
	P1_Status = False
	P2_Status = False

	# Keeping track of which player is allowed to make moves
	P1_Move = False

	P1_Client = ""
	P2_Client = ""


	LocalChessStore = (
						[['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',],
				        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',]])

	t1 = threading.Thread(target=ChessFunc)
	t2 = threading.Thread(target=Server().start)

	
	t1.start()
	t2.start()
	print(f"{SERVER}:{PORT}")
	print("Initilising Server...")
