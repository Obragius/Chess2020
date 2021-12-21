import threading
import time
import wx
import socket
import pickle
import os
import tkinter as tk



root = tk.Tk()
root.title("Starting Server")
root.iconbitmap("Images/White_Pawn_Grey_Icon.ico")

filename = tk.PhotoImage(file = "Images/Background.png")
background_label = tk.Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

FirstInput = tk.Entry(root, width=20)
FirstInput.place(relx=0.34, rely=0.05)
Server = socket.gethostbyname(socket.gethostname())
FirstInput.insert(0, Server)

SecondInput = tk.Entry(root, width=20)
SecondInput.place(relx=0.34, rely=0.15)
Port = "5500"
SecondInput.insert(0, Port)

def OnKeyPress(event):
	if str(event.keysym) == "Return":
		OnClick()

def OnClick():
	global PORT, SERVER
	SERVER = FirstInput.get()
	PORT = int(SecondInput.get())
	root.destroy()

Button = tk.Button(root, text="Start Server", command=OnClick)
Button.place(relx=0.41, rely=0.3)

root.bind('<KeyPress>', OnKeyPress)

root.mainloop()
time.sleep(0.5)


# SERVER = Server
# PORT = int(Port)
HEADER = 64
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

class Server():
	def handle_client(conn, addr):
		global P1_Status, P2_Status, P1_Move, FirstPart, P1_Client, P2_Client, LocalChessStore
		import ChessController139 as Chess
		print(f"New Connection: {addr} connected\n")
		if P1_Status == False:
			P1_Status = addr
			P1_Client = conn
		elif P2_Status == False:
			P2_Status = addr
			P2_Client = conn
		connected = True
		while connected:
			try:
				msg_len = conn.recv(HEADER).decode(FORMAT)
			except:
				if P1_Status == addr:
					P1_Status = False
					P1_Client = ""
				elif P2_Status == addr:
					P2_Status = False
					P2_Client = ""
				connected = False
				break
			# If message_len is not none
			if msg_len:
				Player = Chess.Players().GetPlayer()
				if Player == 1:
					P1_Move = True
				else:
					P1_Move = False
				msg_len = int(msg_len)
				msg = conn.recv(msg_len).decode(FORMAT)
				msg_len2 = conn.recv(HEADER).decode(FORMAT)
				msg_len2 = int(msg_len2)
				msg2 = conn.recv(msg_len2).decode(FORMAT)
				if msg2 == "True":
					if addr == P1_Status:
						Chess.GaveUpWhite = True
						Chess.CurrentStatusMsg = "White Gave Up"
					elif addr == P2_Status:
						Chess.GaveUpBlack = True
						Chess.CurrentStatusMsg = "Black Gave Up"
				if msg == DISCONNECT_MESSAGE:
					connected = False
				if msg != "":
					print(f"({addr}) : {msg}")
					if len(msg) == 3:
						MoveToMake = msg
						MakeAMove(MoveToMake)
					elif P1_Move == True: 
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
			print(f"Users Conected: {threading.activeCount() - 5}")


def ChessFunc():
	import ChessController139 as Chess
	app = Chess.App()
	app.MainLoop()

def MakeAMove(Move):
	import ChessController139 as Chess
	Chess.OnlineMove = Move

def SendBoardToUserP1():
	import ChessController139 as Chess
	while True:
		try:
			time.sleep(0.025)
			Player = Chess.Players().GetPlayer()
			if Player == 1:
				P1_Move = True
			else:
				P1_Move = False
			if P1_Client != "":
				message = pickle.dumps(Chess.Board().BoardConfig)
				msg_length = len(message)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				P1_Client.send(send_length)
				P1_Client.send(message)
				if P1_Move == True:
					message2 = pickle.dumps(Chess.GreenBoardToSend)
					msg_length = len(message2)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message2)
					message3 = b'True'
					msg_length = len(message3)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message3)
					message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
					msg_length = len(message4)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message4)
					message5 = pickle.dumps(Chess.MessageList)
					msg_length = len(message5)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message5)
					message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
					msg_length = len(message6)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message6)
					if Chess.GaveUpWhite == True:
						GaveUpBool = "You"
					elif Chess.GaveUpBlack == True:
						GaveUpBool = "Other"
					else:
						GaveUpBool = "False"
					msg7 = GaveUpBool.encode(FORMAT)
					msg_length = len(msg7)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg7)
					if Chess.UpdateTimeD == True:
						SendUpdate = "True"
					else:
						SendUpdate = "False"
					msg8 = SendUpdate.encode(FORMAT)
					msg_length = len(msg8)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg8)
					if Chess.PawnWhiteClient == True:
						SendPawn = "WhiteTrue"
					else:
						SendPawn = "False"
					msg9 = SendPawn.encode(FORMAT)
					msg_length = len(msg9)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg9)
				else:
					message2 = pickle.dumps(Chess.EmptyBoard)
					msg_length = len(message2)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message2)
					message3 = b'False'
					msg_length = len(message3)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message3)
					message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
					msg_length = len(message4)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message4)
					message5 = pickle.dumps(Chess.MessageList)
					msg_length = len(message5)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message5)
					message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
					msg_length = len(message6)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(message6)
					if Chess.GaveUpWhite == True:
						GaveUpBool = "You"
					elif Chess.GaveUpBlack == True:
						GaveUpBool = "Other"
					else:
						GaveUpBool = "False"
					msg7 = GaveUpBool.encode(FORMAT)
					msg_length = len(msg7)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg7)
					if Chess.UpdateTimeD == True:
						SendUpdate = "True"
					else:
						SendUpdate = "False"
					msg8 = SendUpdate.encode(FORMAT)
					msg_length = len(msg8)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg8)
					if Chess.PawnWhiteClient == True:
						SendPawn = "WhiteTrue"
					else:
						SendPawn = "False"
					msg9 = SendPawn.encode(FORMAT)
					msg_length = len(msg9)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P1_Client.send(send_length)
					P1_Client.send(msg9)
		except:
			pass
		
def SendBoardToUserP2():
	import ChessController139 as Chess
	while True:
		try:
			time.sleep(0.025)
			Player = Chess.Players().GetPlayer()
			if Player == 1:
				P1_Move = True
			else:
				P1_Move = False
			if P2_Client != "":
				message = pickle.dumps(Chess.Board().BoardConfig)
				msg_length = len(message)
				send_length = str(msg_length).encode(FORMAT)
				send_length += b' ' * (HEADER- len(send_length))
				P2_Client.send(send_length)
				P2_Client.send(message)
				if P1_Move != True:
					message2 = pickle.dumps(Chess.GreenBoardToSend)
					msg_length = len(message2)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message2)
					message3 = b'True'
					msg_length = len(message3)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message3)
					message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
					msg_length = len(message4)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message4)
					message5 = pickle.dumps(Chess.MessageList)
					msg_length = len(message5)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message5)
					message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
					msg_length = len(message6)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message6)
					if Chess.GaveUpBlack == True:
						GaveUpBool = "You"
					elif Chess.GaveUpWhite == True:
						GaveUpBool = "Other"
					else:
						GaveUpBool = "False"
					msg7 = GaveUpBool.encode(FORMAT)
					msg_length = len(msg7)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg7)
					if Chess.UpdateTimeD == True:
						SendUpdate = "True"
					else:
						SendUpdate = "False"
					msg8 = SendUpdate.encode(FORMAT)
					msg_length = len(msg8)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg8)
					if Chess.PawnBlackClient == True:
						SendPawn = "BlackTrue"
					else:
						SendPawn = "False"
					msg9 = SendPawn.encode(FORMAT)
					msg_length = len(msg9)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg9)
				else:
					message2 = pickle.dumps(Chess.EmptyBoard)
					msg_length = len(message2)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message2)
					message3 = b'False'
					msg_length = len(message3)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message3)
					message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
					msg_length = len(message4)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message4)
					message5 = pickle.dumps(Chess.MessageList)
					msg_length = len(message5)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message5)
					message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
					msg_length = len(message6)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(message6)
					if Chess.GaveUpBlack == True:
						GaveUpBool = "You"
					elif Chess.GaveUpWhite == True:
						GaveUpBool = "Other"
					else:
						GaveUpBool = "False"
					msg7 = GaveUpBool.encode(FORMAT)
					msg_length = len(msg7)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg7)
					if Chess.UpdateTimeD == True:
						SendUpdate = "True"
					else:
						SendUpdate = "False"
					msg8 = SendUpdate.encode(FORMAT)
					msg_length = len(msg8)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg8)
					if Chess.PawnBlackClient == True:
						SendPawn = "BlackTrue"
					else:
						SendPawn = "False"
					msg9 = SendPawn.encode(FORMAT)
					msg_length = len(msg9)
					send_length = str(msg_length).encode(FORMAT)
					send_length += b' ' * (HEADER- len(send_length))
					P2_Client.send(send_length)
					P2_Client.send(msg9)
		except:
			pass
		
		

# t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=Server().start)
t3 = threading.Thread(target=SendBoardToUserP1)
t4 = threading.Thread(target=SendBoardToUserP2)

t2.start()
# t1.start()
t3.start()
t4.start()


print(f"{SERVER}:{PORT}")
print("Initilising Server...")
ChessFunc()

