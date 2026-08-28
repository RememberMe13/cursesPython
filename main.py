#!/usr/bin/python
import curses
import time
from curses.textpad import Textbox, rectangle
from windows import setupWindows


def main(stdscr):
    # Disables the cursor if False
    curses.curs_set(True)

    name = getName(stdscr)

    msg, side, art = setupWindows(stdscr)

    side.addstr(0, 0, "Player: " + name)
    side.refresh()

    art.addstr(0, 0, "I LOVE PYTHON")
    art.refresh()

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
    time.sleep(2)

    window.clear()
    return text


curses.wrapper(main)
