#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket
import time
import random
import math

def createTraffic(dataSize):
    inputString = ''
    for i in range(int(dataSize)-1):
        inputString += '1'
    inputString += '0'
    return inputString


host = '' 
port = 8000 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

while 1:
    client, address = s.accept() 
    data = client.recv(size).decode()
    print('got data\n')
    breakup = data.split('//') # second field should be size of HTTP request
    if (breakup[0] == 'GET http:'):
        print('registered HTTP request')
        client.send(createTraffic(breakup[1]).encode())
    else: 
        client.send(data.encode())
    # close connection after responding to data
    client.close()
