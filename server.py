import gc
import pickle
import dill
import socket
import sys
import time
import _thread


# Command line arguments
if '-h' in sys.argv or '--help' in sys.argv:
    print('-m || --main      : Destination to main.py file. Required.')
    print('-f || --functions : Destination to functions.py file. Required.')
    print('-d || --debug     : Debug mode')
    print('Full documentation at GITHUB LINK')
    exit()

if '-m' in sys.argv:
    main_file = sys.argv[sys.argv.index('-m') + 1]
elif '--main' in sys.argv:
    main_file = sys.argv[sys.argv.index('--main') + 1]
else:
    print('Invalid arguments.  Type -h or --help for further help.')
    exit()

if '-f' in sys.argv:
    function_file = sys.argv[sys.argv.index('-f') + 1]
elif '--functions' in sys.argv:
    function_file = sys.argv[sys.argv.index('--functions') + 1]
else:
    print('Invalid arguments.  Type -h or --help for further help.')
    exit()

if '-d' in sys.argv or '--debug' in sys.argv:
    debug = True
else:
    debug = False

if main_file[-3:] != '.py' or function_file[-3:] != '.py':
    print("'main' and 'functions' must be *.py files")
    exit()

main = __import__(main_file.replace('.py', ''))

# Make sure main is properly setup
try:
    main.generate_function
    main.handle_received
    main.PORT
except NameError:
    print("'generate_function' or 'handle_received' is not defined in {}.\
        Read full documentation at GITHUB LINK".format(main_file))
    exit()

# Get IP and port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
s.close()
PORT = main.PORT

# Create socket and start server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

sock.listen()
print('Server Started on port', PORT)

# For every client connected...
def threaded_client(conn, addr, user_id):
    # Send definitions and file name
    with open(function_file, 'rb') as f:
        file = f.read()
        f.close()
    if debug:
        print('Sending file to', addr)
    conn.send(file + b'*L_?*')
    # Sleep to make sure client has caught up
    time.sleep(1)
    if debug:
        print('Sending file name to', addr)
    conn.send(function_file.encode() + b'*L_?*')
    time.sleep(1)
    while True:
        # Gets function, inputs, and name to client
        if debug:
            print('Sending Function to', addr)
        process_data = main.generate_function(user_id)
        if len(process_data) != 3:
            print('Function data generated incorrectly. Expected a tuple of\
            length 3, received a tuple of length {}'.format(len(process_data)))
            exit()
        data = pickle.dumps(process_data)
        conn.send(data + b'*L_?*')
        # Receives output as 'y'
        while True:
            try:
                if debug:
                    print('Receiving from', addr)
                data = []
                received = 0
                while True:
                    packet = conn.recv(1024)
                    replaced = packet.replace(b'*L_?*', b'')
                    received += len(replaced)
                    if packet:
                        data.append(replaced)
                    # Terminates on null packet or close message '*L_?*'
                    if not packet or packet == b'' or b'*L_?*' in packet:
                        break
                data = b"".join(data)
                if debug:
                    print('SIZE:', len(data))
                y = pickle.loads(data)
                break
            except (EOFError, pickle.UnpicklingError) as e:
                print(e, type(e))
                print(addr)
                raise Exception(e)

        # Do whatever with data
        if debug:
            print('Received output', addr)
        main.handle_received(y, user_id)
        # Garbage collect
        gc.collect()
    # Handles connection loss
    print('Lost Connection from', addr)
    conn.close()

# Connect new users forever
user_id = 0
while True:
    conn, addr = sock.accept()
    print('New Connection From: ', addr)
    _thread.start_new_thread(threaded_client, (conn, addr, user_id))
    user_id += 1
