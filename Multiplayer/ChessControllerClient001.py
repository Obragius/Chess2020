import threading
import time
import wx
import socket

HEADER = 64
PORT = 1231
SERVER = "25.47.70.115"
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

while True:
	Info = input("Enter a message\n")
	if Info == "Q":
		send(DISCONNECT_MESSAGE)
		break
	else:
		send(Info)