import client
import sys
import random
import time


def client_jobs_generator(clientName):
    random.seed()
    for j in range(100):
        clientNameN = clientName + str(j)
        for i in range(1):
            time.sleep(random.randint(100, 400) / 1000)
            client.client_job(clientNameN)


if __name__ == "__main__":
    client_jobs_generator(sys.argv[1])
