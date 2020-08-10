class sendObject:
    def __init__(self, _type, **kwargs):
        self.type = _type

        for v in kwargs:
            exec(f"self.{v} = {kwargs[v]}")
