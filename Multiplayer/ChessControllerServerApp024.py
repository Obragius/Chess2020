import threading
import time
import wx
import socket
import pickle
import os
import tkinter as tk
import logging
import sys



START = False
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
	global PORT, SERVER, START
	SERVER = FirstInput.get()
	PORT = int(SecondInput.get())
	START = True
	root.destroy()

Button = tk.Button(root, text="Start Server", command=OnClick)
Button.place(relx=0.41, rely=0.3)

root.bind('<KeyPress>', OnKeyPress)

root.mainloop()
time.sleep(0.5)
if START:

	# SERVER = Server
	# PORT = int(Port)
	HEADER = 64
	ADDR = (SERVER, PORT)
	FORMAT = 'utf-8'
	DISCONNECT_MESSAGE = '&USEROUT'
	DETECTION = "&DETECTION"
	CONFIRMATION = "&RECEIVED"

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
			import ChessController141 as Chess
			print(f"New Connection: {addr} connected\n")
			Listtosend = pickle.dumps(Chess.MessageList)
			msg_l = len(Listtosend)
			send_l = str(msg_l).encode(FORMAT)
			send_l += b' ' * (HEADER- len(send_l))
			conn.send(send_l)
			conn.send(Listtosend)
			if P1_Status == False:
				P1_Status = addr
				P1_Client = conn
				Chess.User1 = P1_Status[0]
			elif P2_Status == False:
				P2_Status = addr
				P2_Client = conn
				Chess.User2 = P2_Status[0]
			connected = True
			while connected:
				try:
					msg_len = conn.recv(HEADER).decode(FORMAT)
				except:
					if P1_Status == addr:
						P1_Status = False
						P1_Client = ""
						Chess.User1 = ""
					elif P2_Status == addr:
						P2_Status = False
						P2_Client = ""
						Chess.User2 = ""
					connected = False
					break
				# If message_len is not none
				if msg_len:
					ConfirmLetter = ["A","B","C","D","E","F","G","H"]
					Player = Chess.Players().GetPlayer()
					if Player == 1:
						P1_Move = True
					else:
						P1_Move = False
					try:
						msg_len = int(msg_len)
						msg = conn.recv(msg_len).decode(FORMAT)
						msg_len2 = conn.recv(HEADER).decode(FORMAT)
						msg_len2 = int(msg_len2)
						msg2 = conn.recv(msg_len2).decode(FORMAT)
						msg_len3 = conn.recv(HEADER).decode(FORMAT)
						msg_len3 = int(msg_len3)
						msg3 = conn.recv(msg_len3).decode(FORMAT)
						if msg == "" or msg2 == "" or msg3 == "":
							raise 
					except:
						if P1_Status == addr:
							P1_Status = False
							P1_Client = ""
							Chess.User1 = ""
						elif P2_Status == addr:
							P2_Status = False
							P2_Client = ""
							Chess.User2 = ""
						connected = False
						break
					for Letter in ConfirmLetter:
						if msg[0] == Letter:
							MoveToMake = msg
						if msg2[0] == Letter:
							MoveToMake = msg2
						if msg3[0] == Letter:
							MoveToMake = msg3
					if msg2 == "True" or msg == "True" or msg3 == "True":
						if addr == P1_Status:
							Chess.GaveUpWhite = True
							Chess.CurrentStatusMsg = "White Gave Up"
						elif addr == P2_Status:
							Chess.GaveUpBlack = True
							Chess.CurrentStatusMsg = "Black Gave Up"
					if msg3 == CONFIRMATION or msg == CONFIRMATION or msg2 == CONFIRMATION:
						if addr == P1_Status:
							Chess.User1Recieve = True
						elif addr == P2_Status:
							Chess.User2Recieve = True
					if msg == DISCONNECT_MESSAGE or msg2 == DISCONNECT_MESSAGE or msg3 == DISCONNECT_MESSAGE:
						connected = False
					if msg != "1111" and msg2 != "1111" and msg3 != "1111":
						print(f"({addr}) : ms1 : {msg}, msg2: {msg2}, msg3: {msg3}")
						if len(msg) == 3:
							MoveToMake = msg
							MakeAMove(MoveToMake)
						elif len(msg2) == 3:
							MoveToMake = msg2
							MakeAMove(MoveToMake)
						elif len(msg3) == 3:
							MoveToMake = msg3
							MakeAMove(MoveToMake)
						elif P1_Move == True: 
							if addr == P1_Status:
								try:
									MakeAMove(MoveToMake)
								except:
									pass
								for i in range(8):
									for j in range(8):
										LocalChessStore[i][j] = Chess.Board().BoardConfig[i][j]
							else:
								print("Wrong Player")

						else:
							if addr == P2_Status:
								try:
									MakeAMove(MoveToMake)
								except:
									pass
								for i in range(8):
									for j in range(8):
										LocalChessStore[i][j] = Chess.Board().BoardConfig[i][j]
							else:
								print("Wrong Player")


			if addr == P1_Status:
				P1_Status = False
				Chess.User1 = ""
				P1_Client = ""
				Chess.User1Recieve = False
			elif addr == P2_Status:
				P2_Status = False
				Chess.User2 = ""
				P2_Client = ""
				Chess.User2Recieve = False
			print(f"User {addr} have disconected")
			conn.close()


		@staticmethod
		def start():
			import ChessController141 as Chess
			server.listen()
			while Chess.ServerRun:
				conn, addr = server.accept()
				playert = threading.Thread(target=Server.handle_client, args=(conn,addr))
				playert.start()
				print(f"Users Conected: {threading.activeCount() - 4}")
			else:
				sys.exit(1)


	def ChessFunc():
		import ChessController141 as Chess
		app = Chess.App()
		app.MainLoop()

	def MakeAMove(Move):
		import ChessController141 as Chess
		Chess.OnlineMove = Move

	def SendBoardToUserP1():
		import ChessController141 as Chess
		while Chess.ServerRun:
			try:
				time.sleep(0.1)
				Player = Chess.Players().GetPlayer()
				if Player == 1:
					P1_Move = True
				else:
					P1_Move = False
				if P1_Client != "":
					if Chess.User1Recieve == True:
						DettectionSend = DETECTION.encode(FORMAT)
						message = pickle.dumps(Chess.Board().BoardConfig)
						msg_length1 = len(message)
						send_length1 = str(msg_length1).encode(FORMAT)
						send_length1 += b' ' * (HEADER- len(send_length1))
						if P1_Move == True:
							message3 = b'True'
							message2 = pickle.dumps(Chess.GreenBoardToSend)
						else:
							message3 = b'False'
							message2 = pickle.dumps(Chess.EmptyBoard)
							# --------------------------------------------
						msg_length2 = len(message2)
						send_length2 = str(msg_length2).encode(FORMAT)
						send_length2 += b' ' * (HEADER- len(send_length2))
						msg_length3 = len(message3)
						send_length3 = str(msg_length3).encode(FORMAT)
						send_length3 += b' ' * (HEADER- len(send_length3))
						message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
						msg_length4 = len(message4)
						send_length4 = str(msg_length4).encode(FORMAT)
						send_length4 += b' ' * (HEADER- len(send_length4))
						message5 = bytes(Chess.MessageListLast,FORMAT)
						msg_length5 = len(message5)
						send_length5 = str(msg_length5).encode(FORMAT)
						send_length5 += b' ' * (HEADER- len(send_length5))
						message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
						msg_length6 = len(message6)
						send_length6 = str(msg_length6).encode(FORMAT)
						send_length6 += b' ' * (HEADER- len(send_length6))
						if Chess.GaveUpWhite == True:
							GaveUpBool = "You"
						elif Chess.GaveUpBlack == True:
							GaveUpBool = "Other"
						else:
							GaveUpBool = "False"
						msg7 = GaveUpBool.encode(FORMAT)
						msg_length7 = len(msg7)
						send_length7 = str(msg_length7).encode(FORMAT)
						send_length7 += b' ' * (HEADER- len(send_length7))
						if Chess.UpdateTimeD == True:
							SendUpdate = "True"
						else:
							SendUpdate = "False"
						msg8 = SendUpdate.encode(FORMAT)
						msg_length8 = len(msg8)
						send_length8 = str(msg_length8).encode(FORMAT)
						send_length8 += b' ' * (HEADER- len(send_length8))
						if Chess.PawnWhiteClient == True:
							SendPawn = "WhiteTrue"
						else:
							SendPawn = "False"
						msg9 = SendPawn.encode(FORMAT)
						msg_length9 = len(msg9)
						send_length9 = str(msg_length9).encode(FORMAT)
						send_length9 += b' ' * (HEADER- len(send_length9))
						P1_Client.send(DettectionSend)
						P1_Client.send(send_length1)
						P1_Client.send(message)
						P1_Client.send(send_length2)
						P1_Client.send(message2)
						P1_Client.send(send_length3)
						P1_Client.send(message3)
						P1_Client.send(send_length4)
						P1_Client.send(message4)
						P1_Client.send(send_length5)
						P1_Client.send(message5)
						P1_Client.send(send_length6)
						P1_Client.send(message6)
						P1_Client.send(send_length7)
						P1_Client.send(msg7)
						P1_Client.send(send_length8)
						P1_Client.send(msg8)
						P1_Client.send(send_length9)
						P1_Client.send(msg9)
						Chess.User1Recieve = False
			except:
				pass
		else:
			sys.exit(1)

			
	def SendBoardToUserP2():
		import ChessController141 as Chess
		while Chess.ServerRun:
			try:
				time.sleep(0.1)
				Player = Chess.Players().GetPlayer()
				if Player == 1:
					P1_Move = True
				else:
					P1_Move = False
				if P2_Client != "":
					if Chess.User2Recieve == True:
						DettectionSend = DETECTION.encode(FORMAT)
						message = pickle.dumps(Chess.Board().BoardConfig)
						msg_length1 = len(message)
						send_length1 = str(msg_length1).encode(FORMAT)
						send_length1 += b' ' * (HEADER- len(send_length1))
						if P1_Move != True:
							message3 = b'True'
							message2 = pickle.dumps(Chess.GreenBoardToSend)
						else:
							message3 = b'False'
							message2 = pickle.dumps(Chess.EmptyBoard)
							# --------------------------------------------
						msg_length2 = len(message2)
						send_length2 = str(msg_length2).encode(FORMAT)
						send_length2 += b' ' * (HEADER- len(send_length2))
						msg_length3 = len(message3)
						send_length3 = str(msg_length3).encode(FORMAT)
						send_length3 += b' ' * (HEADER- len(send_length3))
						message4 = bytes(str(Chess.Board().BoardLogLastMove[1]),FORMAT)
						msg_length4 = len(message4)
						send_length4 = str(msg_length4).encode(FORMAT)
						send_length4 += b' ' * (HEADER- len(send_length4))
						message5 = bytes(Chess.MessageListLast,FORMAT)
						msg_length5 = len(message5)
						send_length5 = str(msg_length5).encode(FORMAT)
						send_length5 += b' ' * (HEADER- len(send_length5))
						message6 = bytes(Chess.CurrentStatusMsg,FORMAT)
						msg_length6 = len(message6)
						send_length6 = str(msg_length6).encode(FORMAT)
						send_length6 += b' ' * (HEADER- len(send_length6))
						if Chess.GaveUpBlack == True:
							GaveUpBool = "You"
						elif Chess.GaveUpWhite == True:
							GaveUpBool = "Other"
						else:
							GaveUpBool = "False"
						msg7 = GaveUpBool.encode(FORMAT)
						msg_length7 = len(msg7)
						send_length7 = str(msg_length7).encode(FORMAT)
						send_length7 += b' ' * (HEADER- len(send_length7))
						if Chess.UpdateTimeD == True:
							SendUpdate = "True"
						else:
							SendUpdate = "False"
						msg8 = SendUpdate.encode(FORMAT)
						msg_length8 = len(msg8)
						send_length8 = str(msg_length8).encode(FORMAT)
						send_length8 += b' ' * (HEADER- len(send_length8))
						if Chess.PawnBlackClient == True:
							SendPawn = "BlackTrue"
						else:
							SendPawn = "False"
						msg9 = SendPawn.encode(FORMAT)
						msg_length9 = len(msg9)
						send_length9 = str(msg_length9).encode(FORMAT)
						send_length9 += b' ' * (HEADER- len(send_length9))
						P2_Client.send(DettectionSend)
						P2_Client.send(send_length1)
						P2_Client.send(message)
						P2_Client.send(send_length2)
						P2_Client.send(message2)
						P2_Client.send(send_length3)
						P2_Client.send(message3)
						P2_Client.send(send_length4)
						P2_Client.send(message4)
						P2_Client.send(send_length5)
						P2_Client.send(message5)
						P2_Client.send(send_length6)
						P2_Client.send(message6)
						P2_Client.send(send_length7)
						P2_Client.send(msg7)
						P2_Client.send(send_length8)
						P2_Client.send(msg8)
						P2_Client.send(send_length9)
						P2_Client.send(msg9)
						Chess.User2Recieve = False
			except:
				pass
		else:
			sys.exit(1)
			
			
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

