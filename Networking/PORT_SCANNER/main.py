import socket
import dotenv
import os
import json
import threading
from queue import Queue

dotenv.load_dotenv()

TARGET = os.environ.get("PORT_SCANNER_IP")
PORT = 80
FROM_PORT = 1
TO_PORT = 5000

queue = Queue()
result = {
    "opened" : [],
    "closed" : []
}

def portscan(port):
    global TARGET
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET, port))
        return True
    except:
        return False

def fill_queue(from_port, to_port):
    for port in range(from_port, to_port):
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if  portscan(port):
            result['opened'].append(port)
        else:
            result['closed'].append(port)

def save_result():
    global result
    with open("result.json", "w") as f:
        f.write(json.dumps(result))
        f.close()

def main():
    fill_queue(from_port=FROM_PORT, to_port=TO_PORT)

    # Making a list of threads
    thread_list = []
    for t in range(10):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    print(f"Checking ports in the range - ({FROM_PORT, TO_PORT}) - on the machine {TARGET}")
    # Start all the threads
    for thread in thread_list:
        thread.start()

    # Wait for all the threads to finish before saving the result to the file
    for thread in thread_list:
        thread.join()

    save_result()
    print("Result is saved to a file")


if __name__ == "__main__":
    main()
