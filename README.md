# wireless-supercomputer v0.2
Connecting local computers to compute a problem.
This program allows you to send functions to other computers on a local network and receive the computed output.

# Documentation
1. Specify `PORT` in `main.py` to tell the server what port to run the program on.
2. Write `functions.py` which will include all the functions that could possibly be executed on the client.
3. Write `generate_function(user_id)` in `main.py` which will return 3 values: 
    1. the function itself
    2. a dictionary or tuple of the inputs to the function
    3. the name of the function
4. Write `handle_received(received, user_id)` to specify what to do with the incoming data the client computed
5. Make sure that the client has all the dependencies installed, or make a function in `functions.py` to install them.
6. Run the server with `python3 server.py -m main.py -f functions.py`
7. Run the client with `python3 client.py SERVER_IP PORT`

For help with running `server.py` or `client.py` run `python3 server.py -h` or `python3 client.py -h` respectively.

For a basic example, see `example_functions.py` and `example_main.py`.  More complicated examples using Tensorflow and Keras will be added soon.

#### Disclaimer
This program is in alpha and still greatly under development, so expect bugs.  This is not to be used on a public network nor is any developer of this program responsible for damage or information leaked because of this program.  You must be extremely careful when using this program with Tensorflow or Keras with a Tensorflow backend, as graphs become very tricky to manage.

#### TODO:
Add examples using Keras and/or Tensorflow.  Add on_connect and on_disconnect function.
