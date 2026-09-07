class Enemy:
    def __init__(self, name, artName, quotes, hp, atk):
        self.name = name
        self.artName = artName
        self.quotes = quotes
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

# Quotes
antQuotes = ["im gonna squish you!", "Better run!", "chud"]
gabeQuotes = ["Prepare for your half-life to end!", "go buy a GabeCube", "youll be left for dead!"]
wireQuotes = ["Im aLIVE and kicking!", "go call a sparky", "got any tape?"]
mathQuotes = ["Whats 2+2?", "dont be discriminate", "drop and give me 20!"]
protractorQuotes = ["quote 1", "quote 2", "quote 3"]
scienceQuotes = ["science 1", "science 2", "science 3"]
noScienceQuotes = ["science 1", "science 2", "science 3"]
englishQuotes = ["english 1", "english 2", "english 3"]
noEnglishQuotes = ["english 1", "english 2", "english 3"]
