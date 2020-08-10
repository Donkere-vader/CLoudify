import os
from file import File
from config import IP, PORT, AUTH_KEY, SYNC_FOLDER, HEADERSIZE
from sendobject import sendObject
import socket
import pickle
import getpass

class Client:
    def __init__(self):
        self.files: list
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Starting...")
        self.index()
        self.start()

    def getListOfFiles(self, dirName):
        listOfFile = os.listdir(dirName)
        allFiles = list()

        for entry in listOfFile:
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    def index(self):
        print("[+] Scanning")
        self.files = []
        file_names = self.getListOfFiles(SYNC_FOLDER)
        for file_name in file_names:
            self.files.append(File(file_name))

    def start(self):
        self.sock.connect((IP, PORT))

        self.authenticate()

        self.server_connection()

    def server_connection(self):
        new_data = True
        new = b""

        while True:
            data = self.sock.recv(1024)

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

                self.handle_data(full_data)
                full_data = b""

    def handle_data(self, data):
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
        elif data.type == 'authfail':
            print("[!] Either the autkey expired or you provided the wrong login details.")
            self.login()

    def send(self, _type, **kwargs):
        data = sendObject(
            _type,
            **kwargs
        )

        bData = pickle.dumps(data)

        header = bytes(str(len(bData)).ljust(HEADERSIZE), "utf-8")
        full_bData = header + bData

        self.sock.send(full_bData)

    def authenticate(self):
        if AUTH_KEY is not None:
            self.send("auth", auth_key=AUTH_KEY)  # auth is short for authentication
        else:
            self.login()

    def login(self):
        print("[+] Please log in to the server")
        self.send("login", username=input("[?] Username:"), password=getpass.getpass("[?] Password:"))
        print("Atempting login...")

def main():
    client = Client()

if __name__ == "__main__":
    main()
