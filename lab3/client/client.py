import socket
import random

disconnectionMsg = "please disconnect!"
MAX_RES = 100

def client_job(clientName):
    # Create a socket object
    s = socket.socket()
    # print("idle")
    # Define the port on which you want to connect
    port = 12345
    random.seed()
    workAmmount = 1
    # connect to the server on local computer
    print("waiting")
    s.connect(('127.0.0.1', port))

    # while workAmmount > 0:
    # work = random.randint(250, 900)
    # message = clientName + ": Work in milliseconds: " + str(work)
    # movement = random.randint(0, 1)
    res = random.randint(1, MAX_RES)
    message = clientName + ": I demand " + str(res) + " resources."


    s.sendall(message.encode())
    print("blocked")

    # receive data from the server and decoding to get the string.
    print(s.recv(1024).decode())
    s.sendall("Please work on it!".encode())
    print(s.recv(1024).decode())
    # workAmmount -= 1
    # close the connection
    s.sendall(disconnectionMsg.encode())
    print(s.recv(1024).decode())
    s.sendall("Thanks for the info!".encode())
    print(s.recv(1024).decode())
    s.close()
    print("idle")
