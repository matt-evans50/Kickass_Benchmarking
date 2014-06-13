#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time                 # you guessed it
import random
import math
from multiprocessing import Process
import argparse               # example for using this module: https://docs.python.org/3.4/library/argparse.html#module-argparse
#import matplotlib.pyplot as plt
#import numpy as np

host = '129.105.7.79'          # Get local machine name
port = 8000               # Reserve a port for your service.
iterations = 2           # number of times each client sends data
numProcs = 4               # number of processes to run
fileBase = "kickassBenchmarkingOutput"
args = None


def createHTTPrequest(alpha, randMode):
    # outputs in the format: 'GET http://[number of bytes]
    if (randMode == 'pareto'): # pareto distribution
        inputSize = math.ceil(10000*random.paretovariate(alpha))
    elif (randMode == 'rand'): # uniform distribution
        inputSize = math.ceil(10000*random.randrange(400))
    elif (randMode == 'exp'): #exponential distribution
        inputSize = math.ceil(10000*random.expovariate(1/200))
    return 'GET http://' + str(int(inputSize))


def getWaitTime(meanWaitTime):
    waitlen = random.expovariate(1/meanWaitTime)
    return waitlen


# each process (client) creates output file to graph later
def createClient(iterations, id):
    xvals = [] # number of bytes transferred
    yvals = [] # flow completion time
    tvals = [] # times at which 1024 bytes have been sent
    zvals = [] # integer number line representing num of packet sent 
    for i in range(0,iterations):
        print('iteration', i, 'of', iterations)
        s = socket.socket()         # Create a socket object
        #print(str(id) + ' connecting to ' + str(args.dest) + ':' + str(args.port) + '...')
        #s.setsockopt(socket.IPPTROTO_TCO, 13, "reno")        
        s.connect((host, args.port))
        #print('connection successful.')
        #print('send HTTP request:')
        inputString = createHTTPrequest(2, args.sizeDist)
        breakup = inputString.split('//')
        numBytes = int(breakup[1])
        xvals = xvals + [numBytes]
        #print(inputString)
        r=inputString
        s.send(r.encode())
        packetNo = 1 # index used to keep track of number of packets
        start_time = time.time()
        data = s.recv(1024).decode()
        #start_time = time.time()
        while data[-1] != '0':
            elapsed = (time.time() - start_time)*1000 # figure out tval
            #print(elapsed)
            tvals = tvals + [elapsed]
            zvals = zvals + [packetNo]
            data = s.recv(1024).decode()
            #time.sleep(0.0001)
            packetNo += 1
        elapsed = (time.time() - start_time)*1000 # puts in ms
        yvals = yvals + [elapsed]
        #print('elapsed time: ', elapsed, 'ms')
        s.close()
        #print('socket closed')
        time.sleep(getWaitTime(1))
    '''
    plt.plot(zvals, tvals)
    plt.xlabel('Number of Packets Transferred (1024B)')
    plt.ylabel('Elapsed Transmission Time (ms)')
    plt.title('The Life of a Flow')    
    plt.axis([0, max(zvals), 0, max(tvals)])
    #plt.show()    
    
    #x = np.arange(xvals)
    plt.plot(xvals, yvals, linestyle="none", marker=".")
    plt.xlabel('Number of Bytes Transferred')
    plt.ylabel('Transmission Time (ms)')
    plt.title('Transfer Time based on Message Size')    
    plt.axis([min(xvals), max(xvals), min(yvals), max(yvals)])
    plt.show()
    ''' 
    # Print out arrays
    try:
        f = open(fileBase + '-' + str(id), 'w')
        for x in xvals:
            f.write(str(x) + '\t')
        f.write('\n')
        for y in yvals:
            f.write(str(y) + '\t')
        f.write('\n')
        for t in tvals:
            f.write(str(t) + '\t')
        f.write('\n')
        for z in zvals:
            f.write(str(z) + '\t')
        f.write('\n')
    except IOError as error:
        print("Error") 
        


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
