import os
import hashlib

class File:
    def __init__(self, name):
        self.name = name
        self.mtime = os.path.getmtime(self.name)  # modified time

        with open(self.name, 'rb') as f:
            self.hash = hashlib.md5(f.read()).hexdigest()

    def __repr__(self):
        return f"<File {self.name} mtime: {self.mtime} hash: {self.hash}>"
