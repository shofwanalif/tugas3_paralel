import socket

HOST = "127.0.0.1"
PORT = 5000


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Terhubung ke server {HOST}:{PORT}. Ketik 'exit' untuk keluar.")

    try:
        while True:
            message = input("Pesan: ")
            if not message:
                continue

            client.sendall(message.encode("utf-8"))
            response = client.recv(1024).decode("utf-8")
            print(response)

            if message.strip().lower() == "exit":
                break
    finally:
        client.close()
        print("Koneksi ditutup.")


if __name__ == "__main__":
    main()