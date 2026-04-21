import socket
import threading
import subprocess
import sys
import time

HOST = "127.0.0.1"
PORT = 55555

clients = []
nicknames = []

def broadcast(message, _client):
    print(message.decode("utf-8"))  

    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()

        nickname = nicknames[index]
        nicknames.remove(nickname)

        broadcast(f"{nickname} left the chat.".encode("utf-8"), client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            remove_client(client)
            break

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER STARTED] {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {address}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"[NICKNAME] {nickname}")

        broadcast(f"{nickname} joined the chat!".encode("utf-8"), client)

        client.send("Connected!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



def launch_clients():
    time.sleep(1)

    print("[AUTO] Launching clients...")

    python = sys.executable

    subprocess.Popen(
        f'start cmd /k "{python} client.py"',
        shell=True
    )

    subprocess.Popen(
        f'start cmd /k "{python} cliant2.py"',
        shell=True
    )

threading.Thread(target=launch_clients).start()
receive_connections()