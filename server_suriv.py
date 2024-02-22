import socket
from threading import Thread

all_clients = []

conn_found = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# host = '127.0.0.1'
host = input("IP: ")
# port = 8080
port = int(input("PORT: "))

sock.bind((host, port))
sock.listen(5)

print(f"Server listening at: {(host,port)}")

def manage_conn():
    while True:
        command = input(">> ")
        if command == "cl":
            for s,a in all_clients:
                print(a, end="<|>")

            print("\n")
        
        else:
            args = command.split("<|>")
            request = args[-1]
            for element in args[0:-1]:
                client_socket = all_clients[int(element)][0]
                client_socket.send(request.encode())


def receiver(client, addr):
    while True:
        output = client.recv(1024).decode()
        if not output:
            print(f"Client ({addr}) disconnected.")
            break
        print(f"\n\n{addr} -> {output}\n\n")

    client.close()
    all_clients.remove((client, addr))


while True:
    c_sock, address = sock.accept()
    print(f"\n\nNew connection initiated: {address}\n\n")
    all_clients.append((c_sock, address))

    c_thread = Thread(target=receiver, args=(c_sock, address))
    c_thread.start()

    if not conn_found:
        conn_found = True
        thread = Thread(target=manage_conn)
        thread.start()


