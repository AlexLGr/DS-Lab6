import os
from os import walk
import socket
from threading import Thread

# Port opened for TCP connections
port = 6666
SEPARATOR = "<SEPARATOR>"

# Dictionary for checking if copies of files exist
filesystem = {}


# Class implementing the threading approach
class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock

    def _close(self):
        self.sock.close()
        print(self.name + ' ' + 'conection closed')

    def run(self):
        global filesystem

        # Receiving data about the file
        data = self.sock.recv(512).decode()
        filename, size = data.split(SEPARATOR)

        # Checking if the file with the same name already exists
        keys = filesystem.keys()
        if filename in keys:
            name, ext = os.path.splitext(filename)
            filesystem[filename] += 1
            filename = f"{name}_copy{filesystem[filename]}{ext}"
        else:
            filesystem[filename] = 1

        # Receiving the file in chunks
        with open(filename, "wb") as f:
            read = True
            while read:
                read = self.sock.recv(512)
                if not read:
                    break
            f.write(read)
        f.close()
        self._close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Specifying the port that listens to the connections
    sock.bind((" ", port))
    sock.listen(2)
    while True:
        connection, address = sock.accept()
        ClientListener(address).start()


if __name__ == "__main__":
    main()
