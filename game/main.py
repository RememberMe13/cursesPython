#!/usr/bin/python
import curses
from curses.textpad import Textbox, rectangle

from name import getName
from windows import setupWindows


def mPrint(window, msg, y=0, x=0):
    window.clear()
    window.addstr(y, x, msg)
    window.refresh()


def main(stdscr):
    # Disables the cursor if False
    curses.curs_set(True)

    # Set up colours
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    name = getName(stdscr)

    # Get the 3 windows that setupWindows makes
    msg, side, art = setupWindows(stdscr)

    side.addstr(0, 0, "Player: " + name)
    side.bkgd(' ', curses.color_pair(1))
    side.refresh()

    art.addstr(0, 0, "I am printing stuf")
    art.bkgd(' ', curses.color_pair(2))
    art.refresh()

    msg.addstr(0, 0, "You enter the hallway...")
    msg.bkgd(' ', curses.color_pair(3))    
    msg.refresh()
    

    # --------------- START GAME ------------- #
    mPrint(
        msg,
        "“I arrived at school on a chilly, windy morning.”\n"
        "“I hadn't slept too well last night, too much Math homework.”\n"
        "“As I stepped up the ramp leading into the school, I saw…”"
    )

















    # this just exits on keypress after everything else
    stdscr.getch()



curses.wrapper(main)
