from database import db, Tables
from config import IP, PORT, HEADERSIZE
from user import User
import pickle
import console
import threading
import socket


class Server:
    def __init__(self):
        self.console = console.Console()
        self.users = []
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
            new_user = User(connection, address)
            self.user.append(new_user)
            self.console.log(f"New connection with {new_user}")

            # start a thread for this user
            new_thread = threading.Thread(target=self.user_connection, args=(new_user, ))
            self.threads.append(new_thread)
            new_thread.daemon = True
            new_thread.start()

    def user_connection(self, user):
        new_data = True
        new = b""

        while True:
            try:
                data = user.connection.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                self.console.log(f"Lost connection with {user}", negative=True)
                self.users.remove(user)
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

                self.handle_data(full_data, user)
                full_data = b""

    def handle_data(self, data, user):
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

def main():
    server = Server()
    server.start()
