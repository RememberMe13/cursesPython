import curses
from curses.textpad import Textbox, rectangle

from scores import scores


def showIntro(window, version):
    window.clear()
    midY = int(curses.LINES / 2)
    midX = int(curses.COLS / 2)
   
    message = "enter start to start, scores for scores, quit for exit."
    title = "GAME NAME HERE"


    window.addstr((midY - 5), (midX - int(len(title) / 2)), title, curses.A_BOLD)
    window.addstr((midY - 2), (midX - int(len(message) / 2)), message)
    window.addstr(curses.LINES - 1, 0, str(version))

    # number of lines, number of cols, startY startX
    win1 = curses.newwin(1, 15, midY, (midX - 7))
    box = Textbox(win1)

    # Draw a rectangle (border)
    rectangle(window, (midY - 1), (midX - 8), (midY + 1), (midX + 8))
    window.refresh()

    box.edit()
    text = box.gather().strip()

    if text == "start":
        return "start"
    elif text == "scores":
        return "scores"
    elif text == "quit":
        return "quit"

def showScores(window):
    window.clear()
    window.addstr(0, 0, "scores\nPress any key to continue.")
    for i, (name, score) in enumerate(scores.items(), start = 2):
        window.addstr(i, 0, f"{name}:{score}")
    window.refresh()
    window.getch()


if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
