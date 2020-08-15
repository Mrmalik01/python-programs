import socket
import threading
import os
import dotenv

dotenv.load_dotenv()

HOST = os.environ.get("CHAT_ROOM_SERVER_IP")
PORT = int(os.environ.get("CHAT_ROOM_SERVER_PORT"))
CONFIRMATION_MESSAGE = os.environ.get("CHAT_ROOM_CONFIRMATION_MESSAGE")

class Client:
    def __init__(self, nickname):
        self.nickname = nickname

    def establish_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

    def receieve_message(self):
        while True:
            try:
                message = self.client.recv(1024).decode("ascii")
                if message == CONFIRMATION_MESSAGE:
                    self.client.send(str(self.nickname).encode("ascii"))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def send_message(self):
        while True:
            message = f"{self.nickname}: {input('')}"
            self.client.send(message.encode("ascii"))


    def receiveing_start(self):
        receieve_thread = threading.Thread(target=self.receieve_message)
        receieve_thread.start()

    def sending_start(self):
        send_thread = threading.Thread(target=self.send_message)
        send_thread.start()

def main():
    print("Chat room 11220 - ")

    nickname = input("Please enter your nickname to join the room - ")
    client = Client(nickname)
    client.establish_connection()
    client.receiveing_start()
    client.sending_start()

if __name__ == "__main__":
    main()