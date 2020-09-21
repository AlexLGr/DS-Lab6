import socket
import sys
import os
import tqdm

# Creating a socket
sock = socket.socket()
SEPARATOR = "<SEPARATOR>"

# How many bites we will send before updating the progress
chunks = 512

# Obtaining command line arguments 
filename, host, port = sys.argv[1:4]
size = os.path.getsize(filename)

# Establishing the connection
sock.connect((host, int(port)))

# Encoding and sending the info about the file
sock.send(f"{filename}{SEPARATOR}{size}".encode())

# Creating a progress bar 
progress_bar = tqdm.tqdm(range(size),
                         f"File {filename}: sending ...",
                         unit_scale=True,
                         unit_divisor=chunks)

# Reading the specified amount of data from the file
f = open(filename, 'rb')
data = f.read(chunks)

# Updating the progress bar every time we send 512 bytes
for i in progress_bar:
    sock.send(data)
    data = f.read(chunks)
    progress_bar.update(len(data))

# Closing the file and connection
f.close()
sock.shutdown(socket.SHUT_WR)
sock.close()
