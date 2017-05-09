class Animal:
    def __init__(self):
        print("Animal __init__()")

class Tiger(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Tiger __init__()")

class Lion(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Lion __init__()")

class Liger(Tiger, Lion):
    def __init__(self):
        Tiger.__init__(self)
        Lion.__init__(self)
        print("Liger __init__()")