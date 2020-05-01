import socket
import threading
from Protocol import *
from serverFunctions import getCountFromMsg
import time
import logging
from datetime import datetime


# Function that resets the connection
def resetCon(sock1: socket):
    global clientAddress
    try:
        sent = sock1.sendto(serverResetCon().encode(), clientAddress)
    except OSError:
        print('Caught OSError')
    finally:
        sock1.close()

    
# Function that a supposed to count packages pr. second but it doesnt work yet
def countPackagesPrSec(count: int):
    serverIsNotBeingSpammed: bool = False
    while serverIsNotBeingSpammed is False:
        before = count
        print(before)
        time.sleep(1)
        after = count
        print(after)
        if (after - before) > 50:
            print('The server is being spammed. Closing the connection.')
            serverIsNotBeingSpammed = True
            resetCon()


def handshake(sock1: socket):
    untilRequestFromClient(sock1)
    address = untilAccept(sock1)
    return address, True


def untilRequestFromClient(sock1):
    firstPartOfHandshake: bool = False
    while firstPartOfHandshake is False:
        # keep receiving incoming message until three way handshake
        data, address = sock1.recvfrom(4096)
        # if the first msg received equals the first msg in the protocol then send accept
        if data.decode() == request(address[0]):
            sent = sock1.sendto(serverAccept(address[0]).encode(), address)
            firstPartOfHandshake = True


def untilAccept(sock1):
    secondPartOfHandshake: bool = False
    while secondPartOfHandshake is False:
        data, address = sock1.recvfrom(4096)
        # if the 2 msg equals the 2 msg in the protocol accept client
        if data.decode() == clientAccept():
            secondPartOfHandshake = True
            timeOfEvent = datetime.now()
            logging.info(str(timeOfEvent) + ': Handshake completed with client with IP address' + str(address))
    return address


def receiveMessages(sock1: socket):
    global clientCount, clientAccepted, count
    while clientAccepted is True:
        isMsg: bool
        # sets a timer that runs the reset function when 4.0 sec has elapsed
        t = threading.Timer(4.0, resetCon, args=(sock1,))
        t.start()
        try:
            data, address = sock1.recvfrom(4096)
        except ConnectionResetError:
            break
        except OSError:
            break
        # timer resets after every msg received
        t.cancel()
        try:
            clientCount = getCountFromMsg(data.decode())
            isMsg = True
            # try to get count from every msg. When a msg that doesnt follow protocol is received it will raise a
            # ValueError if the received msg is a heartbeat it resets the timer else the connection is reset
        except ValueError:
            isMsg = False
            if data.decode() == heartbeat():
                t.cancel()
            else:
                resetCon(sock1)

        # if the client msg count is wrong breakout of the while loop
        if isMsg is True & clientCount != count:
            print('Count was: ' + str(count) + ' ClientCount was: ' + str(clientCount))
            clientAccepted = False

        # if the recevied is a msg send a servermessage and increment the count by 2. One for msg recieved and one for
        # msg send
        if isMsg:
            print('\nClient: {} '.format(data.decode()))
            count = count + 1
            sent = sock1.sendto(serverMessage(count).encode(), address)
            print('\nServer: {} '.format(serverMessage(count)))
            count = count + 1


def createSocket():
    # Create a UDP socket
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = ('localhost', 20000)
    sock1.bind(server_address)
    return sock1


# Setting configuration for logging
logging.basicConfig(filename='log.txt', level='INFO')
# message count on serverside
count = 0
clientAccepted = False
clientCount = 0

sock = createSocket()
clientAddress, clientAccepted = handshake(sock)
thread = threading.Thread(target=countPackagesPrSec, args=(count,))
receiveMessages(sock)
#receiveMessages(sock)
resetCon(sock)
