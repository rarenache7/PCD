import socket
import sys
import os
import datetime

# Server protocol type
sock_proto = ''
# Package / buffer size
pack_size = 512  # default buffer size - small power of 2
# File to transfer
file_name = 'send'  # default file to transfer to server


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
    print('Done sending')
    print('\nClient execution ended')
    print('\n-------------------')
    print('Client session info below:')
    print('\tFamily  :', families[sock.family])
    print('\tType    :', types[sock.type], '(' + sys.argv[1] + ')')
    print('\tProtocol:', protocols[sock.proto])
    print('\tData chunks read: ', data_count)
    print('\tData bytes read: ', data_count * pack_size)
    print('\tClient transmission time:', end_timestamp - start_timestamp)
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
server_address = (socket.gethostname(), 10001)

if sys.argv[1] == 'TCP':
    # Connect the socket to the port where the server is listening
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
try:
    transfer_done_flag = ''
    if sys.argv[1] == 'TCP':
        send_file_fd = open(os.getcwd() + '/' + file_name, 'rb')
        # Send data
        print('Sending data bytes..\n')
        data = send_file_fd.read(pack_size)
        data_count = 1
        start_timestamp = datetime.datetime.now()#.replace(microsecond=0)
        while data:
            sock.send(data)
            print('Sent ', data_count * pack_size, ' bytes..')
            data = send_file_fd.read(pack_size)
            data_count += 1
        sock.shutdown(socket.SHUT_WR)
        send_file_fd.close()
        end_timestamp = datetime.datetime.now()#.replace(microsecond=0)
        get_stats()
    elif sys.argv[1] == 'UDP':
        send_file_fd = open(os.getcwd() + '/' + file_name, 'rb')
        print('Sending data bytes..\n')
        data = send_file_fd.read(pack_size)
        data_count = 1
        start_timestamp = datetime.datetime.now()  # .replace(microsecond=0)
        # Send data
        while data:
            traffic_sent = sock.sendto(data, server_address)
            while traffic_sent < pack_size and len(data) == pack_size:
                traffic_sent = sock.sendto(data, server_address)
            print('Sent ', data_count * pack_size, ' bytes..')
            data = send_file_fd.read(pack_size)
            data_count += 1
        send_file_fd.close()
        transfer_done_flag = 'done'
        traffic_sent = sock.sendto(transfer_done_flag.encode('ISO-8859-1'), server_address)
        end_timestamp = datetime.datetime.now()  # .replace(microsecond=0)
        get_stats()
finally:
    print('closing socket')
    sock.close()
