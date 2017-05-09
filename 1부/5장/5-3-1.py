class CounterManager:
    insCount = 0
    def __init__(self):
        CounterManager.insCount += 1
    def printInstaceCount():
        print("Instance Count: ", CounterManager.insCount)

a, b, c = CounterManager(), CounterManager(), CounterManager()
CounterManager.printInstaceCount()
b.printInstaceCount()