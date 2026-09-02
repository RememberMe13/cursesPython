import curses
from curses.textpad import rectangle


def main(stdscr):
    while True:
        key = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(0, 0, str(key))
        stdscr.refresh()

curses.wrapper(main)
