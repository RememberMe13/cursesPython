import curses
from curses.textpad import rectangle


def showIntro(window, version):
    window.erase()
    choice = "start"

    #window.clear()
    midY = int(curses.LINES / 2)
    midX = int(curses.COLS / 2)
   
    title = r"""   _________    __  _________   _   _____    __  _________    __  ____________  ______
  / ____/   |  /  |/  / ____/  / | / /   |  /  |/  / ____/   / / / / ____/ __ \/ ____/
 / / __/ /| | / /|_/ / __/    /  |/ / /| | / /|_/ / __/     / /_/ / __/ / /_/ / __/   
/ /_/ / ___ |/ /  / / /___   / /|  / ___ |/ /  / / /___    / __  / /___/ _, _/ /___   
\____/_/  |_/_/  /_/_____/  /_/ |_/_/  |_/_/  /_/_____/   /_/ /_/_____/_/ |_/_____/   """

    window.addstr(curses.LINES - 1, 0, str(version))
    window.addstr(curses.LINES - 1, curses.COLS - 11, "By Henry M")

    # Disable cursor block
    curses.curs_set(False)

    st = curses.newwin(1, 2, 13, midX - 10)
    sc = curses.newwin(1, 2, 16, midX - 10)
    qu = curses.newwin(1, 2, 19, midX - 10)
    tWin = curses.newwin(5, 88, 3, midX - 42)
    
    rectangle(window, 12, midX - 11, 14, midX - 8)
    rectangle(window, 15, midX - 11, 17, midX - 8)
    rectangle(window, 18, midX - 11, 20, midX - 8)
    
    window.addstr(13, midX - 5, "Start")
    window.addstr(16, midX - 5, "Scores")
    window.addstr(19, midX - 5, "Quit")
    tWin.addstr(0, 0, title)

    window.refresh()
    tWin.refresh()
    blocks = [st, sc, qu]

    def increment(choice):
        if choice == "start":
            return "scores"
        elif choice == "scores":
            return "quit"
        elif choice == "quit":
            return "start"

    def deincrement(choice):
        if choice == "start":
            return "quit"
        elif choice == "scores":
            return "start"
        elif choice == "quit":
            return "scores"


    while True:
        for i in blocks:
            i.bkgd(' ', curses.color_pair(4))
            i.refresh()
        if choice == "start":
            st.bkgd(' ', curses.color_pair(3))
            st.refresh()
        elif choice == "scores":
            sc.bkgd(' ', curses.color_pair(3))
            sc.refresh()
        elif choice == "quit":
            qu.bkgd(' ', curses.color_pair(3))
            qu.refresh()
        
        key = window.getch()
        if key == 10:
            break
        elif key == 258:
            choice = increment(choice)
        elif key == 259:
            choice = deincrement(choice)

    if choice == "start":
        return "start"
    elif choice == "scores":
        return "scores"
    elif choice == "quit":
        return "quit"

def showScores(window):
    count = 3

    window.clear()
    window.addstr(0, 0, "scores\nPress any key to continue.")

    with open("scores.txt", "r") as f:
        for line in f:
            window.addstr(count, 0, line)
            count += 1
    window.refresh()

    window.getch()


if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
