#!/usr/bin/python
import curses


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Hello, world!", curses.A_UNDERLINE)
    stdscr.addstr(int(curses.LINES / 2), int((curses.COLS - len("Middle")) / 2), "Middle")

    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)
