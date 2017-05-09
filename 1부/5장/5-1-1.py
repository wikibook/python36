str = "NOT Class Member"
class GString:
    str = ""
    def Set(self, msg):
        self.str = msg
    def Print(self):
        print(str)

g = GString()
g.Set("First Message")
g.Print()