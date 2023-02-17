import socket
import threading
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *

HOST = '192.168.1.5'
PORT = 33000
BUFFER = 1024
ADDR = (HOST, PORT)
FORMAT = "utf-8"

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFFER).decode(FORMAT)
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, FORMAT))


top = tkinter.Tk()
top.title("Messenger")

background_image = PhotoImage(file="stray.png")
background_label = Label(top, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15,
                           width=50, yscrollcommand=scrollbar.set, bg='#C1C1CD')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(
    top, text="Send", command=send, bg='green', fg='white')
send_button.pack()


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
