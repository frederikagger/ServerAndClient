import socket
import threading
from Protocol import *
from serverFunctions import getCountFromMsg
import time
import logging
from datetime import datetime


# Function that resets the connection
def resetCon():
    global sent, data, address, clientAccepted
    try:
        sent = sock.sendto(serverResetCon().encode(), address)
        clientAccepted = False
        sock.close()
    except OSError:
        print('Caught OSError')
        sock.close()


# Function that a supposed to count packages pr. second but it doesnt work yet
def countPackagesPrSec():
    global count, clientAccepted
    while True:
        before = count
        print(before)
        time.sleep(1)
        after = count
        print(after)
        if (after - before) > 25:
            print('The server is being spammed. Closing the connection.')
            clientAccepted = False
            resetCon()


# Setting configuration for logging
logging.basicConfig(filename='log.txt', level='INFO')

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 20000)

sock.bind(server_address)
# message count on serverside
count = 0
clientAccepted = False
clientCount = 0

# counter = threading.Thread(target=countPackagesPrSec)
# counter.start()

while clientAccepted is False:
    # keep receiving incoming message until three way handshake
    data, address = sock.recvfrom(4096)
    # if the first msg received equals the first msg in the protocol then send accept
    if data.decode() == request(address[0]):
        sent = sock.sendto(serverAccept(address[0]).encode(), address)
    # log the msg that did not follow protocol

    data, address = sock.recvfrom(4096)
    # if the 2 msg equals the 2 msg in the protocol accept client
    if data.decode() == clientAccept():
        clientAccepted = True
        timeOfEvent = datetime.now()
        logging.info(str(timeOfEvent) + ': Handshake completed with client with IP address' + str(address))
    # log the msg that did not follow protocol

while clientAccepted is True:
    isMsg: bool
    # sets a timer that runs the reset function when 4.0 sec has elapsed
    t = threading.Timer(4.0, resetCon)
    t.start()
    try:
        data, address = sock.recvfrom(4096)
    except ConnectionResetError:
        break
    except OSError:
        break
    # timer resets after every msg received
    t.cancel()
    try:
        clientCount = getCountFromMsg(data.decode())
        isMsg = True
        # try to get count from every msg. When a msg that doesnt follow protocol is received it will raise a ValueError
        # if the received msg is a heartbeat it resets the counter else the connection is reset
    except ValueError:
        isMsg = False
        if data.decode() == heartbeat():
            t.cancel()
        else:
            resetCon()

    # if the client msg count is wrong breakout of the while loop and close socket
    if isMsg is True & clientCount != count:
        print('Count was: ' + str(count) + ' ClientCount was: ' + str(clientCount))
        clientAccepted = False

    # if the recevied is a msg send a servermessage and increment the count by 1. One for msg recieved and one for
    # msg send
    if isMsg:
        print('\nClient: {} '.format(data.decode()))
        count = count + 1
        sent = sock.sendto(serverMessage(count).encode(), address)
        print('\nServer: {} '.format(serverMessage(count)))
        count = count + 1

sock.close()
