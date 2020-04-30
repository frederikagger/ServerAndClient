import socket
from pip._vendor.distlib.compat import raw_input
from Protocol import *


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# count message number
count = 0
server_address = ('127.0.0.1', 20000)
message = request(server_address[0]).encode()  # message in three way handshake
msg = 'hello, i am new user'  # message to be parsed to function clientMessage(msg)


while True:
    print('\nClient: {}'.format(message).encode())
    sent = sock.sendto(message, server_address)
    count = count + 1
    # Receive response
    data, server = sock.recvfrom(4096)
    count = count + 1
    print('\nServer: {}'.format(data.decode()))
