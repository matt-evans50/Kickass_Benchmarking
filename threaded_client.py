#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time                 # you guessed it
import random
import math
from multiprocessing import Process

host = 'localhost' # Get local machine name
port = 8000               # Reserve a port for your service.
iterations = 2           # number of times each client sends data
numProcs = 4               # number of processes to run

#inputSize = math.ceil(100*random.paretovariate(2))


def createHTTPrequest(alpha, randMode):
    # outputs in the format: 'GET http://[number of bytes]
    if (randMode == 1): # pareto distribution
        inputSize = math.ceil(100*random.paretovariate(alpha))
    elif (randMode == 2): # uniform distribution
        inputSize = math.ceil(100*random.randrange(400))
    elif (randMode == 3): #exponential distribution
        inputSize = math.ceil(100*random.expovariate(1/200))
    return 'GET http://' + str(inputSize)

def createTraffic(alpha, randMode):
    # creates a random number of bytes ('1's)ending in a '0'
    if (randMode == 1): # pareto distribution
        inputSize = math.ceil(100*random.paretovariate(alpha))
    elif (randMode == 2): # uniform distribution
        inputSize = math.ceil(100*random.randrange(400))
    elif (randMode == 3): #exponential distribution
        inputSize = math.ceil(100*random.expovariate(1/200))
    inputString = ''
    for i in range(inputSize):
        inputString += '1'
    inputString += '0'
    return inputString

def getWaitTime(meanWaitTime):
    waitlen = random.expovariate(1/meanWaitTime)
    return waitlen



def createClient(iterations, id):
    for i in range(0,iterations):
        s = socket.socket()         # Create a socket object
        print(str(id) + ' connecting...')
        s.connect((host, port))
        print('connection successful.')
        print('send HTTP request:')
        inputString = createHTTPrequest(2, 1)
        print(inputString)
        r=inputString
        start_time = time.time()
        s.send(r.encode())
        data = s.recv(1024).decode()
        elapsed = time.time() - start_time
        print('elapsed time: ', elapsed)
        s.close()
        print('socket closed')
        time.sleep(getWaitTime(1))




if __name__ == '__main__':
    processes = [Process(target=createClient, args=(iterations, ('client' + str(id))), name=('client' + str(id))) for id in range(0,numProcs) ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print("All clients done.");



''' steps forward:

client:
    pick size data chunk
    wait (rho time)
    sends
    [kickass: exponential times, pareto sizes]

implement sizes from 1) uniform (all random)
                     2) exponential
                     3) pareto



NEXT:
add a number of clients to congest the network
    Each draws from the same distribution, with different randomly selected parameters

multiprocessing library!
HTTP requests (GET, ACK, etc.) [there is a python library for this]
    client: sends request for a URL
    server: response: k bytes (not really important what it contains)

structure: keep application structure separate
1) bulk data - threading
2) http-esque

priorities
1) threading/multi-processing
2) HTTP-ish structure
3) TCP-level information (rate of how fast it was supposed to send at)


Data Reporting:
flow was N bytes long
log time every k bytes (charts throughput over time)
total bytes vs. time (visualize how smooth the flow is) [TCP Dump]
send 100 packets, record time, repeat
    if time - wireshark/tcp dump creates file called pcap which contains flow info
    

, threads library may be useful
    want NO GLOBAL PROCESSING LOCK


HTTP Traffic



Report:
Diagrams of what we're doing, how it works.
'''
            