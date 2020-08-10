class Connection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.authenticated = False
        self.user = None

    def __repr__(self):
        return f"<Connection from {self.address}>"
