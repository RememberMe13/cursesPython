import curses
import hashlib
from curses.textpad import rectangle


def showIntro(window, version):
    window.erase()
    choice = "start"

    #window.clear()
    midX = int(curses.COLS / 2)
   
    title = r"""   _________    __  _________   _   _____    __  _________    __  ____________  ______
  / ____/   |  /  |/  / ____/  / | / /   |  /  |/  / ____/   / / / / ____/ __ \/ ____/
 / / __/ /| | / /|_/ / __/    /  |/ / /| | / /|_/ / __/     / /_/ / __/ / /_/ / __/   
/ /_/ / ___ |/ /  / / /___   / /|  / ___ |/ /  / / /___    / __  / /___/ _, _/ /___   
\____/_/  |_/_/  /_/_____/  /_/ |_/_/  |_/_/  /_/_____/   /_/ /_/_____/_/ |_/_____/   """

    # version and me
    window.addstr(curses.LINES - 1, 0, str(version))
    window.addstr(curses.LINES - 1, curses.COLS - 11, "By Henry M")

    # Disable cursor block
    curses.curs_set(False)
    
    # define 'windows' (just the boxes that light up)
    st = curses.newwin(1, 2, 13, midX - 10)
    sc = curses.newwin(1, 2, 16, midX - 10)
    qu = curses.newwin(1, 2, 19, midX - 10)
    tWin = curses.newwin(5, 88, 3, midX - 42)
    
    # draw borders around boxes
    rectangle(window, 12, midX - 11, 14, midX - 8)
    rectangle(window, 15, midX - 11, 17, midX - 8)
    rectangle(window, 18, midX - 11, 20, midX - 8)
    
    # add labels
    window.addstr(13, midX - 5, "Start")
    window.addstr(16, midX - 5, "Scores")
    window.addstr(19, midX - 5, "Quit")
    tWin.addstr(0, 0, title)
    
    # draw the stuff
    window.refresh()
    tWin.refresh()
    blocks = [st, sc, qu]
    
    # changes what box is highlighted
    def increment(choice):
        if choice == "start":
            return "scores"
        elif choice == "scores":
            return "quit"
        elif choice == "quit":
            return "start"

    # same as before
    def deincrement(choice):
        if choice == "start":
            return "quit"
        elif choice == "scores":
            return "start"
        elif choice == "quit":
            return "scores"

    # menu loop
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
        
        # if key is enter stop, else change
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

# Function to show the scoreboard
def showScores(window, player = ""):
    maxY, maxX = window.getmaxyx()
    midX = int(maxX / 2)
    line = 11

    err = 0
    window.erase()
    window.addstr(8, midX - 3, "SCORES", curses.A_BOLD)
    unsort = []

    # If file no exist, make file
    try:
        open("scores.txt", "r").close()
    except FileNotFoundError:
        open("scores.txt", "w").close()
    
    # Filters and sorts the scores into unsort. It checks the hash in the file with the hash of the name and score and gets the first 10 charaters.
    with open("scores.txt", "r") as f:
        for fLine in f:
            name, score, h = fLine.strip("\n").split(":")

            # Hashing mechanism
            hashed = hashlib.sha512(name.encode("utf-8") + score.encode("utf-8")).hexdigest()[:10]
            if h != hashed:
                window.addstr(11, midX - 20, "Error: below line has an incorrect hash!")
                window.addstr(12, midX - 17, "Please remove the infringing line!")
                window.addstr(14, midX - len(name) - len(score) - 2, name + ":" + score + ":" + h)
                err = 1
                break
            else:
                unsort.append(f"{name}:{score}")
    
    # If no errors, draw scores
    if err == 0:
        num = 1
        
        # sorts it by the score at the end.
        sort = sorted(unsort, key=lambda x: int(x.split(":")[-1]), reverse=True)
        for item in sort:
            window.addstr(line, int(maxX / 3) + 1, str(num) + " " + ("-" * (int(maxX / 3) - 4 - len(item))))

            if item.split(":")[0] == player:
                window.addstr(line, (int(maxX / 3) * 2) - len(item), item, curses.A_BLINK)
            else:
                window.addstr(line, (int(maxX / 3) * 2) - len(item), item)

            line += 1
            num += 1
    
    window.addstr(maxY - 8, midX - 13, "Press anything to continue")

    window.refresh()
    window.getch()
    
# Shows the death screen
def showDeath(window, score):
    maxY, maxX = window.getmaxyx()
    x = int(maxX / 2)
    y = int(maxY / 2)

    window.erase()
    window.addstr(y - 6, x - 7, "You have died.", curses.A_BOLD)
    window.addstr(y - 4, x - 5, f"Score: {score}")
    window.addstr(maxY - 2, x - 13, "Press anything to continue")
    window.refresh()
    
    window.getch()

# Shows the win screen
def showWin(window, score):
    maxY, maxX = window.getmaxyx()
    x = int(maxX / 2)
    y = int(maxY / 2)

    window.erase()
    window.addstr(y - 6, x - 7, "You have won!", curses.A_BOLD | curses.A_BLINK)
    window.addstr(y - 4, x - 5, f"Score: {score}")
    window.addstr(maxY - 2, x - 13, "Press anything to continue")
    window.refresh()
    
    window.getch()


if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
