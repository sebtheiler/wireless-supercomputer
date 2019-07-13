import example_functions

# Define the port for the server to use
PORT = 12345

# Store received data
data = []


# Generate a function for a user:
def generate_function(user_id):
    #       Function                        Input dict/tuple             Function name
    return (example_functions.random_sleep, {'a': 15, 'b': user_id + 3}, "random sleep")


# When output of function is computed and received...
def handle_received(received, user_id):
    print('Received output from user #{}'.format(user_id))
    data.append(received)
    print(data)

# To run:
# On server: python3 server.py -m example_main.py -f example_functions.py
# On client: python3 client.py SERVER_IP 12345
