#!/usr/bin/python
import curses
import hashlib
from curses.textpad import Textbox, rectangle


def main(stdscr):
    midY = int(curses.LINES / 2)
    midX = int(curses.COLS / 2)

    # Disables the cursor if False
    curses.curs_set(True)
    
    stdscr.addstr((midY - 2), (midX - 11), "Please enter your name:")

    # number of lines, number of cols, startY startX
    win1 = curses.newwin(1, 14, midY, (midX - 7))
    box = Textbox(win1)

    # Draw a rectangle (border) TODO: try stdscr.bkgd Format: topleft y/x, bottom right y\x
    rectangle(stdscr, (midY - 1), (midX - 8), (midY + 1), (midX + 8))
    stdscr.refresh()

    box.edit()
    text = box.gather().replace("\n", "").strip()
    hshText = hashlib.md5(text.encode()).hexdigest()

    stdscr.clear()
    stdscr.addstr(midY, int(midX - len(text) / 2), text, curses.A_BLINK | curses.A_BOLD)
    stdscr.addstr((midY + 1), int(midX - len(hshText) / 2), "Hash: " + hshText)


    stdscr.getch()


curses.wrapper(main)
