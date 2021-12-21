import threading
import time
import wx
import socket

PORT = 5550
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class Server:
	def handle_client(conn, addr):
		pass

	def start():
		server.listen()
		while True:
			conn, addr = server.accept()
			playert = threading.Thread(target=Server.handle_client, args=(conn,addr))
			print(f"Users Conected: {threading.activeCount() - 2}")


def Chess():
	import ChessController135 as Chess
	app = Chess.App()
	app.MainLoop()

def Prompt():
	import ChessController135 as Chess
	while True:
		move = input("Do a Move\n")
		Chess.Sumashi = move
		
		
		

t1 = threading.Thread(target=Chess)
t2 = threading.Thread(target=Prompt)
print("Initilising Server...")

t2.start()
t1.start()
