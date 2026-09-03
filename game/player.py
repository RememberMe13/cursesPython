class Player:
    __hp = 100
    __gold = 0
        
    def __init__(self, name):
        self.name = name

    def getHP(self):
        return self.__hp
    
    def getGold(self):
        return self.__gold
    
    def hurt(self, amount):
        self.__hp -= amount

    def heal(self, amount):
        self.__hp += amount

    def gainGold(self, amount):
        self.__gold += amount

    def spendGold(self, amount):
        self.__gold -= amount

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
