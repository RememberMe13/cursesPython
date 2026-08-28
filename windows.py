import curses
from curses.textpad import rectangle


def setupWindows(window):
    msg = curses.newwin(3, (curses.COLS - 4), (curses.LINES - 4), 2)
    side = curses.newwin((curses.LINES - 7), 17, 1, (curses.COLS - 19))
    art = curses.newwin((curses.LINES - 7), (curses.COLS - 24), 1, 2)

    # format: tl y/x,  br y/x
    # messages
    rectangle(window, (curses.LINES - 5), 1, (curses.LINES - 1), (curses.COLS - 2))
    # sidebar
    rectangle(window, 0, (curses.COLS - 20), (curses.LINES - 6), (curses.COLS - 2))
    # art box
    rectangle(window, 0, 1, (curses.LINES - 6), (curses.COLS - 22))
    
    window.refresh()

    
    return msg, side, art


if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
