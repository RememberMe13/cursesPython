import curses
import hashlib
import random
from curses.textpad import Textbox
from time import sleep

from game.enemy import *
from game import artAscii


def wdwPrint(window, msg, refresh="yes", y=0, x=0):
    if refresh == "yes":
        window.erase()
    window.addstr(y, x, msg)
    window.refresh()

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

def calcEnemy(enemy, window):
    #y, x = window.getmaxyx()
    window.erase()
    window.addstr(0, 0, "HP: " + str(enemy.getHP()))
    window.addstr(0, 12, "Health bar [||||||||]")
    window.refresh()

def getInput(nLines, nCols, startY, startX):
    win1 = curses.newwin(nLines, nCols, startY, startX)
    win1.bkgd(' ', curses.color_pair(3))
    box = Textbox(win1)

    box.edit()
    text = box.gather().strip().lower()
    return text

def fight(enemy, player, msg, side, art, enemyAttrs):
    aY, _ = art.getmaxyx()
    asciHeight = getattr(artAscii, enemy.artName).count("\n") + 1
    # Print art
    wdwPrint(art, getattr(artAscii, enemy.artName), "yes", int((aY / 2) - int(asciHeight / 2)), 0)
    calcEnemy(enemy, enemyAttrs)

    wdwPrint(msg, f"You are fighting {enemy.name}")
    sleep(1)
    
    golds = [] # will get 10 - the distance and add it here, and add the sum at the end

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


        if player.getHP() <= 0:
            wdwPrint(msg, "YOU HAVE DIED!!!")
            keyToCont(msg)
            break
        elif enemy.getHP() <= 0:
            wdwPrint(msg, "Zabito Boga! (enemy felled)")
            break

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
    ds = 1

    #choices are here for easier looking back at
    choice1 = "" # tech / math
    choice2 = "" # yes / no
    choice3 = 0  # 1-4
    choice4 = "" # science / english
    choice5 = "" # yes / no

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

    if not fight(ant, player, msg, side, art, enemyAttrs):
        return False
    
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
            #TODO add money from ram
            wdwPrint(msg, "As you put the valuable sand into your pocket Gabe Newell jumps up and scares you!")
            keyToCont(msg)
            if not fight(gabe, player, msg, side, art, enemyAttrs):
                return False
            #Maybe gabe steals some of the money back after
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
            #TODO add money from calc
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


    if choice1 == "tech" and choice4 == "science":
        wdwPrint(msg, "good ending")
    elif choice1 == "math" and choice4 == "english":
        wdwPrint(msg, "Bad ending")
    else:
        wdwPrint(msg, "neutral ending")
    
    # if no file make file
    try:
        open("scores.txt", "r").close()
    except FileNotFoundError:
        open("scores.txt", "w").close()

    with open("scores.txt", "a") as f:
        n = player.name
        s = str(player.getGold() + player.getHP())
        # create hash
        h = hashlib.sha512(n.encode("utf-8") + s.encode("utf-8")).hexdigest()[:10]
        f.write(f"{n}:{s}:{h}\n")

    stdscr.getch()

    return True

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
