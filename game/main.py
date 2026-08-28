#!/usr/bin/python
import curses
import time
from curses.textpad import Textbox, rectangle

from name import getName
from windows import setupWindows


def main(stdscr):
    # Disables the cursor if False
    curses.curs_set(True)

    # Set up colours
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    
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
    
    # this just exits on keypress after everything else
    stdscr.getch()



curses.wrapper(main)
