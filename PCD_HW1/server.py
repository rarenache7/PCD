import socket
import sys
import os


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


# Server protocol type
sock_proto = ''
buff_size = 4096  # default buffer size - small power of 2
if sys.argv[1]:  # Server protocol choice
    if sys.argv[1] == 'TCP':
        sock_proto = socket.SOCK_STREAM
    elif sys.argv[1] == 'UDP':
        sock_proto = socket.SOCK_DGRAM

if sys.argv[2] != '':  # Set buffer size
    buff_size = int(sys.argv[2])

print('Chosen server protocol: ', sys.argv[1])

families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a <sock_proto> socket
sock = socket.socket(socket.AF_INET, sock_proto)

# Bind the socket to the port
server_address = (socket.gethostname(), 10001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])

# Listen for incoming connections
if sys.argv[1] == 'TCP':
    sock.listen(3)  # 3 incoming connections at once supported

while True:
    if sys.argv[1] == 'TCP':
        # Wait for a connection
        print('Waiting for a connection..\n')
        connection, client_address = sock.accept()
        print('Client connection from', client_address)
        # Open file descriptor to write received file
        recv_file_fd = open(os.getcwd() + '\\server_storage\\recv.mp4', 'wb')
        # Receive the data in small chunks
        print('Receiving data bytes..\n')
        data_count = 1
        data = connection.recv(buff_size)
        print('Received ', data_count * buff_size, ' bytes of data..')
        while data:
            recv_file_fd.write(data)
            data = connection.recv(buff_size)
            data_count += 1
            print('Received ', data_count * buff_size, ' bytes of data..')
        print('Done receiving!')
        recv_file_fd.close()
        # Clean up the connection
        connection.close()
    elif sys.argv[1] == 'UDP':
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(4096)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data)

        if data:
            sent = sock.sendto(data, address)
            print('sent {} bytes back to {}'.format(
                sent, address))
