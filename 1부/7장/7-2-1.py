def RaiseErrorFunc():
    raise NameError

try:
    RaiseErrorFunc()
except:
    print("NameError is Catched")