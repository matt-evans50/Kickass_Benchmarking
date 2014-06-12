#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time                 # you guessed it
import random
import math
from multiprocessing import Process
import argparse               # example for using this module: https://docs.python.org/3.4/library/argparse.html#module-argparse

host = 'localhost'          # Get local machine name
port = 8000               # Reserve a port for your service.
iterations = 2           # number of times each client sends data
numProcs = 4               # number of processes to run
fileName = 'client-timing-'
args = None


def createHTTPrequest(alpha, randMode):
    # outputs in the format: 'GET http://[number of bytes]
    if (randMode == 'pareto'): # pareto distribution
        inputSize = math.ceil(100*random.paretovariate(alpha))
    elif (randMode == 'rand'): # uniform distribution
        inputSize = math.ceil(100*random.randrange(400))
    elif (randMode == 'exp'): #exponential distribution
        inputSize = math.ceil(100*random.expovariate(1/200))
    return 'GET http://' + str(int(inputSize))

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
        goodFile = False
        try:
            f = open(fileName + str(id), 'w')
            goodFile = True
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        s = socket.socket()         # Create a socket object
        print(str(id) + ' connecting to ' + str(args.dest) + ':' + str(args.port) + '...')
        s.connect((args.dest, args.port))
        print('connection successful.')
        print('send HTTP request:')
        inputString = createHTTPrequest(2, args.sizeDist)
        print(inputString)
        r=inputString
        start_time = time.time()
        s.send(r.encode())
        data = s.recv(1024).decode()
        elapsed = time.time() - start_time
        print('elapsed time: ', elapsed)
        s.close()
        print('socket closed')
        f.write(str(start_time) + '\t' + str(elapsed) + '\t')
        f.close()
        time.sleep(getWaitTime(1))


def handleCommandLineArguments():
    global args

    parser = argparse.ArgumentParser(description = 'Start threaded client for Kickass testing.')
    # dest: destination address of server
    parser.add_argument('-d', '--dest', default='localhost')
    # port: port to connect to
    parser.add_argument('-p', '--port', type=int, default=8000)
    # iterations: the number of times each client sends data
    parser.add_argument('-i', '--iter', type=int, default=2)
    # numClients: the number of clients to start up (as separate processes)
    parser.add_argument('-n', '--numClients', type=int, default=2)
    # sizeDist: the type of distribution of sizes (pareto, rand, exp)
    parser.add_argument('--sizeDist', type=str, default='pareto')
    # waitDist: type of distribution of wait between sends
    #parser.add_argument('-w', '--wait')


    args = parser.parse_args()




if __name__ == '__main__':
    # handle command line args, this function will quit program if error in options
    handleCommandLineArguments()

    processes = [Process(target=createClient, args=(args.iter, ('client' + str(id))), name=('client' + str(id))) for id in range(0,args.numClients) ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print("All clients done.");




            
