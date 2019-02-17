

class Roster():
    def __init__(self, name, size):
        self.__name = str(name)
        self.__slots = int(size)
        self.__playSlots = [""] * self.__slots
        self.__waitList = [""] * (self.__slots // 2)

    