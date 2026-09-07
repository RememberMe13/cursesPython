class Enemy:
    def __init__(self, name, artName, hp, atk):
        self.name = name
        self.artName = artName
        self.__hp = hp
        self.__atk = atk

    def getHP(self):
        return self.__hp
    
    def hurt(self, amount):
        self.__hp -= amount

    def heal(self, amount):
        self.__hp += amount

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()

