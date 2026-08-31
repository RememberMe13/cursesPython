class Player:
    __hp = 100
    __gold = 0
        
    def __init__(self, name):
        self.name = name

    def getHP(self):
        return self.__hp
    
    def getGold(self):
        return self.__gold
