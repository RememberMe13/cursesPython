import curses
from curses.textpad import rectangle

# This is a homemade dev tool that shows the key number of any key typed.

def main(stdscr):
    while True:
        key = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(0, 0, str(key))
        stdscr.refresh()

curses.wrapper(main)
