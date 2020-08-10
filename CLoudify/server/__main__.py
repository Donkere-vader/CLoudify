from database import db, Tables
from config import IP, PORT, HEADERSIZE
from connection import Connection
from sendobject import sendObject
import pickle
import console
import threading
import socket


class Server:
    def __init__(self):
        self.console = console.Console()
        self.connections = []
        self.threads = []

    def handle_connections(self):
        pass

    def start(self):
        self.console.log("Starting server...")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((IP, PORT))
        self.sock.listen(5)

        self.console.log(f"Server online @ ({socket.gethostbyname(socket.gethostname())}, {PORT})")

        # listen for connection attempts

        while True:
            connection, address = self.sock.accept()
            new_connection = Connection(connection, address)
            self.connections.append(new_connection)
            self.console.log(f"New connection with {new_connection}")

            # start a thread for this user
            new_thread = threading.Thread(target=self.user_connection, args=(new_connection, ))
            self.threads.append(new_thread)
            new_thread.daemon = True
            new_thread.start()

    def user_connection(self, connection):
        new_data = True
        new = b""

        while True:
            try:
                data = connection.connection.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                self.console.log(f"Lost connection with {connection}", negative=True)
                self.connections.remove(connection)
                return

            if data == b"":
                continue

            if new_data:
                new_data = False
                full_data = b""

                data = new + data

                new = b""
                data_len = int(data[:HEADERSIZE].decode("utf-8"))
                full_data += data[HEADERSIZE:]
            else:
                full_data += data

            if len(full_data) >= data_len:
                new_data = True

                new = full_data[data_len:]
                full_data = full_data[:data_len]

                self.handle_data(full_data, connection)
                full_data = b""

    def handle_data(self, data, connection):
        _tries = 0
        while True:
            _tries += 1
            try:
                data = pickle.loads(data)
                break
            except pickle.UnpicklingError as e:
                if _tries == 10:
                    self.console.log(f"Failed to load data Error: {e}", negative=True)
                    return
                self.console.log(f"Error {e} while loading data.. trying again ", negative=True)

        # check for data type
        if data.type == 'file_req':
            # file request
            pass
        elif data.type == 'error':
            self.console.log(data.error, negative=True)
        elif data.type == 'login':  # user tries to log in
            self.console.log(f"Login attempt from {connection}")
            user = Tables.User.select(username=data.username)

            console.log(f"user: {user}")

            if not user:
                self.send("authfail", connection)

    def send(self, _type, connection, **kwargs):
        data = sendObject(
            _type,
            **kwargs
        )

        bData = pickle.dumps(data)

        header = bytes(str(len(bData)).ljust(HEADERSIZE), "utf-8")
        full_bData = header + bData

        self.connection.send(full_bData)

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
