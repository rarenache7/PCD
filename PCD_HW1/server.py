import socket
import sys
import os


# Server protocol type
sock_proto = ''
# Package / buffer size
pack_size = 512  # default buffer size - small power of 2


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


# Get statistics at the end of client's execution
def get_stats():
    print('\nClient session ended')
    print('\n-------------------')
    print('Client session info below:')
    print('\tFamily  :', families[sock.family])
    print('\tType    :', types[sock.type], '(' + sys.argv[1] + ')')
    print('\tProtocol:', protocols[sock.proto])
    print('\tData chunks read: ', data_count)
    print('\tData bytes read: ', data_count * pack_size)
    print('-------------------\n')


# Decide connection type for a client session
def determine_connection_type(conn_type):
    global sock_proto
    if conn_type == 'TCP':
        sock_proto = socket.SOCK_STREAM
    elif conn_type == 'UDP':
        sock_proto = socket.SOCK_DGRAM


def set_packet_size(given_size):
    global pack_size
    if given_size != '':  # Set buffer size
        pack_size = int(given_size)


def set_file_name(given_name):
    global file_name
    if given_name:
        file_name = given_name


determine_connection_type(sys.argv[1])
set_packet_size(sys.argv[2])
# set_file_name(sys.argv[3])

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

# Listen for incoming connections
if sys.argv[1] == 'TCP':
    sock.listen(3)  # 3 incoming connections at once supported

client_id = 1
while True:
    if sys.argv[1] == 'TCP':
        # Wait for a connection
        print('Waiting for a connection..\n')
        connection, client_address = sock.accept()
        print('Client connection from', client_address)
        # Open file descriptor to write received file
        recv_file_fd = open(os.getcwd() + '/recv' + str(client_id), 'wb')
        # Receive the data in small chunks
        print('Receiving data bytes..\n')
        data_count = 0
        data = connection.recv(pack_size)
        # print('Received ', pack_size, ' bytes of data..')
        while data:
            recv_file_fd.write(data)
            data = connection.recv(pack_size)
            data_count += 1
            # print('Received ', data_count * pack_size, ' bytes of data..')
        print('Done receiving!')
        recv_file_fd.close()
        # Clean up the connection
        connection.close()
        get_stats()
    elif sys.argv[1] == 'UDP':
        data_count = 1
        print('\nWaiting to receive data bytes..')
        data, address = sock.recvfrom(pack_size)
        # while len(data) < pack_size:
        recv_file_fd = open(os.getcwd() + '/recv' + str(client_id), 'wb')
        # print('Received ', data_count * pack_size, ' bytes of data..')
        while data:
            recv_file_fd.write(data)
            data, address = sock.recvfrom(pack_size)
            if data.decode('ISO-8859-1') == 'done':
                print('Transfer is done!')
                break
            data_count += 1
            # print('Received ', data_count * pack_size, ' bytes of data..')
        print('Done receiving!')
        data_count -= 1
        recv_file_fd.close()
        get_stats()
