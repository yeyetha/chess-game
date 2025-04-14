import socket
import threading

class NetworkServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.conn = None
        self.addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        print("Waiting for connection...")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected to {self.addr}")

    def send_move(self, move):
        self.conn.sendall(move.encode())

    def receive_move(self):
        return self.conn.recv(1024).decode()

class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("Connected to server")

    def send_move(self, move):
        self.socket.sendall(move.encode())

    def receive_move(self):
        return self.socket.recv(1024).decode()
