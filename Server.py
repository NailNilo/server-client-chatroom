import socket
import threading
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '192.168.1.5'
PORT = 33000
BUFFER = 1024
FORMAT = 'utf-8'
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("User %s:%s Connected to The Server." % client_address)
        client.send(
            bytes("Please Enter Your Nickname: ", FORMAT))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFFER).decode(FORMAT)
    welcome = 'Welcome To The Chatroom %s!' % name
    client.send(bytes(welcome, FORMAT))
    msg = "%s Has Joined The Chat!" % name
    broadcast(bytes(msg, FORMAT))
    clients[client] = name

    while True:
        msg = client.recv(BUFFER)
        broadcast(msg, name+": ")


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, FORMAT)+msg)


if __name__ == "__main__":
    SERVER.listen()
    print("[The SERVER IS STARTING...]")
    print(f"The Server is Active On: {HOST}")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
