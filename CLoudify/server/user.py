class User:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

    def __repr__(self):
        return f"<User from {self.address}>"
