import socket
import sys


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
if sys.argv[1]:
    if sys.argv[1] == 'TCP':
        sock_proto = socket.SOCK_STREAM
    elif sys.argv[1] == 'UDP':
        sock_proto = socket.SOCK_DGRAM

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

print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print('Client socket info:', sock)

message = b'This is the message.  It will be repeated.'

try:
    if sys.argv[1] == 'TCP':
        # Send data
        print('sending {!r}'.format(message))
        sock.send(message)

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))
    elif sys.argv[1] == 'UDP':
        # Send data
        print('sending {!r}'.format(message))
        sent = sock.sendto(message, server_address)

        # Receive response
        print('waiting to receive')
        data, server = sock.recvfrom(4096)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
