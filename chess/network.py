import socket
import threading

class NetworkServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.conn = None
        self.addr = None
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(1)
        print("Waiting for connection...")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected to {self.addr}")

    def send_move(self, move):
        try:
            self.conn.sendall(move.encode())
        except Exception as e:
            print("Connection lost while sending move:", e)
            self.running = False

    def receive_move(self):
        try:
            data = self.conn.recv(1024)
            if not data:
                self.running = False
                return None
            return data.decode()
        except Exception as e:
            print("Connection lost while receiving move:", e)
            self.running = False
            return None

    def close(self):
        self.conn.close()
        self.socket.close()


class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
            print("Connected to server")
            self.running = True
        except Exception as e:
            print("Connection failed:", e)
            self.running = False

    def send_move(self, move):
        try:
            self.socket.sendall(move.encode())
        except Exception as e:
            print("Connection lost while sending move:", e)
            self.running = False

    def receive_move(self):
        try:
            data = self.socket.recv(1024)
            if not data:
                self.running = False
                return None
            return data.decode()
        except Exception as e:
            print("Connection lost while receiving move:", e)
            self.running = False
            return None

    def close(self):
        self.socket.close()
