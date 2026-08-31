#!/usr/bin/python
import curses

from name import getName
from player import Player
from windows import setupWindows


def wdwPrint(window, msg, y=0, x=0):
    window.clear()
    window.addstr(y, x, msg)
    window.refresh()


def main(stdscr):
    minX = 93
    minY = 25
    if (curses.COLS < minX) or (curses.LINES < minY):
        stdscr.clear()
        stdscr.addstr(0, 0,
                      f"Terminal size too small: "
                      f"{curses.COLS}x{curses.LINES}.\nRequired: "
                      f"{minX}x{minY}"
        )
        stdscr.refresh()
        stdscr.getch()
        return

    # Disables the cursor if False
    curses.curs_set(True)
    
    # Set up colours
    curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    name = getName(stdscr)
    player = Player(name)

    # Get the 3 windows that setupWindows makes
    msg, side, art = setupWindows(stdscr)

    side.addstr(0, 0, "Player: " + name)
    side.addstr(1, 0, "HP: " + str(player.getHP()))
    side.addstr(2, 0, "Gold: " + str(player.getGold()))
    side.bkgd(' ', curses.color_pair(1))
    side.refresh()

    art.addstr(0, 0, "I am printing stuf")
    art.bkgd(' ', curses.color_pair(2))
    art.refresh()

    msg.addstr(0, 0, "You enter the hallway...")
    msg.bkgd(' ', curses.color_pair(3))    
    msg.refresh()
    

    # --------------- START GAME ------------- #
    """mPrint(
        msg,
        "“I arrived at school on a chilly, windy morning.”\n"
        "“I hadn't slept too well last night, too much Math homework.”\n"
        "“As I stepped up the ramp leading into the school, I saw…”"
    )"""
    wdwPrint(
        msg,
        "I arrived at school on a chilly, windy morning.\n"
        "I hadn't slept too well last night, too much Math homework.\n"
        "As I stepped up the ramp leading into the school, I saw…"
    )
 
    wdwPrint(art, monster)















    # this just exits on keypress after everything else
    stdscr.getch()








monster = r'''        .-"""".
       /       \
   __ /   .-.  .\
  /  `\  /   \/  \
  |  _ \/   .==.==.
  | (   \  /____\__\
   \ \      (_()(_()
    \ \            '---._
     \                   \_
  /\ |`       (__)________/
 /  \|     /\___/
|    \     \||VV
|     \     \|"""",
|      \     ______)
\       \  /`
jgs      \('''




curses.wrapper(main)
