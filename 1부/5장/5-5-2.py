class GString:
    def __init__(self, init=None):
        self.content = init

    def __sub__(self, str):
        print("- opreator is called!")

    def __isub__(self, str):
        print("-= opreator is called!")

g = GString("aBcdef")
g - "a"
g -= "a"
