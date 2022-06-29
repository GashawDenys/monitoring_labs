import socket
import re
import time
import threading

disconnectionMsg = "please disconnect!"


def client_interaction(c, addr):
    print("I'm busy with " + str(addr) + " connection")
    connection = True
    while connection:
        data = c.recv(1024)
        strData = data.decode()
        print(strData)
        if strData == disconnectionMsg:
            connection = False
        else:
            workTime = int(re.findall(r'\d+', strData)[-1]) / 1000
            print(workTime)
            time.sleep(workTime)
        c.send('Thank you for asking'.encode())
    c.close()


def main():
    s = socket.socket()
    print("Socket successfully created")

    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))

    s.listen()
    print("socket is listening")

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        thread = threading.Thread(target=client_interaction, args=(c, addr))
        thread.start()
        print("Current connections " + str(threading.activeCount() - 1))


if __name__ == "__main__":
    main()
