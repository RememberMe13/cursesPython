#!/usr/bin/python
import curses
import time
from curses.textpad import Textbox, rectangle
from windows import setupWindows


def main(stdscr):
    # Disables the cursor if False
    curses.curs_set(True)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

    name = getName(stdscr)

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
    
    

    stdscr.getch()



def getName(window):
    midY = int(curses.LINES / 2)
    midX = int(curses.COLS / 2)
    
    window.addstr((midY - 2), (midX - 11), "Please enter your name:")

    # number of lines, number of cols, startY startX
    win1 = curses.newwin(1, 9, midY, (midX - 7))
    box = Textbox(win1)

    # Draw a rectangle (border)
    rectangle(window, (midY - 1), (midX - 8), (midY + 1), (midX + 8))
    window.refresh()

    box.edit()
    text = box.gather().replace("\n", "").strip().capitalize()

    curses.curs_set(False)
    window.clear()
    
    window.addstr(midY, int(midX - len(text) / 2), text, curses.A_BLINK | curses.A_BOLD)
    window.refresh()
    time.sleep(0.2) #TODO change time when finished

    window.clear()
    return text


curses.wrapper(main)
