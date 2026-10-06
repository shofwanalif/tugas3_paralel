import socket
import threading
import time
from threading import current_thread

HOST = "127.0.0.1"
PORT = 5000


class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        print(f"{current_thread().name}: terhubung dengan {self.client_address}")
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data: 
                    break

                message = data.decode("utf-8").strip()
                print(f"{current_thread().name}: pesan dari client - {message}")

                if message.lower() == "exit":
                    self.client_socket.sendall("Server menerima: exit".encode("utf-8"))
                    break

                time.sleep(1) 
                reply = f"Server menerima: {message}"
                self.client_socket.sendall(reply.encode("utf-8"))
        except ConnectionResetError:
            print(f"{current_thread().name}: koneksi diputus paksa oleh client")
        finally:
            self.client_socket.close()
            print(f"{current_thread().name}: koneksi {self.client_address} ditutup")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(3)
    print(f"Server berjalan di {HOST}:{PORT}, menunggu client...")

    try:
        while True:
            client_socket, client_address = server.accept()
            thread = ClientThread(client_socket, client_address)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.close()


if __name__ == "__main__":
    main()