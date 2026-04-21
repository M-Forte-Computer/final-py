import socket
import threading

HOST = "127.0.0.1"
PORT = 55555

nickname = input("Client2 nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)

        except:
            print("Disconnected.")
            client.close()
            break

def write():
    while True:
        msg = input("")
        client.send(f"{nickname}: {msg}".encode("utf-8"))

threading.Thread(target=receive).start()
threading.Thread(target=write).start()