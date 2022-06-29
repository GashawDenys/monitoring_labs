import socket
import re
import time
import threading

STAYING = 0
GOING_UP = 1
GOING_DOWN = 2
N = 5


class Elevator:
    people = []
    floor = 1
    f1f = {}
    fq1 = []
    fq2 = []
    fq3 = []
    fq4 = []
    fq5 = []
    state = STAYING

    def appendPeople(self, person):
        self.people.append(person)
        print("Cur elevator people: " + str(self.people))

    def appenddict(self, floorn, person):
        self.f1f[person] = floorn

    def appendq(self, qn, person):
        if qn == 1:
            self.fq1.append(person)
        if qn == 2:
            self.fq2.append(person)
        if qn == 3:
            self.fq3.append(person)
        if qn == 4:
            self.fq4.append(person)
        if qn == 5:
            self.fq5.append(person)

    def queueReduce(self, queue, people):
        return [x for x in queue if x not in people]
        # if qnum == 1:
        #     self.fq1 = [x for x in self.fq1 if x not in people]

    def firstFloorUpDict(self, people):
        maxFloor = 2
        print(self.f1f)
        for person in people:
            if person in self.f1f:
                if maxFloor < self.f1f[person]:
                    maxFloor = self.f1f[person]
                self.f1f.pop(person)
        return maxFloor

    def checkDict(self, person):
        return person in self.f1f

    def checkq(self, person, qn):
        if qn == 1:
            return person in self.fq1
        if qn == 2:
            return person in self.fq2
        if qn == 3:
            return person in self.fq3
        if qn == 4:
            return person in self.fq4
        if qn == 5:
            return person in self.fq5

    def get_peopleq(self):
        return len(self.people)

    def longestQueue(self):
        lenL = [len(self.fq2), len(self.fq3), len(self.fq4), len(self.fq5)]
        return lenL.index(max(lenL)) + 2

    def setFloor(self, floor):
        self.floor = floor

    def go_up(self, floorn):
        self.state = GOING_UP
        time.sleep(0.2)
        self.floor = floorn

        time.sleep(0.3)
        print("Passengers " + str(self.people) + " lifted")
        self.fq1 = self.queueReduce(self.fq1, self.people)
        self.people = []
        self.state = STAYING

    def go_down(self, floorn):
        self.state = GOING_DOWN
        time.sleep(0.3)
        self.floor = 1
        print("Passengers went down from " + str(floorn) + " " + str(self.people))


        self.people = []
        self.state = STAYING
        # self.f1f = {}
        # if self.floor < floorn:
        #     self.state = self.GOING_DOWN

    def tryAppendPerson(self, person, floorFrom, floor_to=-1):
        # print(self.checkq(person, floorFrom))
        if not self.checkq(person, floorFrom):
            if floorFrom == 1:
                self.appenddict(floor_to, person)
            self.appendq(floorFrom, person)
        if self.checkq(person, floorFrom) and len(self.people) < N and self.state == STAYING and floorFrom == self.floor:
            if floorFrom == 1:
                self.fq1 = self.queueReduce( self.fq1, [person])
            if floorFrom == 2:
                self.fq2 = self.queueReduce( self.fq2, [person])
            if floorFrom == 3:
                self.fq3 = self.queueReduce( self.fq3, [person])
            if floorFrom == 4:
                self.fq4 = self.queueReduce( self.fq4, [person])
            if floorFrom == 5:
                self.fq5 = self.queueReduce( self.fq5, [person])
            # self.queueReduce(floorFrom, [person])
            self.appendPeople(person)

            return True
        else:
            return False

    def __init__(self, n=5, people=[], floor=1):
        self.state = STAYING
        self.N = n
        self.people = people
        self.floor = floor
        self.f1f = {}
        self.fq1 = []
        self.fq2 = []
        self.fq3 = []
        self.fq4 = []
        self.fq5 = []


disconnectionMsg = "please disconnect!"
elevator = Elevator(N, people=[], floor=1)


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
            clientName = strData.split(':')[0]
            # print(clientName)
            floors = re.findall(r'\d+', strData)[-2:]
            floorFrom = int(floors[0])
            floorTo = int(floors[1])
            inEl = False
            if floorFrom == 1:
                elevator.appenddict(floorTo, clientName)
                if elevator.tryAppendPerson(clientName, floorFrom, floorTo):
                    inEl = True
                else:
                    # elevator.appendq(floorFrom, clientName)
                    while not inEl:
                        time.sleep(0.05)
                        inEl = elevator.tryAppendPerson(clientName, floorFrom, floorTo)
            else:
                if elevator.tryAppendPerson(clientName, floorFrom):
                    print("right into elevator2")
                    inEl = True
                else:
                    # elevator.appendq(floorFrom, clientName)
                    while not inEl:
                        time.sleep(0.05)
                        inEl = elevator.tryAppendPerson(clientName, floorFrom)
        time.sleep(0.1 * (abs(floorTo - floorFrom)))
        # else:
        #     workTime = int(re.findall(r'\d+', strData)[-1]) / 1000
        #     print(workTime)
        #     time.sleep(workTime)
        c.send('Thank you for asking'.encode())
    c.close()


def elevatorSim():
    time.sleep(0.5)
    passN = 0
    while True:
        print(elevator.floor)
        print(passN)
        print("fq1 " + str(elevator.fq1))
        print("fq2 " + str(elevator.fq2))
        print("fq3 " + str(elevator.fq3))
        print("fq4 " + str(elevator.fq4))
        print("fq5 " + str(elevator.fq5))
        passN += 1
        if elevator.state == STAYING and passN % 4 == 0:
            # time.sleep(0.1)
            elevator.setFloor(elevator.longestQueue())
            # time.sleep(0.1)
            print("taking from " + str(elevator.longestQueue()))


        elif elevator.floor == 1 and elevator.state == STAYING:
            time.sleep(0.1)
            if elevator.get_peopleq() == 0:
                continue
            print("Elevator lifting job")
            elevator.state = GOING_UP
            floor = elevator.firstFloorUpDict(elevator.people)
            time.sleep(0.1)
            elevator.go_up(floor)
            # time.sleep(0.1)
        elif elevator.state == STAYING:
            time.sleep(0.1)
            print("Elevator shifting job")
            elevator.state = GOING_DOWN
            time.sleep(0.1)
            elevator.go_down(elevator.floor)
            # time.sleep(0.1)



def main():
    s = socket.socket()
    print("Socket successfully created")

    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))

    s.listen()
    print("socket is listening")
    elevatorThread = threading.Thread(target=elevatorSim)
    elevatorThread.start()
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        thread = threading.Thread(target=client_interaction, args=(c, addr))
        thread.start()
        print("Current connections " + str(threading.activeCount() - 1))


if __name__ == "__main__":
    main()
