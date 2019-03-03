import socket
import sys
import os
import datetime

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
# Package / buffer size
buff_size = 512  # default buffer size - small power of 2
# File to transfer
file_name = 'send'  # default file to transfer to server

if sys.argv[1]:
    if sys.argv[1] == 'TCP':
        sock_proto = socket.SOCK_STREAM
    elif sys.argv[1] == 'UDP':
        sock_proto = socket.SOCK_DGRAM

if sys.argv[2] != '':  # Set buffer size
    buff_size = int(sys.argv[2])

if sys.argv[3]:
    file_name = str(sys.argv[3])

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
    send_file_fd = open(os.getcwd() + '/' + file_name, 'rb')
    transfer_done_flag = ''
    if sys.argv[1] == 'TCP':
        # Send data
        print('Sending data bytes..\n')
        data = send_file_fd.read(buff_size)
        data_count = 1
        start_timestamp = datetime.datetime.now()#.replace(microsecond=0)
        while data:
            sock.send(data)
            print('Sent ', data_count * buff_size, ' bytes..')
            data = send_file_fd.read(buff_size)
            data_count += 1
        sock.shutdown(socket.SHUT_WR)
        send_file_fd.close()
        end_timestamp = datetime.datetime.now()#.replace(microsecond=0)
        print('Done sending')
        print('\nClient execution ended')
        print('\n-------------------')
        print('Client session info below:')
        print('\tFamily  :', families[sock.family])
        print('\tType    :', types[sock.type], '(' + sys.argv[1] + ')')
        print('\tProtocol:', protocols[sock.proto])
        print('\tData chunks read: ', data_count)
        print('\tData bytes read: ', data_count * buff_size)
        print('\tClient transmission time:', end_timestamp - start_timestamp)
        print('-------------------\n')
    elif sys.argv[1] == 'UDP':
        print('Sending data bytes..\n')
        data = send_file_fd.read(buff_size)
        data_count = 1
        start_timestamp = datetime.datetime.now()  # .replace(microsecond=0)
        # Send data
        while data:
            traffic_sent = sock.sendto(data, server_address)
            while traffic_sent < buff_size and len(data) == buff_size:
                traffic_sent = sock.sendto(data, server_address)
            print('Sent ', data_count * buff_size, ' bytes..')
            data = send_file_fd.read(buff_size)
            data_count += 1
        send_file_fd.close()
        transfer_done_flag = 'done'
        traffic_sent = sock.sendto(transfer_done_flag.encode('ISO-8859-1'), server_address)
        end_timestamp = datetime.datetime.now()  # .replace(microsecond=0)
        print('Done sending')
        print('\nClient execution ended')
        print('\n-------------------')
        print('Client session info below:')
        print('\tFamily  :', families[sock.family])
        print('\tType    :', types[sock.type], '(' + sys.argv[1] + ')')
        print('\tProtocol:', protocols[sock.proto])
        print('\tData chunks read: ', data_count)
        print('\tData bytes read: ', data_count * buff_size)
        print('\tClient transmission time:', end_timestamp - start_timestamp)
        print('-------------------\n')
finally:
    print('closing socket')
    sock.close()
