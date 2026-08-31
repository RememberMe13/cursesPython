import curses
from curses.textpad import rectangle


def setupWindows(window):
    
    
    # nlines, ncols, startX, startY
    msg = curses.newwin(5, (curses.COLS - 4), (curses.LINES - 6), 2)
    side = curses.newwin((curses.LINES - 9), 23, 1, (curses.COLS - 25))
    art = curses.newwin((curses.LINES - 9), (curses.COLS - 30), 1, 2)

    # format: tl y/x,  br y/x
    # messages
    rectangle(window, (curses.LINES - 7), 1, (curses.LINES - 1), (curses.COLS - 2))
    # sidebar
    rectangle(window, 0, (curses.COLS - 26), (curses.LINES - 8), (curses.COLS - 2))
    # art box
    rectangle(window, 0, 1, (curses.LINES - 8), (curses.COLS - 28))
    
    window.refresh()

    
    return msg, side, art


if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
