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
buff_size = 512  # default buffer size - small power of 2
if sys.argv[1]:
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
server_address = (socket.gethostname(), 10001)

if sys.argv[1] == 'TCP':
    # Connect the socket to the port where the server is listening
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

try:
    send_file_fd = open(os.getcwd() + '\\client_storage\\send.mp4', 'rb')
    if sys.argv[1] == 'TCP':
        # Send data
        print('Sending data bytes..\n')
        data = send_file_fd.read(buff_size)
        data_count = 1
        print('Sent ', data_count * buff_size, ' bytes..')
        start_timestamp = datetime.datetime.now()#.replace(microsecond=0)
        while data:
            sock.send(data)
            data = send_file_fd.read(buff_size)
            data_count += 1
            print('Sent ', data_count * buff_size, ' bytes..')
        sock.shutdown(socket.SHUT_WR)
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
        # Send data
        #print('sending {!r}'.format(message))
        #sent = sock.sendto(message, server_address)

        # Receive response
        print('waiting to receive')
        data, server = sock.recvfrom(4096)
        print('received {!r}'.format(data))
    send_file_fd.close()
finally:
    print('closing socket')
    sock.close()
