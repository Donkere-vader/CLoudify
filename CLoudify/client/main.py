import os
from file import File
from config import IP, PORT, AUTH_KEY, SYNC_FOLDER

class Client:
    def __init__(self):
        self.files: list

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
        self.files = []
        file_names = self.getListOfFiles(SYNC_FOLDER)
        for file_name in file_names:
            self.files.append(File(file_name))


def main():
    client = Client()
    client.index()

    for f in client.files:
        print(f)