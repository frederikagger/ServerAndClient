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
'''
try:
    # Send data
    print('\nClient {}'.format(clientAccept))
    sent = sock.sendto(clientAccept().encode(), server_address)
    # Receive response
    data, server = sock.recvfrom(4096)
    print('\nServer: {}'.format(data.decode()))

    if data.decode() == serverAccept(server_address[0]):
        print('\nClient {}'.format(clientAccept()))
        sent = sock.sendto(clientAccept().encode(), server_address)
    else:
        sock.close()

except IOError:
    sock.close()'''


while True:
    st = raw_input("")
    print('\nClient: {}'.format(clientMessage(count, st)))
    sent = sock.sendto(st.encode(), server_address)
    count = count + 1
    # Receive response
    data, server = sock.recvfrom(4096)
    count = count + 1
    print('\nServer: {}'.format(data.decode()))
