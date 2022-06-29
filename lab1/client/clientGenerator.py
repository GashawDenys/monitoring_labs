import client
import sys
import random
import time


def client_jobs_generator(clientName):
    random.seed()

    for i in range(50):
        time.sleep(random.randint(100, 400) / 1000)
        client.client_job(clientName)


if __name__ == "__main__":
    client_jobs_generator(sys.argv[1])
