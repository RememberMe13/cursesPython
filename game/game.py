import curses
from curses.textpad import Textbox
from time import sleep

import artAscii


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

def getInput(nLines, nCols, startY, startX):
    win1 = curses.newwin(nLines, nCols, startY, startX)
    box = Textbox(win1)

    box.edit()
    text = box.gather().strip().lower()
    return text

def fight(name, artName, player, msg, side, art):
    wdwPrint(art, getattr(artAscii, artName))
    wdwPrint(msg, f"You are fighting {name}")
    player.hurt(10)
    calcAttrs(player, side)
    sleep(1)
    wdwPrint(msg, f"{name} won")
    keyToCont(msg)

    art.erase()
    msg.erase()
    art.refresh()
    msg.refresh()

def game(player, msg, side, art, stdscr):
    #Default sleep time
    ds = 1

    #choices are here for easier looking back at
    choice1 = "" # tech / math
    choice2 = "" # yes / no
    choice3 = 0  # 1-4
    choice4 = "" # science / english
    choice5 = "" # yes / no

    #Set backgrounds
    art.bkgd(' ', curses.color_pair(2))
    msg.bkgd(' ', curses.color_pair(3))
    side.bkgd(' ', curses.color_pair(1))
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
    fight("BIG ANT", "snake", player, msg, side, art)
    
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
                wdwPrint(msg, f"you chose {choice2}")
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice2 == "yes":
            #TODO add money from ram
            wdwPrint(msg, "As you put the valuable sand into your pocket Gabe Newell jumps up and scares you!")
            fight("Gabe Newell", "face", player, msg, side, art)
            #Maybe gabe steals some of the money back after
        elif choice2 == "no":
            wdwPrint(msg, "As you walk away from the expensive sand you accidentally touch a live wire!")
            player.hurt(5)
            calcAttrs(player, side)
            fight("Live Wire", "monster", player, msg, side, art)

    elif choice1 == "math":
        while True:
            wdwPrint(msg, "As you reminece about your CASIO FX-1AU graphing calculator you spot one unatended\n on a table!")
            sleep(ds)
            wdwPrint(msg, "Do you take the $270 calculator? yes/no", "no", 2)
            wdwPrint(msg, "->", "no", 3)
            choice2 = getInput(1, 4, curses.LINES - 3, 5)
            if choice2 == "yes" or choice2 == "no":
                wdwPrint(msg, f"you chose {choice2}")
                break
            else:
                wdwPrint(msg, "Please enter yes or no!")
                sleep(ds)

        if choice2 == "yes":
            #TODO add money from calc
            wdwPrint(msg, "As you put the overpriced computer in your pocket an angry Math teacher approaches!")
            fight("well known math teacher", "face", player, msg, side, art)
        elif choice2 == "no":
            wdwPrint(msg, "As you walk away from the calc (short for calculator) you step on an upturned protractor!")
            player.hurt(5)
            calcAttrs(player, side)
            fight("Angry protractor", "monster", player, msg, side, art)


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
                continue
            choice3 = int(choice3)
        except ValueError:
            wdwPrint(msg, "Please enter a number!")
            sleep(ds)

        if choice3 in [1, 2, 3, 4]:
            wdwPrint(msg, f"Choice: {choice3}")
            break
        else:
            wdwPrint(msg, "Please enter a number from 1 to 4!")
            sleep(ds)


            















    stdscr.getch()

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
