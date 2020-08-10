class sendObject:
    def __init__(self, _type, **kwargs):
        self.type = _type

        for v in kwargs:
            if type(kwargs[v]) == str:
                exec(f"self.{v} = '{kwargs[v]}'")
            else:
                exec(f"self.{v} = {kwargs[v]}")
