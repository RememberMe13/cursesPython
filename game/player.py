class Player:
    __hp = 100
    __gold = 0
        
    def __init__(self, name):
        self.name = name

    def getHP(self):
        return self.__hp
    
    def getGold(self):
        return self.__gold
    
    def getName(self):
        return self.name

    def hurt(self, amount):
        self.__hp -= amount

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
