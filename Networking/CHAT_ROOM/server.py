import threading
import socket
import os
import dotenv

dotenv.load_dotenv()

HOST = os.environ.get("CHAT_ROOM_SERVER_IP")
PORT = int(os.environ.get("CHAT_ROOM_SERVER_PORT"))
CONFIRMATION_MESSAGE = os.environ.get("CHAT_ROOM_CONFIRMATION_MESSAGE")

class ChatServer:
    def __init__(self):
        self.clients = []
        self.nicknames = []

    def listen(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()
        print(f"Chat server has started running on the machine - ({HOST}/{PORT})")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                # Receieve a message from a client (1024 characters)
                message = client.recv(1024)
                self.broadcast(message)
            except:
                # Otherwise we remove the client from our list
                index = self.clients.index(client)
                nickname = self.nicknames[index]

                self.clients.remove(client)
                self.nicknames.remove(nickname)
                break

    def receive_client(self):
        while True:
            client, address = self.server.accept()

            print(f"Connection established with a client : {address}")
            client.send(CONFIRMATION_MESSAGE.encode("ascii"))

            nickname = client.recv(1024).decode("ascii")
            self.nicknames.append(nickname)
            self.clients.append(client)
            print(f"Client : {address} | Nickname : {nickname}")

            self.broadcast(f"{nickname} joined the chat!".encode("ascii"))
            client.send("Connected to our chat server".encode("ascii"))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


def main():
    chat_server = ChatServer()
    chat_server.listen()
    chat_server.receive_client()


if __name__ == "__main__":
    main()