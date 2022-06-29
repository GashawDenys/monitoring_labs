import socket
import re
import time
import threading

N = 100

disconnectionMsg = "please disconnect!"


class ResStack:
    availableRes = N
    queue = {}
    queueL = []

    def appendToQueue(self, person, res_amount):
        self.queueL.append(person)
        self.queue[person] = res_amount

    def tryPop(self):
        print("Current work queue:" + str(self.queueL))
        if len(self.queueL) > 0:
            print("process wants " + str(self.queue[self.queueL[0]]) + ". and " + str(self.availableRes) + " available.")
            if self.availableRes - self.queue[self.queueL[0]] >= 0:
                print("Process " + str(self.queueL[0]) + " is now in process")
                time.sleep(self.queue[self.queueL[0]] * 0.02)
                self.availableRes -= self.queue[self.queueL[0]]
                self.queue.pop(self.queueL[0])
                self.queueL.pop(0)
                print("Available " + str(self.availableRes) + " resources")
                return True
            else:
                print("Server lacks " + str(self.queue[self.queueL[0]] - self.availableRes) + "resources.")
                return False
        else:
            # print("queue is empty")
            return False


    def retRecources(self, res_amount):
        print("Available " + str(self.availableRes) + " resources and freeing some...")
        self.availableRes += res_amount
        print("Now available " + str(self.availableRes))

    def isInQueue(self, person):
        return person in self.queueL

    def __init__(self, n):
        self.availableRes = n
        self.queue = {}
        self.queueL = []


resourcesStack = ResStack(N)


def client_interaction(c, addr):
    print("I'm busy with " + str(addr) + " connection")
    # work_start = time.time()
    # work_end = work_start
    connection = True
    while connection:
        data = c.recv(1024)
        strData = data.decode()

        print(strData)
        if strData == disconnectionMsg:
            connection = False
            work_end = time.time()
            work_time = work_end - work_start
            work_time_str = clientName + " spent there " + str(work_time) + " seconds."
            c.send(work_time_str.encode())
            print(c.recv(1024).decode())
        else:
            clientName = strData.split(':')[0]
            # print(clientName)
            print(strData)
            res_demand = int(re.findall(r'\d+', strData)[-1])
            work_start = time.time()
            c.send("Task understood".encode())
            print(c.recv(1024).decode())
            resourcesStack.appendToQueue(clientName, res_demand)
            while resourcesStack.isInQueue(clientName):
                time.sleep(0.05)
            resourcesStack.retRecources(res_demand)
            c.send("Job done!".encode())

        time.sleep(0.1)

        # else:
        #     workTime = int(re.findall(r'\d+', strData)[-1]) / 1000
        #     print(workTime)
        #     time.sleep(workTime)

    c.send('Thank you for asking'.encode())
    c.close()


def workSim():
    time.sleep(0.5)
    while True:
        time.sleep(0.02)
        resourcesStack.tryPop()


def main():
    s = socket.socket()
    print("Socket successfully created")

    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))

    s.listen()
    print("socket is listening")
    workThread = threading.Thread(target=workSim)
    workThread.start()

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        thread = threading.Thread(target=client_interaction, args=(c, addr))
        thread.start()
        print("Current connections " + str(threading.activeCount() - 1))


if __name__ == "__main__":
    main()
