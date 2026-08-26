#!/usr/bin/python
import curses  # This was installed by default on my system. On windows, install windows-curses

def drawMenu(stdscr):

    # Initialise the curses object
    stdscr = curses.initscr()

    # Do not echo keys back to terminal
    curses.noecho()

    # Makes it so that curses does not wait for Enter key
    curses.cbreak()

    # Turn off blinking cursor
    curses.curs_set(False)

    # Enable color
    if curses.has_colors():
        curses.start_color()
    
    # Change colors
    curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)

    # Enables arrow keys (and others) to be thought of as single presses
    stdscr.keypad(True)


    errors = ""
    testingOut = ""

    try:
        screenDetailText = "This screen is " + str(curses.LINES) + " high, and " + str(curses.COLS) + " wide."
        startingXPos = int((curses.COLS - len(screenDetailText)) / 2)

        # In the form [posY] [posX] [text]
        stdscr.addstr(int(curses.LINES / 2), startingXPos, screenDetailText)

        # Using insstr instead of addstr means there is no line 'added?' after it.
        stdscr.insstr((int(curses.LINES) - 1), 0, "Press any key to quit.")

        # Actually draws the text above
        stdscr.refresh()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        index = 0
        done = False
        while done == False:
            # If on first iteration, skip to window
            if index != 0:
                ch = stdscr.getch()
                if ch == ord('q') or ch == ord('Q'):
                    done = True

            stdscr.bkgd(' ', curses.color_pair(1))
            if index % 2 == 0:
                stdscr.box()
            else:
                stdscr.border('l', 'r', 't', 'b', 'c', 'c', 'c', 'c')
            stdscr.refresh()

            index = 1 + index
        
        # Gets keyboard
        stdscr.getch()

    except Exception as err:
        # needed because if i print straight from here it will not work, as i am still in curses
        errors = str(err)

    # Begin shutdown
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)

    # Checking if errors or testing output
    if "" != errors:
        print(f"Got error(s): {errors}")
    
    if "" != testingOut:
        print(testingOut)

curses.wrapper(drawMenu)
