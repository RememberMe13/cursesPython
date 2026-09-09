#!/usr/bin/python
import curses

from game.game import game
from game.intro import *
from game.name import getName
from game.player import Player
from game.windows import setupWindows


def main(stdscr):
    minX = 93
    minY = 26
    version = 0.1
    if (curses.COLS < minX) or (curses.LINES < minY):
        stdscr.erase()
        stdscr.addstr(0, 0,
                      f"Terminal size too small: "
                      f"{curses.COLS}x{curses.LINES}.\nRequired: "
                      f"{minX}x{minY}"
        )
        stdscr.refresh()
        stdscr.getch()
        return

    # Disables the cursor if False
    curses.curs_set(True)
    
    # Set up colours
    curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    while True:
        choice = showIntro(stdscr, version)

        if choice == "start":
            stdscr.erase()
            break
        elif choice == "scores":
            showScores(stdscr)
        elif choice == "quit":
            return



    name = getName(stdscr)
    player = Player(name)

    # Get the 4 windows that setupWindows makes
    msg, side, art, enemyAttrs = setupWindows(stdscr)

    if not game(player, msg, side, art, enemyAttrs, stdscr):
        showDeath(stdscr)
    else:
        showWin(stdscr)
    showScores(stdscr)



curses.wrapper(main)
print("Program finished succesfully")
