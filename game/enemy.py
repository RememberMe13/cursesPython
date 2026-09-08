class Enemy:
    def __init__(self, name, artName, quotes, hp):
        self.name = name
        self.artName = artName
        self.quotes = quotes
        self.__hp = hp

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
antQuotes = ("\"I'm gonna squish you!\"", "\"Better run!\"", "\"Pluh\"")
gabeQuotes = ("Prepare for your half-life to end!", "Go buy a GabeCube", "You'll be left for dead!")
wireQuotes = ("Im aLIVE and kicking!", "Go call a sparky", "Got any tape?")
mathQuotes = ("Whats 2+2?", "Don't be discriminate", "Drop and give me 20!")
protractorQuotes = ("a² + b² = c²", "You are not ACUTE-y", "Will you measure up?")
goldQuotes = ("I'm gold, I'm bold, and quite shiny I'm told", "5 bucks says I'm heavier than you", "I am worth $500,000!")
puddleQuotes = ("Are you in a muddle?", "My brother is a pool", "Prepare to be dehydrated!")
bookQuotes = ("Book uses papercut!", "Did you know: the n in Ncurses stands for new", "#!&!@?*&# (curse word)")
englishQuotes = ("Give me a 1000 word essay on the origins of a K.O!", "Where is my cardigan?", "You forgot your annotated bibliography!")
