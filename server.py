import socket
import threading

HOST = "127.0.0.1"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast mesajı
def broadcast(message):
    for client in clients:
        client.send(message)

# Her istemciyi yönetme fonksiyonu
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}: {message.decode('UTF-8')}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames.pop(index)
            print(f"{nickname} disconnected!")
            broadcast(f"{nickname} has left the chat.".encode("UTF-8"))
            break

# İstemcileri kabul etme fonksiyonu
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode("UTF-8"))
        nickname = client.recv(1024).decode("UTF-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode("UTF-8"))
        client.send("Connected to the server".encode("UTF-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server Run!!!")
receive()
