#!/usr/bin/python
import curses
from curses.textpad import Textbox, rectangle


def display(y, x, screen):
    out = []
    while True:
        key = screen.getch()
        if key == 10:
            break
        char = chr(key)
        out.append(char)
    res = "".join(out)
    screen.addstr(y, x, res)
    screen.refresh()


def main(stdscr):
    # Disables the cursor
    curses.curs_set(False)

    # Makes a new window, and textbox
    win = curses.newwin(3, 18, 2, 2)
    box = Textbox(win)

    # Makes a new rectable (basically a border)
    rectangle(stdscr, 1, 1, 5, 20)
    stdscr.refresh()
    
    # Makes an editable text box
    box.edit()
    text = box.gather().upper().replace("\n", "").strip()
    stdscr.addstr(10, 40, text)
    
    display(20, 20, stdscr)

    # Exits on any keypress
    stdscr.getch()

curses.wrapper(main)
