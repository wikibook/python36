class GString:
    def __init__(self, init=None):
        self.content = init

    def __sub__(self, str):
        for i in str:
            self.content = self.content.replace(i, '')
        return GString(self.content)

    def Remove(self, str):
        return self.__sub__(str)