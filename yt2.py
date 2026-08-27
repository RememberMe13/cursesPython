#!/usr/bin/python
import curses
import time


def main(stdscr):
    #                   foreground        background
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    BLUE_AND_YELLOW = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    RED_AND_WHITE = curses.color_pair(3)

    stdscr.addstr(0, 0, "This screen is " + str(curses.LINES) + " high, and " + str(curses.COLS) + " wide.")
    
    # New pad       height, width
    pad = curses.newpad(40, 103)
    stdscr.refresh()

    for i in range(100):
        for j in range(26):
            char = chr(97 + j)
            pad.addstr(char, GREEN_AND_BLACK)


    # Start pad at 0,0, 5,5 is where the contens starts to be displayed, 25, 74 is the size of the content
    pad.refresh(1, 3, 1, 3, int(curses.LINES - 2), int(curses.COLS))
    stdscr.getch()



curses.wrapper(main)
