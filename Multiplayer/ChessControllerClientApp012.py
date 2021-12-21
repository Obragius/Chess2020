import threading
import time
import wx
import socket
import pickle
import sys


import tkinter as tk



root = tk.Tk()
root.title("Starting Client")
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

Button = tk.Button(root, text="Start Client", command=OnClick)
Button.place(relx=0.41, rely=0.3)

root.bind('<KeyPress>', OnKeyPress)

root.mainloop()
time.sleep(0.5)

HEADER = 64
# SERVER = input("Input IP: ")
# PORT = int(input("Input Port: "))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '&USEROUT'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	import ChessControllerClient139 as Chess
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER- len(send_length))
	client.send(send_length)
	client.send(message)
	Structure = Chess.GiveUP
	Give = Structure.encode(FORMAT)
	msg_length2 = len(Give)
	send_length2 = str(msg_length2).encode(FORMAT)
	send_length2 += b' ' * (HEADER- len(send_length2))
	client.send(send_length2)
	client.send(Give)

def ChessFunc():
	# import ChessControllerClient139 as Chess
	app = Chess.App()
	app.MainLoop()

def SendBoard():
	# import ChessControllerClient139 as Chess
	local_Send_Press = False
	while Chess.ChessRun:
		time.sleep(0.015)
		send(Chess.Send_Status_Press)
		Chess.Send_Status_Press = ""
		Chess.GiveUP = "False"

def ListenForBoard():
	# import ChessControllerClient139 as Chess
	while Chess.ChessRun:
		time.sleep(0.01)
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
			msg_len5 = client.recv(HEADER).decode(FORMAT)
			msg_len5 = int(msg_len5)
			msg5 = client.recv(msg_len5)
			SentMessageList = pickle.loads(msg5)
			if SentMessageList != Chess.MessageList:
				Chess.MessageList = []
				for Value in SentMessageList:
					Chess.MessageList.append(Value)
			msg_len6 = client.recv(HEADER).decode(FORMAT)
			msg_len6 = int(msg_len6)
			msg6 = client.recv(msg_len6)
			Chess.CurrentStatusMsg = msg6.decode(FORMAT)
			msg_len7 = client.recv(HEADER).decode(FORMAT)
			msg_len7 = int(msg_len7)
			GiveUPBool = client.recv(msg_len7).decode(FORMAT)
			Chess.GiveUPDis = GiveUPBool
			msg_len8 = client.recv(HEADER).decode(FORMAT)
			msg_len8 = int(msg_len8)
			UpdateFromRestart = client.recv(msg_len8).decode(FORMAT)
			if UpdateFromRestart == "True":
				Chess.UpdateTimeD = True
			msg_len9 = client.recv(HEADER).decode(FORMAT)
			msg_len9 = int(msg_len9)
			PawnMessage = client.recv(msg_len9).decode(FORMAT)
			if PawnMessage == "WhiteTrue":
				Chess.WhitePawnDis = True
				Chess.PawnDelete = False
			elif PawnMessage == "BlackTrue":
				Chess.BlackPawnDis = True
				Chess.PawnDelete = False
			else:
				Chess.WhitePawnDis = False
				Chess.BlackPawnDis = False
				Chess.PawnDelete = True

		
		
import ChessControllerClient139 as Chess		

t1 = threading.Thread(target=ChessFunc)
t2 = threading.Thread(target=ListenForBoard)
t3 = threading.Thread(target=SendBoard)
t1.start()
t2.start()
t3.start()




