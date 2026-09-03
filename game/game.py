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
    window.addstr(0, 0, "Player: " + player.getName())
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

def fight(entity, player, msg, side, art):
    wdwPrint(art, artAscii.snake)
    wdwPrint(msg, f"You are fighting {entity}")
    player.hurt(10)
    calcAttrs(player, side)
    sleep(1)
    wdwPrint(msg, f"{entity} won")
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

    #set up side panel
    calcAttrs(player, side)

    # ---------START INTRO----------- 
    wdwPrint(msg, "I arrived at school on a chilly, windy morning.", "no")
    sleep(ds)
    wdwPrint(msg, "I hadn't slept too well last night, too much Math homework.", "no", 1)
    sleep(ds)
    wdwPrint(msg, "As I stepped up the ramp leading into the school, I saw…", "no", 2)
    keyToCont(msg)
   
    wdwPrint(msg, "The squished remains of an ant I had accidentally stepped on.")
    sleep(ds)
    wdwPrint(msg, "And then out of nowhere a giant bull ant appered and challenged me to a fight!", "no", 1)
    keyToCont(msg)

    fight("BIG ANT", player, msg, side, art)
    
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
    
    

















    stdscr.getch()

if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
