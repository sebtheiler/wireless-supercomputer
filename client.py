import gc
import pickle
import select
import socket
import sys
import time


# Command line arguments
if '-h' in sys.argv or '--help' in sys.argv:
    print('Usage: python3 client.py IP PORT')
    print('Example: python3 client.py 192.168.1.8 7777')
    print('Full documentation at GITHUB LINK')
    exit()

try:
    IP = sys.argv[1]
    try:
        int(IP)
        print('Must specify IP, then port.  Use -h or --help for help.')
        exit()
    except Exception:
        pass
except Exception:
    print('Must specify IP and port values.  Use -h or --help for help.')
    exit()


try:
    port = int(sys.argv[2])
    if 65536 > port > 1023:
        PORT = port
    else:
        print('Port value must be no less than 1024 and no greater than 65535.')
        exit()
except Exception:
    print('Must specify port value.  Use -h or --help for help.')
    exit()


class Connection:
    def __init__(self, server_ip, port, debug=False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = port
        self.addr = (self.server, self.port)
        self.debug = debug
        self._connect()

        self.output = None
    
    def _connect(self):
        self.client.connect(self.addr)
        # Get functions file
        print('Getting definitions file')
        data = []
        while True:
            packet = self.client.recv(1024)
            replaced = packet.replace(b'*L_?*', b'')
            if packet:
                data.append(replaced)
            if not packet or packet == b'' or b'*L_?*' in packet:
                break
        file = b"".join(data)

        # Get name of functions file
        if self.debug:
            print('Getting file name')
        data = []
        while True:
            packet = self.client.recv(1024)
            replaced = packet.replace(b'*L_?*', b'')
            if packet:
                data.append(replaced)
            if not packet or packet == b'' or b'*L_?*' in packet:
                break
        filename = b"".join(data)

        # Write functions file
        if self.debug:
            print(filename)
        with open(filename, 'w+b') as f:
            f.write(file)
    
    
    def new(self):
        print('Receiving...')
        data = []
        while True:
            packet = self.client.recv(1024)
            replaced = packet.replace(b'*L_?*', b'')
            if packet:
                data.append(replaced)
            if b'*L_?*' in packet: # not packet or packet == b'' or 
                break
        data = b"".join(data)

        if not data:
            print('Error Receiving Data')
            print(data)
            exit()

        if self.debug:
            print('Deserializing...')
        func, x, name = pickle.loads(data)

        if self.debug:
            print('Evaluating', name, 'on', x)
        if isinstance(x, tuple) or isinstance(x, list):
            self.output = func(*x)
        elif isinstance(x, dict):
            self.output = func(**x)
        else:
            print('Unexpected type of input', x, type(x))
            exit()
        msg = pickle.dumps(self.output)
        if self.debug:
            print(msg, self.output)
            print('SIZE: ', len(msg))
        print('Sending...')
        self.client.send(msg + b'*L_?*')

        gc.collect()
        return self.output


c = Connection(IP, PORT)
while True:
    c.new()
