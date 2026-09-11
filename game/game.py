import curses
import hashlib
import random
from curses.textpad import Textbox
from time import sleep

from game.enemy import *
from game import artAscii

# Makes it easier to show text
def wdwPrint(window, msg, refresh="yes", y=0, x=0):
    if refresh == "yes":
        window.erase()
    window.addstr(y, x, msg)
    window.refresh()

# shows in the bottom right corner
def keyToCont(window):
    sleep(0.5)
    y, x = window.getmaxyx()
    window.addstr(y - 1, x - 27, "Press anything to continue")
    window.getch()

# shows the updated attributes after each fight
def calcAttrs(player, window):
    window.erase()
    window.addstr(0, 0, "Player: " + player.name)
    window.addstr(1, 0, "HP: " + str(player.getHP()))
    window.addstr(2, 0, "Gold: " + str(player.getGold()))

    y, x = window.getmaxyx()
    window.addstr(y - 14, x - 23, artAscii.face)
    window.refresh()

# updates the enemys health
def calcEnemy(enemy, window):
    #y, x = window.getmaxyx()
    window.erase()
    window.addstr(0, 0, "HP: " + str(enemy.getHP()))
    window.addstr(0, 12, "Health bar [||||||||]")
    window.refresh()

# makes it easier to get input
def getInput(nLines, nCols, startY, startX):
    win1 = curses.newwin(nLines, nCols, startY, startX)
    win1.bkgd(' ', curses.color_pair(3))
    box = Textbox(win1)

    box.edit()
    text = box.gather().strip().lower()
    return text

# self-explanatory
def fight(enemy, player, msg, side, art, enemyAttrs):
    aY, aX = art.getmaxyx()

    # define picture
    pic = getattr(artAscii, enemy.artName)
    artLines = pic.splitlines()

    # height and width of artwork
    asciHeight = len(artLines)
    asciWidth = max((len(line) for line in artLines), default = 0)

    # To center the artwork
    startY = max(0, (aY - asciHeight) // 2)
    startX = max(0, (aX - asciWidth) // 2)

    art.erase()

    # Instead of printing the artwork in one go (would wrap around to the start of the window)
    # prints the lines one-by-one so i can controll the x coords
    for offset, line in enumerate(artLines):
        y = startY + offset
        x = startX
        art.addstr(y, x, line)

    art.refresh()

    # Show stats
    calcEnemy(enemy, enemyAttrs)

    wdwPrint(msg, f"You are fighting {enemy.name}")
    sleep(1)
    
    golds = [] # will get 10 minus the distance from correct answer and add it here, and add the sum at the end

    # Actual fight loop
    while True:
        wdwPrint(msg, random.choice(enemy.quotes))

        rNum = random.randint(1, 10)
        pNum = ""
        eNum = random.randint(1, 10)
        sleep(1.5)
        
        # Loop to get the number
        while True:
            wdwPrint(msg, "Pick a whole number from 1 - 10: ")
            wdwPrint(msg, "-> ", "no", 2)
            pNum = getInput(1, 3, curses.LINES - 4, 5)
            try:
                pNum = int(pNum)
            except (ValueError, TypeError):
                wdwPrint(msg, "Please enter a number!")
                sleep(2)
                continue

            if pNum < 1 or pNum > 10:
                wdwPrint(msg, "Number outside 1-10!")
                sleep(2)
                continue
            break
        
        # Define the distance you were away from the actual number
        pDist = abs(rNum - pNum)
        eDist = abs(rNum - eNum)

        # Finds out if the enemy or player was closer to the random number
        if pDist < eDist:
            wdwPrint(msg, f"You were closer: {pDist} away vs {eDist} away")
            enemy.hurt(eDist * 10)
            calcEnemy(enemy, enemyAttrs)
            golds.append(10 - pDist)
            keyToCont(msg)
        elif pDist == eDist:
            wdwPrint(msg, f"Tie: {pDist} away vs {eDist} away")
            keyToCont(msg)
        else:
            wdwPrint(msg, f"Enemy was closer: {eDist} away vs {pDist} away")
            player.hurt(pDist)
            calcAttrs(player, side)
            keyToCont(msg)

        # check if player or enemy is dead
        if player.getHP() <= 0:
            wdwPrint(msg, "YOU HAVE DIED!!!")
            keyToCont(msg)
            break
        elif enemy.getHP() <= 0:
            wdwPrint(msg, "Zabito Boga! (enemy felled)")
            sleep(1)
            break
    
    # dont add gold if dead
    if player.getHP() <= 0:
        return False

    player.gainGold(sum(golds))
    wdwPrint(msg, f"Added {sum(golds)} gold!")
    calcAttrs(player, side)
    keyToCont(msg)

    art.erase()
    msg.erase()
    art.refresh()
    msg.refresh()
    return True

def game(player, msg, side, art, enemyAttrs, stdscr):
    #Default sleep time
    ds = 1.5

    #choices are here for easier looking back at
    choice1 = "" # tech / math
    choice2 = "" # yes / no
    choice3 = 0  # 1-4
    choice4 = "" # science / english
    choice5 = "" # yes / no
    choice6 = 0 # 1-3 only for neutral ending

    #Enemys name, name of art, name of quotes, hp
    ant = Enemy("Big Ant", "ant", antQuotes, 20)
    gabe = Enemy("Gabe Newell", "gabe", gabeQuotes, 20)
    wire = Enemy("Live Wire", "wire", wireQuotes, 20)
    math = Enemy("Well known math teacher", "math", mathQuotes, 20)
    protractor = Enemy("Angry Protractor", "protractor", protractorQuotes, 20)
    gold = Enemy("Giant Gold Monster", "gold", goldQuotes, 20)
    puddle = Enemy("Puddle Monster", "puddle", puddleQuotes, 20)
    book = Enemy("Dan Gookins Guide to Ncurses Programming", "book", bookQuotes, 20)
    english = Enemy("Old English Teacher", "english", englishQuotes, 20)

    #Set backgrounds
    art.bkgd(' ', curses.color_pair(2))
    msg.bkgd(' ', curses.color_pair(3))
    side.bkgd(' ', curses.color_pair(1))
    enemyAttrs.bkgd(' ', curses.color_pair(2))
    art.refresh()

    #set up side panel
    calcAttrs(player, side)

    # ---------START INTRO----------- 
    wdwPrint(msg, "You arrived at school on a chilly, windy morning.")
    sleep(ds)
    wdwPrint(msg, "you hadn't slept too well last night, too much Math homework.", "no", 1)
    sleep(ds)
    wdwPrint(msg, "As you step up the ramp leading into the school, you see…", "no", 2)
    keyToCont(msg)
   
    wdwPrint(msg, "The squished remains of an ant you had accidentally stepped on.")
    sleep(ds)
    wdwPrint(msg, "And then out of nowhere a giant bull ant appered and challenged you to a fight!", "no", 1)
    keyToCont(msg)


    # -----------START FIRST FIGHT------------
    
    # if dead returns to the main.py file to show the death screen
    if not fight(ant, player, msg, side, art, enemyAttrs):
        return False
    
    # get choice1
    while True:
        wdwPrint(msg, "Where do you want to head to next? tech or math")
        wdwPrint(msg, "-> ", "no", 1)
        choice1 = getInput(1, 5, curses.LINES - 5, 5) 

        if choice1 == "tech" or choice1 == "math":
            wdwPrint(msg, f"You chose {choice1}")
            break
        else:
            wdwPrint(msg, "Please enter tech or math!")
            sleep(ds)
    
    if choice1 == "tech":
        while True:
            wdwPrint(msg, "As you walk into the technology classrooms you see a 32gb stick of ddr5 ram on a table.")
            sleep(ds)
            wdwPrint(msg, "There is no one around.", "no", 1)
            sleep(ds)
            wdwPrint(msg, "Do you take the ram? yes/no", "no", 2)
            wdwPrint(msg, "->", "no", 3)

            choice2 = getInput(1, 4, curses.LINES - 3, 5)
            if choice2 == "yes" or choice2 == "no":
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice2 == "yes":
            player.gainGold(600)
            calcAttrs(player, side)
            wdwPrint(msg, "As you put the valuable sand into your pocket Gabe Newell jumps up and scares you!")
            keyToCont(msg)

            if not fight(gabe, player, msg, side, art, enemyAttrs):
                return False
            
            wdwPrint(msg, "As you leave the scene of the fight, Gabe runs past and nicks one of the sticks!")
            player.spendGold(300)
            calcAttrs(player, side)
            keyToCont(msg)

        elif choice2 == "no":
            wdwPrint(msg, "As you walk away from the expensive sand you accidentally touch a live wire!")
            player.hurt(5)
            calcAttrs(player, side)
            keyToCont(msg)

            if not fight(wire, player, msg, side, art, enemyAttrs):
                return False

    elif choice1 == "math":
        while True:
            wdwPrint(msg, "As you reminece about your CASIO FX-1AU graphing calculator you spot one unatended\n on a table!")
            sleep(ds)
            wdwPrint(msg, "Do you take the $270 calculator? yes/no", "no", 2)
            wdwPrint(msg, "->", "no", 3)
            choice2 = getInput(1, 4, curses.LINES - 3, 5)
            if choice2 == "yes" or choice2 == "no":
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice2 == "yes":
            player.gainGold(270)
            calcAttrs(player, side)
            wdwPrint(msg, "As you put the overpriced computer in your pocket an angry Math teacher approaches!")
            keyToCont(msg)

            if not fight(math, player, msg, side, art, enemyAttrs):
                return False

        elif choice2 == "no":
            wdwPrint(msg, "As you walk away from the calc (short for calculator) you step on an upturned protractor!")
            player.hurt(5)
            calcAttrs(player, side)
            keyToCont(msg)

            if not fight(protractor, player, msg, side, art, enemyAttrs):
                return False

    # Food loop
    while True:
        wdwPrint(msg, "After all that effort you feel hungry.")
        sleep(ds)
        wdwPrint(msg, "Food options available at the canteen:", "no", 0, 39)
        sleep(ds)
        wdwPrint(msg, "1. Sandwich (20hp) --------------------------- $20", "no", 1, 0)
        wdwPrint(msg, "2. Noodles (10hp) ---------------------------- $10", "no", 2, 0)
        wdwPrint(msg, "3. Potato Wedges with Sour Cream (20hp) ------ $20", "no", 3, 0)
        wdwPrint(msg, "4. Sauce packet (1hp) ------------------------ $5", "no", 4, 0)

        wdwPrint(msg, "choice:", "no", 3, 55)
        choice3 = getInput(1, 2, curses.LINES - 3, 65)

        # Input validation
        try:
            if choice3 == "":
                wdwPrint(msg, "Please enter a number!")
                sleep(ds)
                continue
            choice3 = int(choice3)
        except ValueError:
            wdwPrint(msg, "Please enter a number!")
            sleep(ds)
            continue

        if choice3 in [1, 2, 3, 4]:
            break
        else:
            wdwPrint(msg, "Please enter a number from 1 to 4!")
            sleep(ds)

    match choice3:
        case 1:
            wdwPrint(msg, "You enjoy a fish sandwich.")
            player.spendGold(20)
            player.heal(20)
            calcAttrs(player, side)
        case 2:
            wdwPrint(msg, "You slurp up the noodle")
            player.spendGold(10)
            player.heal(10)
            calcAttrs(player, side)
        case 3:
            wdwPrint(msg, "Yummy potato wedges.")
            player.spendGold(20)
            player.heal(20)
            calcAttrs(player, side)

        case 4:
            wdwPrint(msg, "sorse")
            player.spendGold(5)
            sleep(ds)
            wdwPrint(msg, "Gained 300 gold!", "no", 1)
            player.gainGold(300)
            calcAttrs(player, side)
   
    keyToCont(msg)

    # -----------SCIENCE OR ENGLISH------------- 
    while True:
        wdwPrint(msg, "After consuming some nutrition you walk to the next place.")
        sleep(ds)
        wdwPrint(msg, "Science or English?", "no", 1)
        sleep(ds)
        wdwPrint(msg, "-> ", "no", 2)
        choice4 = getInput(1, 8, curses.LINES - 4, 5) 

        if choice4 == "science" or choice4 == "english":
            break
        else:
            wdwPrint(msg, "Please enter science or english!")
            sleep(ds)
    
    if choice4 == "science":
        while True:
            wdwPrint(msg, "After walking into the science classroom you see a test tube full of a golden liquid.")
            sleep(ds)
            wdwPrint(msg, "It shimmers in the light", "no", 1)
            sleep(ds)
            wdwPrint(msg, "Drink it? yes/no", "no", 2)
            wdwPrint(msg, "->", "no", 3)
            choice5 = getInput(1, 4, curses.LINES - 3, 5)

            if choice5 == "yes" or choice5 == "no":
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice5 == "yes":
            wdwPrint(msg, "Walking back outside, you trip and land in a suspiciously shiny puddle!")
            sleep(ds)
            wdwPrint(msg, "The puddle opens up into a portal to a gold dimension!", "no", 1)
            sleep(ds)
            wdwPrint(msg, "When you exit the portal, a giant gold slime thing attacks!", "no", 2)
            keyToCont(msg)

            if not fight(gold, player, msg, side, art, enemyAttrs):
                return False

        elif choice5 == "no":
            wdwPrint(msg, "Walking back outside, you trip and land in a puddle of water.")
            sleep(ds)
            wdwPrint(msg, "This angers the puddle and it attacks!", "no", 1)
            keyToCont(msg)

            if not fight(puddle, player, msg, side, art, enemyAttrs):
                return False

    elif choice4 == "english":
        while True:
            wdwPrint(msg, "As you enter the english classroom, you spy a musty old book resting on a table.")
            sleep(ds)
            wdwPrint(msg, "On the title it says \"Dan Gookins Guide to Ncurses Programming\"", "no", 1)
            sleep(ds)
            wdwPrint(msg, "Read it? yes/no", "no", 2)
            wdwPrint(msg, "->", "no", 3)

            choice5 = getInput(1, 4, curses.LINES - 3, 5)
            if choice5 == "yes" or choice5 == "no":
                wdwPrint(msg, f"you chose {choice5}")
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice5 == "yes":
            wdwPrint(msg, "The book comes alive! It shouts \"stcscr.clear()\" at you!")
            keyToCont(msg)

            if not fight(book, player, msg, side, art, enemyAttrs):
                return False
        elif choice5 == "no":
            wdwPrint(msg, "An old english teacher bursts out of the side door!")
            sleep(ds)
            wdwPrint(msg, "WHY DID YOU NOT ENRICH YOUR MIND!?", "no", 1)
            keyToCont(msg)

            if not fight(english, player, msg, side, art, enemyAttrs):
                return False

    # ----------ENDING----------------
    if choice1 == "tech" and choice4 == "english": # "good" ending
        wdwPrint(msg, "The clocktower rings thrice, signalling the end of school hours.")
        sleep(ds)
        wdwPrint(msg, "The walk home is arduous and the sun blinds you", "no", 1)
        sleep(ds)
        wdwPrint(msg, "As you cross through the reserve, you spot an owl in the crook of a gumtree")
        sleep(ds)
        wdwPrint(msg, "This is the first time in years that you have seen an owl.")
        keyToCont(msg)

        wdwPrint(msg, "As you pass it, the bird hoots, and flies away")
        sleep(ds)
        wdwPrint(msg, "It was a good day", "no", 1)
        keyToCont(msg)

    elif choice1 == "math" and choice4 == "science": # "bad" ending
        wdwPrint(msg, "You look at your watch and realise it is time to head home")
        sleep(ds)
        wdwPrint(msg, "As you approach the intersection, the sun blinds you for a moment.", "no", 1)
        sleep(ds)
        wdwPrint(msg, "The green man starts walking, and you cross the road", "no", 2)
        keyToCont(msg)

        wdwPrint(msg, "Halfway across, you hear the screeching of brakes as a truck fails to stop before the lights.")
        sleep(ds)
        wdwPrint(msg, "Distracted by the commotion, an unaware driver turns the corner where you have right of way is about to run you over!", "no", 1)

        # fight the truck, it has a lot of health

    else:
        while True: # "neutral" ending
            wdwPrint(msg, "After the last fight of the day, you decide to get a drink from the asian mart")
            sleep(ds)
            wdwPrint(msg, "What would you like?", "no", 1)
            wdwPrint(msg, "1. Soy bean drink", "no", 2)
            wdwPrint(msg, "2. Guyabano nectar", "no", 1)
            wdwPrint(msg, "3. Sour plum tea", "no", 3)
            wdwPrint(msg, "->", "no", 4)
            choice6 = getInput(1, 2, curses.LINES - 2, 5)
            
            if choice6 == "":
                wdwPrint(msg, "Please enter a number!")
                sleep(ds)
                continue
            try:
                choice6 = int(choice6)
            except ValueError:
                wdwPrint(msg, "Please enter a number!")
                sleep(ds)
                continue
            
            if choice6 in [1, 2, 3]:
                break
            else:
                wdwPrint(msg, "Please enter a number from 1 to 3!")
        
        match choice6:
            case 1:
                wdwPrint(msg, "It tastes nice.")
                sleep(ds)
                wdwPrint(msg, "+5 hp", "no", 1)
                player.heal(5)
                keyToCont(msg)
            case 2:
                wdwPrint(msg, "Very sweet.")
                sleep(ds)
                wdwPrint(msg, "+10 hp", "no", 1)
                keyToCont(msg)
            case 3:
                wdwPrint(msg, "The shopkeeper says they are all out of plum tea.")
                sleep(ds)
                wdwPrint(msg, "\"I think the store down the road has some in stock\"", "no", 1)
                sleep(ds)
                wdwPrint(msg, "You say \"Do you know who you are talking to?\" and chinned the bloke right then and there", "no", 2)
                keyToCont(msg)

                shop = Enemy("Angry Shopkeeper", "math", shopQuotes, 30)
                if not fight(shop, player, msg, side, art, enemyAttrs):
                    return False


    
    # if no file make file
    try:
        open("scores.txt", "r").close()
    except FileNotFoundError:
        open("scores.txt", "w").close()
    
    with open("scores.txt", "a") as f:
        n = player.name
        player.score = str(player.getGold() + player.getHP())

        # create hash
        h = hashlib.sha512(n.encode("utf-8") + player.score.encode("utf-8")).hexdigest()[:10]
        f.write(f"{n}:{player.score}:{h}\n")
    
    # True means not dead
    return True

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
