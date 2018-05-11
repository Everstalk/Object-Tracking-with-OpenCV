#!/usr/bin/python3

"""
----------------------------------------------------------------------------
Michael D. Saneke
Robotics Final Project
EV3 Robot code

EV3 Movement Library retrieved from Robotics Group(Ethel, Michael, Anthony)
----------------------------------------------------------------------------
"""


import socket
from movement.ev3movement.movement import * 
import time

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys


#Set up socket connection between Robot and Computer running OpenCV
def receive():

    port = 8000 
    size = 1024

    hostName = gethostbyname( '0.0.0.0' )

    mySocket = socket( AF_INET, SOCK_DGRAM )
    mySocket.bind( (hostName, port) )

    print ("Listening on port ",port)

    #Receiving data from OpenCV
    while True:
        (data,addr) = mySocket.recvfrom(size)
        data = data.decode('utf-8') #Decoding data received from bytes to text
        print (data)

        #Robot should turn right if command received from OpenCV is 'right'
        if data == 'right':
            turn_right_by_angle(10, 400)
            time.sleep(0.5)

        #Robot should turn left if command received from OpenCV is 'left'
        elif data == 'left':
            turn_left_by_angle(10, 400)
            time.sleep(0.5)
            
        else:
            break




def main():

    #Robot should coninuously listen on port 1000 for commands
    while True:
        receive()

            





    
main()
